from __future__ import annotations

import logging

from dataclasses import dataclass

from app.domain.enums import CaseStatus, ControlStatus, FindingStatus, MeasureStatus, ROLE_TIERS, RoleCode
from app.domain.models import CaseActionState, GovernancePolicy, ReviewCase
from app.infrastructure.database import utc_now

log = logging.getLogger(__name__)


@dataclass(slots=True)
class ActionResult:
    ok: bool
    message: str
    case: ReviewCase | None = None
    code: str | None = None


class SessionService:
    def __init__(self, user_repo: object, role_binding_repo: object, session_state: object) -> None:
        self.user_repo = user_repo
        self.role_binding_repo = role_binding_repo
        self.session_state = session_state

    def list_users(self):
        return self.user_repo.list_users()

    def get_current_user(self):
        return self.user_repo.get_user(self.session_state.current_user_id)

    def get_current_roles(self) -> list[str]:
        return self.role_binding_repo.get_roles_for_user(self.session_state.current_user_id)

    def switch_user(self, user_id: int) -> None:
        user = self.user_repo.get_user(user_id)
        if user is None:
            raise ValueError(f"Unknown user id {user_id}")
        self.session_state.current_user_id = user_id

    def has_role(self, role_code: RoleCode) -> bool:
        return role_code.value in self.get_current_roles()

    def effective_tier(self) -> int:
        tier = 0
        for role_code in self.get_current_roles():
            try:
                tier = max(tier, ROLE_TIERS[RoleCode(role_code)])
            except Exception:
                continue
        return tier


class AuditService:
    def __init__(self, audit_repo: object) -> None:
        self.audit_repo = audit_repo

    def list_events(self, limit: int = 200):
        return self.audit_repo.list_events(limit=limit)

    def log(
        self,
        *,
        actor_user_id: int | None,
        severity: str = "info",
        domain: str,
        action: str,
        entity_type: str,
        entity_id: int | None,
        payload: dict[str, object],
    ) -> None:
        log.info(
            "audit_event",
            extra={
                "domain": domain,
                "action": action,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "severity": severity,
            },
        )
        self.audit_repo.add_event(
            actor_user_id=actor_user_id,
            severity=severity,
            domain=domain,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )


class GovernanceService:
    def __init__(self, governance_repo: object, audit_service: AuditService, session_service: SessionService) -> None:
        self.governance_repo = governance_repo
        self.audit_service = audit_service
        self.session_service = session_service

    def get_policy(self) -> GovernancePolicy:
        return self.governance_repo.get_policy()

    def update_policy(self, *, read_only_enabled: bool, review_cases_enabled: bool) -> tuple[bool, str, GovernancePolicy]:
        current_policy = self.get_policy()
        actor_id = self.session_service.session_state.current_user_id
        if not self.session_service.has_role(RoleCode.ADMIN):
            log.warning("Blocked governance policy update for non-admin user_id=%s", actor_id)
            self.audit_service.log(
                actor_user_id=actor_id,
                severity="warning",
                domain="governance",
                action="blocked",
                entity_type="policy",
                entity_id=current_policy.id,
                payload={
                    "reason": "admin_required",
                    "attempted_read_only": read_only_enabled,
                    "attempted_review_cases": review_cases_enabled,
                },
            )
            return False, "Only admins can change governance settings.", current_policy

        if (
            current_policy.read_only_enabled == read_only_enabled
            and current_policy.feature_flags.get("review_cases", True) == review_cases_enabled
        ):
            log.info("Governance policy unchanged for user_id=%s", actor_id)
            return True, "No governance changes were necessary.", current_policy

        policy = self.governance_repo.update_policy(
            read_only_enabled=read_only_enabled,
            feature_flags={"review_cases": review_cases_enabled},
            updated_by=actor_id,
        )
        self.audit_service.log(
            actor_user_id=actor_id,
            severity="info",
            domain="governance",
            action="policy.updated",
            entity_type="policy",
            entity_id=policy.id,
            payload={
                "before": {
                    "read_only_enabled": current_policy.read_only_enabled,
                    "feature_flags": current_policy.feature_flags,
                },
                "after": {
                    "read_only_enabled": policy.read_only_enabled,
                    "feature_flags": policy.feature_flags,
                },
            },
        )
        log.info(
            "Governance policy updated by user_id=%s read_only=%s review_cases=%s",
            actor_id,
            policy.read_only_enabled,
            policy.feature_flags.get("review_cases", True),
        )
        return True, "Governance settings saved.", policy


