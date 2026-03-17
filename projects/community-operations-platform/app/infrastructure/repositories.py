from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from app.domain.models import (
    AuditEvent,
    GovernancePolicy,
    HealthCheckResult,
    MigrationStatus,
    ReviewCase,
    RoleBinding,
    User,
)
from app.infrastructure.database import fetch_table_names, utc_now


def _dt(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


class UserRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_users(self) -> list[User]:
        rows = self.conn.execute(
            "SELECT id, display_name, is_active FROM users WHERE is_active = 1 ORDER BY display_name ASC"
        ).fetchall()
        return [User(id=int(row["id"]), display_name=str(row["display_name"]), is_active=bool(row["is_active"])) for row in rows]

    def get_user(self, user_id: int) -> User | None:
        row = self.conn.execute(
            "SELECT id, display_name, is_active FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return None
        return User(id=int(row["id"]), display_name=str(row["display_name"]), is_active=bool(row["is_active"]))


class RoleBindingRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_bindings(self) -> list[RoleBinding]:
        rows = self.conn.execute(
            "SELECT user_id, role_code, assigned_at FROM role_bindings ORDER BY role_code ASC"
        ).fetchall()
        return [
            RoleBinding(
                user_id=int(row["user_id"]),
                role_code=str(row["role_code"]),
                assigned_at=_dt(str(row["assigned_at"])) or datetime.now(),
            )
            for row in rows
        ]

    def get_roles_for_user(self, user_id: int) -> list[str]:
        rows = self.conn.execute(
            "SELECT role_code FROM role_bindings WHERE user_id = ? ORDER BY role_code ASC",
            (user_id,),
        ).fetchall()
        return [str(row["role_code"]) for row in rows]


class GovernanceRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_policy(self) -> GovernancePolicy:
        row = self.conn.execute(
            "SELECT id, read_only_enabled, feature_flags, updated_at, updated_by FROM governance_policy WHERE id = 1"
        ).fetchone()
        if row is None:
            raise RuntimeError("Governance policy is missing")
        flags = json.loads(str(row["feature_flags"]))
        return GovernancePolicy(
            id=int(row["id"]),
            read_only_enabled=bool(row["read_only_enabled"]),
            feature_flags={str(key): bool(value) for key, value in dict(flags).items()},
            updated_at=_dt(str(row["updated_at"])) or datetime.now(),
            updated_by=None if row["updated_by"] is None else int(row["updated_by"]),
        )

    def update_policy(self, *, read_only_enabled: bool, feature_flags: dict[str, bool], updated_by: int) -> GovernancePolicy:
        now = utc_now()
        with self.conn:
            self.conn.execute(
                """
                UPDATE governance_policy
                SET read_only_enabled = ?, feature_flags = ?, updated_at = ?, updated_by = ?
                WHERE id = 1
                """,
                (1 if read_only_enabled else 0, json.dumps(feature_flags, sort_keys=True), now, updated_by),
            )
        return self.get_policy()


class ReviewCaseRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_cases(self) -> list[ReviewCase]:
        rows = self.conn.execute(
            """
            SELECT id, title, summary, case_kind, risk_level, status, priority, finding_status,
                   control_status, measure_title, measure_status, measure_owner, due_at, evidence_note,
                   claimed_by, claimed_at, decision, decision_reason, created_at, updated_at
            FROM review_cases
            ORDER BY
                CASE status
                    WHEN 'claimed' THEN 0
                    WHEN 'open' THEN 1
                    ELSE 2
                END,
                updated_at DESC,
                id DESC
            """
        ).fetchall()
        return [self._row_to_case(row) for row in rows]

    def get_case(self, case_id: int) -> ReviewCase | None:
        row = self.conn.execute(
            """
            SELECT id, title, summary, case_kind, risk_level, status, priority, finding_status,
                   control_status, measure_title, measure_status, measure_owner, due_at, evidence_note,
                   claimed_by, claimed_at, decision, decision_reason, created_at, updated_at
            FROM review_cases
            WHERE id = ?
            """,
            (case_id,),
        ).fetchone()
        return None if row is None else self._row_to_case(row)

    def update_case(
        self,
        *,
        case_id: int,
        status: str,
        finding_status: str | None = None,
        control_status: str | None = None,
        measure_status: str | None = None,
        measure_owner: int | None = None,
        due_at: str | None = None,
        evidence_note: str | None = None,
        claimed_by: int | None,
        claimed_at: str | None,
        decision: str | None,
        decision_reason: str | None,
    ) -> ReviewCase:
        current = self.get_case(case_id)
        if current is None:
            raise RuntimeError("Case to update was not found")
        now = utc_now()
        with self.conn:
            self.conn.execute(
                """
                UPDATE review_cases
                SET status = ?, finding_status = ?, control_status = ?, measure_status = ?,
                    measure_owner = ?, due_at = ?, evidence_note = ?,
                    claimed_by = ?, claimed_at = ?, decision = ?, decision_reason = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    current.finding_status if finding_status is None else finding_status,
                    current.control_status if control_status is None else control_status,
                    current.measure_status if measure_status is None else measure_status,
                    current.measure_owner if measure_owner is None else measure_owner,
                    current.due_at.isoformat() if due_at is None and current.due_at is not None else due_at,
                    current.evidence_note if evidence_note is None else evidence_note,
                    claimed_by,
                    claimed_at,
                    decision,
                    decision_reason,
                    now,
                    case_id,
                ),
            )
        updated = self.get_case(case_id)
        if updated is None:
            raise RuntimeError("Updated case was not found")
        return updated

    @staticmethod
    def _row_to_case(row: sqlite3.Row) -> ReviewCase:
        return ReviewCase(
            id=int(row["id"]),
            title=str(row["title"]),
            summary=str(row["summary"]),
            case_kind=str(row["case_kind"]),
            risk_level=str(row["risk_level"]),
            status=str(row["status"]),
            priority=str(row["priority"]),
            finding_status=str(row["finding_status"]),
            control_status=str(row["control_status"]),
            measure_title=str(row["measure_title"]),
            measure_status=str(row["measure_status"]),
            measure_owner=None if row["measure_owner"] is None else int(row["measure_owner"]),
            due_at=_dt(row["due_at"]),
            evidence_note=None if row["evidence_note"] is None else str(row["evidence_note"]),
            claimed_by=None if row["claimed_by"] is None else int(row["claimed_by"]),
            claimed_at=_dt(row["claimed_at"]),
            decision=None if row["decision"] is None else str(row["decision"]),
            decision_reason=None if row["decision_reason"] is None else str(row["decision_reason"]),
            created_at=_dt(str(row["created_at"])) or datetime.now(),
            updated_at=_dt(str(row["updated_at"])) or datetime.now(),
        )


class AuditRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_events(self, limit: int = 200) -> list[AuditEvent]:
        rows = self.conn.execute(
            """
            SELECT id, occurred_at, actor_user_id, severity, domain, action, entity_type, entity_id, payload_json
            FROM audit_events
            ORDER BY occurred_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [
            AuditEvent(
                id=int(row["id"]),
                occurred_at=_dt(str(row["occurred_at"])) or datetime.now(),
                actor_user_id=None if row["actor_user_id"] is None else int(row["actor_user_id"]),
                severity=str(row["severity"]),
                domain=str(row["domain"]),
                action=str(row["action"]),
                entity_type=str(row["entity_type"]),
                entity_id=None if row["entity_id"] is None else int(row["entity_id"]),
                payload_json=str(row["payload_json"]),
            )
            for row in rows
        ]

    def add_event(
        self,
        *,
        actor_user_id: int | None,
        severity: str,
        domain: str,
        action: str,
        entity_type: str,
        entity_id: int | None,
        payload: dict[str, object],
    ) -> AuditEvent:
        now = utc_now()
        with self.conn:
            cursor = self.conn.execute(
                """
                INSERT INTO audit_events (
                    occurred_at, actor_user_id, severity, domain, action, entity_type, entity_id, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (now, actor_user_id, severity, domain, action, entity_type, entity_id, json.dumps(payload, sort_keys=True)),
            )
        event_id = int(cursor.lastrowid)
        row = self.conn.execute(
            """
            SELECT id, occurred_at, actor_user_id, severity, domain, action, entity_type, entity_id, payload_json
            FROM audit_events
            WHERE id = ?
            """,
            (event_id,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Audit event missing after insert")
        return AuditEvent(
            id=int(row["id"]),
            occurred_at=_dt(str(row["occurred_at"])) or datetime.now(),
            actor_user_id=None if row["actor_user_id"] is None else int(row["actor_user_id"]),
            severity=str(row["severity"]),
            domain=str(row["domain"]),
            action=str(row["action"]),
            entity_type=str(row["entity_type"]),
            entity_id=None if row["entity_id"] is None else int(row["entity_id"]),
            payload_json=str(row["payload_json"]),
        )


class HealthRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_results(self, limit: int = 20) -> list[HealthCheckResult]:
        rows = self.conn.execute(
            """
            SELECT id, check_type, ok, message, measured_at, details_json
            FROM health_check_results
            ORDER BY measured_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [
            HealthCheckResult(
                id=int(row["id"]),
                check_type=str(row["check_type"]),
                ok=bool(row["ok"]),
                message=str(row["message"]),
                measured_at=_dt(str(row["measured_at"])) or datetime.now(),
                details_json=str(row["details_json"]),
            )
            for row in rows
        ]

    def add_result(self, *, check_type: str, ok: bool, message: str, details: dict[str, object]) -> HealthCheckResult:
        now = utc_now()
        with self.conn:
            cursor = self.conn.execute(
                """
                INSERT INTO health_check_results (check_type, ok, message, measured_at, details_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (check_type, 1 if ok else 0, message, now, json.dumps(details, sort_keys=True)),
            )
        result_id = int(cursor.lastrowid)
        row = self.conn.execute(
            """
            SELECT id, check_type, ok, message, measured_at, details_json
            FROM health_check_results
            WHERE id = ?
            """,
            (result_id,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Health result missing after insert")
        return HealthCheckResult(
            id=int(row["id"]),
            check_type=str(row["check_type"]),
            ok=bool(row["ok"]),
            message=str(row["message"]),
            measured_at=_dt(str(row["measured_at"])) or datetime.now(),
            details_json=str(row["details_json"]),
        )


class MigrationRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_status(self) -> MigrationStatus:
        latest = self.conn.execute(
            "SELECT version, applied_at FROM schema_migrations ORDER BY version DESC LIMIT 1"
        ).fetchone()
        count = self.conn.execute("SELECT COUNT(*) AS count FROM schema_migrations").fetchone()
        expected = {
            "schema_migrations",
            "users",
            "role_bindings",
            "governance_policy",
            "review_cases",
            "audit_events",
            "health_check_results",
        }
        actual = fetch_table_names(self.conn)
        missing = sorted(expected - actual)
        return MigrationStatus(
            current_version="none" if latest is None else str(latest["version"]),
            migration_count=int(count["count"]) if count is not None else 0,
            latest_applied_at=None if latest is None else _dt(str(latest["applied_at"])),
            schema_ok=not missing,
            expected_table_count=len(expected),
            actual_table_count=len(actual),
            missing_items=missing,
        )
