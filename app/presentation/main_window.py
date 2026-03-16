from __future__ import annotations

import json
import logging

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QSettings

from app.state import AppContext
from app.presentation.views import (
    AuditView,
    DashboardView,
    GovernanceConsoleView,
    HealthStatusView,
    ReviewCasesView,
)

log = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_context: AppContext) -> None:
        super().__init__()
        self.app_context = app_context
        self.settings = QSettings("CommunityOperationsPlatform", "GovernanceShowcase")
        self.setWindowTitle("Governance Showcase App")
        self.resize(1320, 820)
        self.setMinimumSize(1120, 720)
        self.setStyleSheet(
            """
            QMainWindow, QWidget { background: #f4f7fb; color: #102a43; }
            QListWidget { background: white; border: 1px solid #d9e2ec; border-radius: 12px; padding: 8px; }
            QListWidget::item { padding: 10px 12px; border-radius: 8px; }
            QListWidget::item:selected { background: #d9eaf7; color: #102a43; }
            QTableView { background: white; border: 1px solid #d9e2ec; border-radius: 12px; gridline-color: #d9e2ec; }
            QPushButton { background: #0f6cbd; color: white; border: none; border-radius: 8px; padding: 10px 14px; font-weight: 600; }
            QPushButton:disabled { background: #9fb3c8; color: #f0f4f8; }
            QComboBox, QCheckBox, QLabel, QListWidget, QTableWidget { font-size: 13px; }
            """
        )

        central = QtWidgets.QWidget()
        root_layout = QtWidgets.QVBoxLayout(central)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(16)

        header = QtWidgets.QFrame()
        header.setStyleSheet("QFrame { background: #102a43; border-radius: 18px; } QLabel { color: white; }")
        header_layout = QtWidgets.QHBoxLayout(header)
        title_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Governance Showcase App")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        subtitle = QtWidgets.QLabel(
            "Controlled processing, auditability, governance guardrails, and runtime health in one local desktop tool."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #d9e2ec; font-size: 13px;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout, 1)

        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(QtWidgets.QLabel("Active user"))
        self.user_combo = QtWidgets.QComboBox()
        self.user_combo.currentIndexChanged.connect(self._handle_user_change)
        controls_layout.addWidget(self.user_combo)
        self.role_badge = QtWidgets.QLabel()
        self.policy_badge = QtWidgets.QLabel()
        controls_layout.addWidget(self.role_badge)
        controls_layout.addWidget(self.policy_badge)
        header_layout.addLayout(controls_layout)
        root_layout.addWidget(header)

        body_layout = QtWidgets.QHBoxLayout()
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.addItems(
            [
                "Dashboard / Home",
                "Review Cases",
                "Governance Console",
                "Audit & Evidence",
                "Health & Change Status",
            ]
        )
        self.nav_list.currentRowChanged.connect(self._handle_nav_change)
        self.nav_list.setFixedWidth(240)
        body_layout.addWidget(self.nav_list)

        self.stack = QtWidgets.QStackedWidget()
        self.dashboard_view = DashboardView()
        self.review_cases_view = ReviewCasesView()
        self.governance_view = GovernanceConsoleView()
        self.audit_view = AuditView()
        self.health_view = HealthStatusView()
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.review_cases_view)
        self.stack.addWidget(self.governance_view)
        self.stack.addWidget(self.audit_view)
        self.stack.addWidget(self.health_view)
        body_layout.addWidget(self.stack, 1)
        root_layout.addLayout(body_layout, 1)
        self.setCentralWidget(central)

        self.review_cases_view.case_selected.connect(self._load_case_detail)
        self.review_cases_view.action_requested.connect(self._perform_case_action)
        self.governance_view.save_requested.connect(self._save_governance_policy)
        self.health_view.run_requested.connect(self._run_health_check)

        self._populate_user_combo()
        self.nav_list.setCurrentRow(0)
        self._restore_window_state()
        self.refresh_all()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

    def refresh_all(self) -> None:
        selected_case_id = self.review_cases_view.current_case_id
        self._refresh_header()
        self._refresh_dashboard()
        self._refresh_cases(selected_case_id=selected_case_id)
        self._refresh_governance()
        self._refresh_audit()
        self._refresh_health()

    def _populate_user_combo(self) -> None:
        self.user_combo.blockSignals(True)
        self.user_combo.clear()
        users = self.app_context.services.session_service.list_users()
        for user in users:
            self.user_combo.addItem(user.display_name, user.id)
        current_id = self.app_context.session.current_user_id
        current_index = max(0, self.user_combo.findData(current_id))
        self.user_combo.setCurrentIndex(current_index)
        self.user_combo.blockSignals(False)

    def _refresh_header(self) -> None:
        current_user = self.app_context.services.session_service.get_current_user()
        roles = ", ".join(self.app_context.services.session_service.get_current_roles()) or "No roles"
        policy = self.app_context.services.governance_service.get_policy()
        self.role_badge.setText(f"Roles: {roles}")
        self.role_badge.setStyleSheet("background: #d9eaf7; color: #102a43; padding: 8px 12px; border-radius: 999px;")
        review_enabled = policy.feature_flags.get("review_cases", True)
        self.policy_badge.setText(
            f"Read-only: {'on' if policy.read_only_enabled else 'off'} | Review Cases: {'on' if review_enabled else 'off'}"
        )
        badge_color = "#f0b429" if policy.read_only_enabled else "#2f855a"
        self.policy_badge.setStyleSheet(
            f"background: {badge_color}; color: white; padding: 8px 12px; border-radius: 999px;"
        )
        self.setWindowTitle(f"Governance Showcase App - {current_user.display_name}")

    def _refresh_dashboard(self) -> None:
        snapshot = self.app_context.services.dashboard_service.get_snapshot()
        self.dashboard_view.refresh(snapshot)

    def _refresh_cases(self, *, selected_case_id: int | None = None) -> None:
        cases = self.app_context.services.case_service.list_cases()
        users = {user.id: user.display_name for user in self.app_context.services.session_service.list_users()}
        policy = self.app_context.services.governance_service.get_policy()
        rows = [
            {
                "id": case.id,
                "title": case.title,
                "risk_level": case.risk_level,
                "finding_status": case.finding_status.replace("_", " ").title(),
                "measure_status": case.measure_status.replace("_", " ").title(),
                "measure_owner_name": users.get(case.measure_owner, "Unassigned") if case.measure_owner is not None else "Unassigned",
                "updated_at": case.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
            for case in cases
        ]
        banner = (
            "Use this queue to review findings, track mitigation work, and close controlled items. "
            f"Read-only is {'enabled' if policy.read_only_enabled else 'disabled'}, "
            f"Review Cases are {'enabled' if policy.feature_flags.get('review_cases', True) else 'disabled'}."
        )
        self.review_cases_view.refresh_case_list(rows, banner)
        if not cases:
            self.review_cases_view.clear_case_detail("No cases are available in the local store yet.")
            return
        selected_case = selected_case_id or self.review_cases_view.current_case_id or cases[0].id
        if self.app_context.services.case_service.get_case(selected_case) is None:
            selected_case = cases[0].id
        self.review_cases_view.select_case(selected_case)

    def _refresh_governance(self) -> None:
        active_user = self.app_context.services.session_service.get_current_user()
        policy = self.app_context.services.governance_service.get_policy()
        bindings = self.app_context.repos.role_binding_repo.list_bindings()
        users = {user.id: user.display_name for user in self.app_context.services.session_service.list_users()}
        grouped: dict[int, list[str]] = {}
        for binding in bindings:
            grouped.setdefault(binding.user_id, []).append(binding.role_code)
        rows = [(users[user_id], ", ".join(sorted(codes))) for user_id, codes in sorted(grouped.items())]
        self.governance_view.refresh(
            active_user=active_user.display_name,
            active_roles=self.app_context.services.session_service.get_current_roles(),
            policy={
                "read_only_enabled": policy.read_only_enabled,
                "review_cases_enabled": policy.feature_flags.get("review_cases", True),
            },
            role_rows=rows,
        )

    def _refresh_audit(self) -> None:
        events = self.app_context.services.audit_service.list_events(limit=200)
        users = {user.id: user.display_name for user in self.app_context.services.session_service.list_users()}
        rows = [
            {
                "occurred_at": event.occurred_at.strftime("%Y-%m-%d %H:%M"),
                "severity": event.severity.upper(),
                "actor_name": users.get(event.actor_user_id, "System") if event.actor_user_id is not None else "System",
                "action": f"{event.domain}.{event.action}",
                "entity_label": f"{event.entity_type}:{event.entity_id or '-'}",
                "payload_pretty": self._format_json_payload(event.payload_json),
            }
            for event in events
        ]
        self.audit_view.refresh(rows)

    def _refresh_health(self) -> None:
        migration = self.app_context.services.health_service.get_migration_status()
        rows = self.app_context.services.health_service.list_results(limit=10)
        summary = rows[0].message if rows else "No health checks recorded yet."
        migration_text = (
            f"Schema version: <b>{migration.current_version}</b> | "
            f"Migrations: <b>{migration.migration_count}</b> | "
            f"Tables: <b>{migration.actual_table_count}/{migration.expected_table_count}</b> | "
            f"Schema OK: <b>{'yes' if migration.schema_ok else 'no'}</b>"
        )
        if migration.missing_items:
            migration_text += f"<br>Missing items: <b>{', '.join(migration.missing_items)}</b>"
        history = [
            f"{row.measured_at.strftime('%Y-%m-%d %H:%M')} | {'OK' if row.ok else 'WARN'} | {row.message}"
            for row in rows
        ]
        detail_lines: list[str] = []
        if rows:
            latest_details = self._parse_json_payload(rows[0].details_json, fallback={"checks": []})
            for check in latest_details.get("checks", []):
                detail_lines.append(
                    f"{'OK' if check.get('ok') else 'WARN'} | {check.get('name')} | {check.get('detail')}"
                )
        details_text = "<br>".join(detail_lines) if detail_lines else "No detailed checks recorded yet."
        self.health_view.refresh(
            migration_text=migration_text,
            summary_text=summary,
            rows=history,
            details_text=details_text,
        )

    def _load_case_detail(self, case_id: int) -> None:
        case = self.app_context.services.case_service.get_case(case_id)
        if case is None:
            return
        users = {user.id: user.display_name for user in self.app_context.services.session_service.list_users()}
        payload = {
            "id": case.id,
            "title": case.title,
            "summary": case.summary,
            "status": case.status.title(),
            "case_kind": case.case_kind.replace("_", " ").title(),
            "risk_level": case.risk_level,
            "finding_status": case.finding_status.replace("_", " ").title(),
            "control_status": case.control_status.replace("_", " ").title(),
            "measure_title": case.measure_title,
            "measure_status": case.measure_status.replace("_", " ").title(),
            "measure_owner_name": users.get(case.measure_owner, "Unassigned") if case.measure_owner is not None else "Unassigned",
            "due_at": case.due_at.strftime("%Y-%m-%d") if case.due_at is not None else "-",
            "evidence_note": case.evidence_note or "-",
            "priority": case.priority,
            "claimed_by_name": users.get(case.claimed_by, "Unclaimed") if case.claimed_by is not None else "Unclaimed",
            "decision": case.decision or "-",
            "decision_reason": case.decision_reason or "-",
            "updated_at": case.updated_at.strftime("%Y-%m-%d %H:%M"),
        }
        action_state = self.app_context.services.case_service.get_case_action_state(case.id)
        payload["allowed_actions"] = action_state.allowed_actions
        payload["primary_hint"] = action_state.primary_hint
        self.review_cases_view.show_case_detail(payload)

    def _perform_case_action(self, action: str, case_id: int) -> None:
        try:
            if action == "claim":
                result = self.app_context.services.case_service.claim_case(case_id)
            elif action == "unclaim":
                result = self.app_context.services.case_service.unclaim_case(case_id)
            elif action == "assign_measure_owner":
                result = self.app_context.services.case_service.assign_measure_owner_to_current_user(case_id)
            elif action == "start_measure":
                result = self.app_context.services.case_service.start_measure(case_id)
            elif action in {"mitigate", "accept_risk"}:
                result = self.app_context.services.case_service.progress_finding(case_id, action)
            else:
                result = self.app_context.services.case_service.decide_case(case_id, action)
        except Exception:
            log.exception("Case action failed action=%s case_id=%s", action, case_id)
            self.review_cases_view.show_feedback("The action failed. See log for details.", ok=False)
            self.statusBar().showMessage("Case action failed. See log for details.", 5000)
            return
        self.review_cases_view.show_feedback(result.message, ok=result.ok)
        self.refresh_all()
        selected_case_id = result.case.id if result.case is not None else case_id
        if self.app_context.services.case_service.get_case(selected_case_id) is not None:
            self.review_cases_view.select_case(selected_case_id)
        self.statusBar().showMessage(result.message, 4000)

    def _save_governance_policy(self, read_only_enabled: bool, review_cases_enabled: bool) -> None:
        try:
            ok, message, _policy = self.app_context.services.governance_service.update_policy(
                read_only_enabled=read_only_enabled,
                review_cases_enabled=review_cases_enabled,
            )
        except Exception:
            log.exception("Governance save failed")
            self.governance_view.show_feedback("Governance update failed. See log for details.", ok=False)
            self.statusBar().showMessage("Governance update failed. See log for details.", 5000)
            return
        self.governance_view.show_feedback(message, ok=ok)
        self.refresh_all()

    def _run_health_check(self) -> None:
        try:
            result = self.app_context.services.health_service.run_health_check()
        except Exception:
            log.exception("Health check failed")
            self.statusBar().showMessage("Health check failed. See log for details.", 5000)
            return
        self.statusBar().showMessage(f"Health check recorded: {'OK' if result.ok else 'WARN'}", 4000)
        self.refresh_all()

    def _handle_nav_change(self, index: int) -> None:
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def _handle_user_change(self, index: int) -> None:
        user_id = self.user_combo.itemData(index)
        if user_id is None:
            return
        self.app_context.services.session_service.switch_user(int(user_id))
        self.refresh_all()

    def _restore_window_state(self) -> None:
        geometry = self.settings.value("geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        state = self.settings.value("windowState")
        if state is not None:
            self.restoreState(state)

    @staticmethod
    def _parse_json_payload(raw_payload: str, *, fallback: dict[str, object]) -> dict[str, object]:
        try:
            parsed = json.loads(raw_payload)
        except (TypeError, json.JSONDecodeError):
            log.warning("Could not decode JSON payload for UI detail view")
            return fallback
        return parsed if isinstance(parsed, dict) else fallback

    def _format_json_payload(self, raw_payload: str) -> str:
        payload = self._parse_json_payload(raw_payload, fallback={"raw_payload": raw_payload})
        return json.dumps(payload, indent=2, sort_keys=True)