class CaseService:
    def __init__(
        self,
        review_case_repo: object,
        governance_service: GovernanceService,
        session_service: SessionService,
        audit_service: AuditService,
    ) -> None:
        self.review_case_repo = review_case_repo
        self.governance_service = governance_service
        self.session_service = session_service
        self.audit_service = audit_service

    def list_cases(self):
        return self.review_case_repo.list_cases()

    def get_case(self, case_id: int):
        return self.review_case_repo.get_case(case_id)

    def get_case_action_state(self, case_id: int) -> CaseActionState:
        case = self.get_case(case_id)
        if case is None:
            return CaseActionState(
                case_id=case_id,
                allowed_actions={},
                primary_hint="Case not found.",
                blocker_code="missing",
            )
        actions = (
            "claim",
            "unclaim",
            "approved",
            "rejected",
            "closed",
            "assign_measure_owner",
            "start_measure",
            "mitigate",
            "accept_risk",
        )
        allowed = {action: self._validate_case_action(case, action) is None for action in actions}
        available_labels = [label for action, label in self._action_labels().items() if allowed.get(action)]
        blocker = self._first_relevant_blocker(case) if not available_labels else None
        return CaseActionState(
            case_id=case_id,
            allowed_actions=allowed,
            primary_hint=(
                f"Available next steps: {', '.join(available_labels)}."
                if available_labels
                else blocker[1] if blocker is not None
                else "No actions available."
            ),
            blocker_code=None if blocker is None else blocker[0],
        )

    def claim_case(self, case_id: int) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, "claim")
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action="claim")
        updated = self.review_case_repo.update_case(
            case_id=case_id,
            status=CaseStatus.CLAIMED.value,
            claimed_by=self.session_service.session_state.current_user_id,
            claimed_at=utc_now(),
            decision=None,
            decision_reason=None,
        )
        self._audit_case("claimed", updated, {"status": updated.status, "claimed_by": updated.claimed_by})
        log.info("Case claimed case_id=%s actor_user_id=%s", case_id, self.session_service.session_state.current_user_id)
        return ActionResult(True, "Case claimed.", updated, code="claimed")

    def unclaim_case(self, case_id: int) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, "unclaim")
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action="unclaim")
        updated = self.review_case_repo.update_case(
            case_id=case_id,
            status=CaseStatus.OPEN.value,
            claimed_by=None,
            claimed_at=None,
            decision=None,
            decision_reason=None,
        )
        self._audit_case(
            "unclaimed",
            updated,
            {"status": updated.status, "released_by": self.session_service.session_state.current_user_id},
        )
        log.info("Case unclaimed case_id=%s actor_user_id=%s", case_id, self.session_service.session_state.current_user_id)
        return ActionResult(True, "Case returned to the queue.", updated, code="unclaimed")

    def decide_case(self, case_id: int, decision: str) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, decision)
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action=decision)

        current_user_id = self.session_service.session_state.current_user_id
        if decision in {"approved", "rejected"}:
            new_status = CaseStatus.APPROVED.value if decision == "approved" else CaseStatus.REJECTED.value
            reason = (
                "Approved after role and control review."
                if decision == "approved"
                else "Rejected because supporting rationale remains incomplete."
            )
        elif decision == "closed":
            new_status = CaseStatus.CLOSED.value
            reason = case.decision_reason or "Case closed after review."
        else:
            return ActionResult(False, f"Unsupported decision {decision}.", case, code="unsupported")

        updated = self.review_case_repo.update_case(
            case_id=case_id,
            status=new_status,
            finding_status=FindingStatus.CLOSED.value if decision == "closed" else None,
            control_status=ControlStatus.EFFECTIVE.value if decision == "closed" else None,
            claimed_by=case.claimed_by if case.claimed_by is not None else current_user_id,
            claimed_at=utc_now() if case.claimed_at is None else case.claimed_at.isoformat(),
            decision=None if decision == "closed" else decision,
            decision_reason=reason,
        )
        self._audit_case(
            decision,
            updated,
            {
                "status": updated.status,
                "decision": updated.decision,
                "decision_reason": updated.decision_reason,
                "claimed_by": updated.claimed_by,
            },
            severity="warning" if decision == "rejected" else "info",
        )
        log.info(
            "Case decision recorded case_id=%s decision=%s actor_user_id=%s",
            case_id,
            decision,
            self.session_service.session_state.current_user_id,
        )
        return ActionResult(True, f"Case {updated.status}.", updated, code=updated.status)

    def assign_measure_owner_to_current_user(self, case_id: int) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, "assign_measure_owner")
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action="assign_measure_owner")
        actor_id = self.session_service.session_state.current_user_id
        updated = self.review_case_repo.update_case(
            case_id=case_id,
            status=case.status,
            measure_owner=actor_id,
            claimed_by=case.claimed_by,
            claimed_at=None if case.claimed_at is None else case.claimed_at.isoformat(),
            decision=case.decision,
            decision_reason=case.decision_reason,
            evidence_note=case.evidence_note or "Measure owner assigned for remediation tracking.",
        )
        self._audit_case(
            "measure.owner_assigned",
            updated,
            {"measure_owner": updated.measure_owner, "finding_status": updated.finding_status},
        )
        return ActionResult(True, "Measure owner assigned to the active user.", updated, code="measure_owner_assigned")

    def start_measure(self, case_id: int) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, "start_measure")
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action="start_measure")
        actor_id = self.session_service.session_state.current_user_id
        updated = self.review_case_repo.update_case(
            case_id=case_id,
            status=case.status,
            finding_status=FindingStatus.IN_PROGRESS.value,
            control_status=ControlStatus.PARTIALLY_EFFECTIVE.value,
            measure_status=MeasureStatus.IN_PROGRESS.value,
            measure_owner=case.measure_owner if case.measure_owner is not None else actor_id,
            claimed_by=case.claimed_by,
            claimed_at=None if case.claimed_at is None else case.claimed_at.isoformat(),
            decision=case.decision,
            decision_reason=case.decision_reason,
            evidence_note="Mitigation work started and ownership confirmed.",
        )
        self._audit_case(
            "measure.started",
            updated,
            {
                "measure_status": updated.measure_status,
                "finding_status": updated.finding_status,
                "measure_owner": updated.measure_owner,
            },
        )
        return ActionResult(True, "Mitigation measure is now in progress.", updated, code="measure_started")

    def progress_finding(self, case_id: int, action: str) -> ActionResult:
        case = self.get_case(case_id)
        if case is None:
            return ActionResult(False, "Case not found.", code="missing")
        blocked = self._validate_case_action(case, action)
        if blocked is not None:
            return self._blocked_result(case, blocked[0], blocked[1], action=action)

        if action == "mitigate":
            updated = self.review_case_repo.update_case(
                case_id=case_id,
                status=case.status,
                finding_status=FindingStatus.MITIGATED.value,
                control_status=ControlStatus.MONITORED.value,
                measure_status=MeasureStatus.COMPLETED.value,
                measure_owner=case.measure_owner,
                claimed_by=case.claimed_by,
                claimed_at=None if case.claimed_at is None else case.claimed_at.isoformat(),
                decision=case.decision,
                decision_reason=case.decision_reason,
                evidence_note="Mitigation completed; control is now under monitoring.",
            )
            self._audit_case(
                "finding.mitigated",
                updated,
                {
                    "finding_status": updated.finding_status,
                    "measure_status": updated.measure_status,
                    "control_status": updated.control_status,
                },
            )
            return ActionResult(True, "Finding marked as mitigated.", updated, code="finding_mitigated")

        if action == "accept_risk":
            updated = self.review_case_repo.update_case(
                case_id=case_id,
                status=case.status,
                finding_status=FindingStatus.ACCEPTED.value,
                control_status=ControlStatus.MONITORED.value,
                measure_status=MeasureStatus.ACCEPTED.value,
                measure_owner=case.measure_owner,
                claimed_by=case.claimed_by,
                claimed_at=None if case.claimed_at is None else case.claimed_at.isoformat(),
                decision=case.decision,
                decision_reason=case.decision_reason or "Residual risk accepted with documented owner.",
                evidence_note="Residual risk acceptance recorded for this item.",
            )
            self._audit_case(
                "risk.accepted",
                updated,
                {
                    "finding_status": updated.finding_status,
                    "measure_status": updated.measure_status,
                    "risk_level": updated.risk_level,
                },
                severity="warning",
            )
            return ActionResult(True, "Residual risk accepted for this item.", updated, code="risk_accepted")

        return ActionResult(False, f"Unsupported progression action {action}.", case, code="unsupported")

    def _policy_blocker(self) -> tuple[str, str] | None:
        policy = self.governance_service.get_policy()
        if policy.read_only_enabled:
            return "read_only", "Changes are blocked because read-only mode is enabled."
        if not policy.feature_flags.get("review_cases", True):
            return "feature_disabled", "Review Cases are disabled by governance policy."
        if self.session_service.effective_tier() < ROLE_TIERS[RoleCode.REVIEWER]:
            return "role_insufficient", "Your current role cannot change review cases."
        return None

    def _validate_case_action(self, case: ReviewCase, action: str) -> tuple[str, str] | None:
        policy_blocker = self._policy_blocker()
        if policy_blocker is not None:
            return policy_blocker

        current_user_id = self.session_service.session_state.current_user_id
        is_admin = self.session_service.has_role(RoleCode.ADMIN)

        if action == "claim":
            if case.status != CaseStatus.OPEN.value:
                return "invalid_status", "Only open cases can be claimed."
            if case.claimed_by is not None:
                return "already_claimed", "This case already has an owner."
            return None

        if action == "unclaim":
            if case.status != CaseStatus.CLAIMED.value:
                return "invalid_status", "Only claimed cases can be released."
            if case.claimed_by != current_user_id and not is_admin:
                return "claim_owner_required", "Only the current owner or an admin can unclaim this case."
            return None

        if action in {"approved", "rejected"}:
            if case.status != CaseStatus.CLAIMED.value:
                return "claim_required", "Claim the case before approving or rejecting it."
            if case.claimed_by != current_user_id and not is_admin:
                return "claim_owner_required", "Only the claim owner or an admin can decide this case."
            return None

        if action == "closed":
            if case.status not in {CaseStatus.APPROVED.value, CaseStatus.REJECTED.value}:
                return "decision_required", "Only approved or rejected cases can be closed."
            if case.finding_status not in {FindingStatus.MITIGATED.value, FindingStatus.ACCEPTED.value}:
                return "finding_resolution_required", "Mitigate the finding or record a residual-risk acceptance before closing."
            if case.claimed_by != current_user_id and not is_admin:
                return "claim_owner_required", "Only the claim owner or an admin can close this case."
            return None

        if action == "assign_measure_owner":
            if case.status == CaseStatus.CLOSED.value:
                return "invalid_status", "Closed cases do not need a new measure owner."
            return None

        if action == "start_measure":
            if case.status == CaseStatus.CLOSED.value:
                return "invalid_status", "Closed cases cannot start new mitigation work."
            if case.finding_status not in {FindingStatus.IDENTIFIED.value, FindingStatus.IN_PROGRESS.value}:
                return "invalid_finding_state", "Only identified or active findings can start mitigation work."
            return None

        if action == "mitigate":
            if case.status == CaseStatus.CLOSED.value:
                return "invalid_status", "Closed cases cannot be mitigated again."
            if case.measure_owner is None:
                return "measure_owner_required", "Assign a measure owner before marking the finding as mitigated."
            if case.measure_status not in {MeasureStatus.IN_PROGRESS.value, MeasureStatus.PLANNED.value}:
                return "measure_progress_required", "Mitigation can only complete after a planned or active measure exists."
            return None

        if action == "accept_risk":
            if not is_admin:
                return "admin_required", "Only admins can record a residual-risk acceptance."
            if case.status == CaseStatus.CLOSED.value:
                return "invalid_status", "Closed cases cannot accept new residual risk."
            if case.finding_status in {FindingStatus.MITIGATED.value, FindingStatus.CLOSED.value}:
                return "invalid_finding_state", "Mitigated or closed findings do not need residual-risk acceptance."
            return None

        return "unsupported", f"Unsupported action: {action}"

    def _first_relevant_blocker(self, case: ReviewCase) -> tuple[str, str] | None:
        for action in ("claim", "start_measure", "mitigate", "closed"):
            blocked = self._validate_case_action(case, action)
            if blocked is not None:
                return blocked
        return None

    @staticmethod
    def _action_labels() -> dict[str, str]:
        return {
            "claim": "Claim",
            "unclaim": "Unclaim",
            "approved": "Approve",
            "rejected": "Reject",
            "closed": "Close",
            "assign_measure_owner": "Assign Owner",
            "start_measure": "Start Measure",
            "mitigate": "Mark Mitigated",
            "accept_risk": "Accept Risk",
        }

    def _blocked_result(self, case: ReviewCase, code: str, message: str, *, action: str) -> ActionResult:
        log.warning(
            "Blocked case action action=%s case_id=%s code=%s actor_user_id=%s",
            action,
            case.id,
            code,
            self.session_service.session_state.current_user_id,
        )
        self.audit_service.log(
            actor_user_id=self.session_service.session_state.current_user_id,
            severity="warning",
            domain="governance",
            action="blocked",
            entity_type="review_case",
            entity_id=case.id,
            payload={
                "requested_action": action,
                "reason": code,
                "case_status": case.status,
                "claimed_by": case.claimed_by,
            },
        )
        return ActionResult(False, message, case, code=code)

    def _audit_case(self, action: str, case: ReviewCase, payload: dict[str, object], *, severity: str = "info") -> None:
        self.audit_service.log(
            actor_user_id=self.session_service.session_state.current_user_id,
            severity=severity,
            domain="review_case",
            action=action,
            entity_type="review_case",
            entity_id=case.id,
            payload={"case_id": case.id, "title": case.title, **payload},
        )


class HealthService:
    def __init__(self, health_repo: object, migration_repo: object, governance_repo: object, user_repo: object, review_case_repo: object, audit_service: AuditService) -> None:
        self.health_repo = health_repo
        self.migration_repo = migration_repo
        self.governance_repo = governance_repo
        self.user_repo = user_repo
        self.review_case_repo = review_case_repo
        self.audit_service = audit_service

    def list_results(self, limit: int = 20):
        return self.health_repo.list_results(limit=limit)

    def get_migration_status(self):
        return self.migration_repo.get_status()

    def run_health_check(self):
        status = self.migration_repo.get_status()
        active_users = self.user_repo.list_users()
        open_cases = [
            case for case in self.review_case_repo.list_cases() if case.status == CaseStatus.OPEN.value
        ]
        overdue_measures = [
            case
            for case in self.review_case_repo.list_cases()
            if case.due_at is not None
            and case.finding_status not in {FindingStatus.MITIGATED.value, FindingStatus.ACCEPTED.value, FindingStatus.CLOSED.value}
            and case.due_at.isoformat() < utc_now()
        ]
        try:
            self.governance_repo.get_policy()
            policy_ok = True
        except Exception:
            policy_ok = False
            log.exception("Health check could not load governance policy")

        checks = [
            {"name": "schema_ok", "ok": status.schema_ok, "detail": f"missing={status.missing_items or '-'}"},
            {"name": "governance_policy_present", "ok": policy_ok, "detail": "Policy row with id=1 exists"},
            {"name": "active_user_count", "ok": len(active_users) >= 3, "detail": f"users={len(active_users)}"},
            {"name": "open_case_queue", "ok": len(open_cases) > 0, "detail": f"open_cases={len(open_cases)}"},
            {"name": "overdue_measures", "ok": len(overdue_measures) == 0, "detail": f"overdue={len(overdue_measures)}"},
        ]
        ok = all(check["ok"] for check in checks)
        message = (
            f"Schema={status.current_version}, tables={status.actual_table_count}/{status.expected_table_count}, "
            f"checks_ok={sum(1 for check in checks if check['ok'])}/{len(checks)}"
        )
        result = self.health_repo.add_result(check_type="manual", ok=ok, message=message, details={"checks": checks})
        self.audit_service.log(
            actor_user_id=None,
            severity="warning" if not ok else "info",
            domain="health",
            action="snapshot",
            entity_type="health",
            entity_id=result.id,
            payload={"ok": result.ok, "message": result.message, "checks": checks},
        )
        log.info("Health snapshot recorded ok=%s checks=%s", result.ok, len(checks))
        return result


class DashboardService:
    def __init__(
        self,
        case_service: CaseService,
        governance_service: GovernanceService,
        audit_service: AuditService,
        health_service: HealthService,
        session_service: SessionService,
    ) -> None:
        self.case_service = case_service
        self.governance_service = governance_service
        self.audit_service = audit_service
        self.health_service = health_service
        self.session_service = session_service

    def get_snapshot(self) -> dict[str, object]:
        cases = self.case_service.list_cases()
        policy = self.governance_service.get_policy()
        audits = self.audit_service.list_events(limit=5)
        health_results = self.health_service.list_results(limit=1)
        current_user = self.session_service.get_current_user()
        claimed_mine = [
            case for case in cases if case.claimed_by == self.session_service.session_state.current_user_id
        ]
        blocked_recent = [
            audit for audit in audits if audit.domain == "governance" and audit.action == "blocked"
        ]
        open_findings = [
            case
            for case in cases
            if case.finding_status in {FindingStatus.IDENTIFIED.value, FindingStatus.IN_PROGRESS.value}
        ]
        overdue_measures = [
            case
            for case in cases
            if case.due_at is not None
            and case.finding_status not in {FindingStatus.MITIGATED.value, FindingStatus.ACCEPTED.value, FindingStatus.CLOSED.value}
            and case.due_at.isoformat() < utc_now()
        ]
        accepted_risks = [case for case in cases if case.finding_status == FindingStatus.ACCEPTED.value]
        return {
            "open_cases": sum(1 for case in cases if case.status == CaseStatus.OPEN.value),
            "claimed_cases": sum(1 for case in cases if case.status == CaseStatus.CLAIMED.value),
            "my_cases": len(claimed_mine),
            "decided_cases": sum(
                1 for case in cases if case.status in {CaseStatus.APPROVED.value, CaseStatus.REJECTED.value}
            ),
            "closed_cases": sum(1 for case in cases if case.status == CaseStatus.CLOSED.value),
            "open_findings": len(open_findings),
            "overdue_measures": len(overdue_measures),
            "accepted_risks": len(accepted_risks),
            "policy": policy,
            "recent_audits": audits,
            "latest_health": health_results[0] if health_results else None,
            "recent_blocked_count": len(blocked_recent),
            "current_user": current_user,
            "current_roles": self.session_service.get_current_roles(),
        }
