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
    HEADER_COMBO_WIDTH = 180
    HEADER_ROLE_BADGE_WIDTH = 160
    HEADER_POLICY_BADGE_WIDTH = 250
    HEADER_ROLE_TEXT_MAX = 20
    HEADER_POLICY_TEXT_MAX = 30
    DISPLAY_MAPS = {
        "risk_level": {"High": "Hoch", "Medium": "Mittel", "Low": "Niedrig"},
        "case_status": {
            "Open": "Offen",
            "Claimed": "Uebernommen",
            "Approved": "Freigegeben",
            "Rejected": "Abgelehnt",
            "Closed": "Geschlossen",
        },
        "finding_status": {
            "Identified": "Identifiziert",
            "In Progress": "In Bearbeitung",
            "Mitigated": "Mitigiert",
            "Accepted": "Akzeptiert",
            "Closed": "Geschlossen",
        },
        "measure_status": {
            "Planned": "Geplant",
            "In Progress": "In Bearbeitung",
            "Completed": "Abgeschlossen",
            "Accepted": "Akzeptiert",
        },
        "control_status": {
            "Needs Attention": "Aufmerksamkeit noetig",
            "Partially Effective": "Teilweise wirksam",
            "Monitored": "Unter Beobachtung",
            "Effective": "Wirksam",
        },
        "case_kind": {
            "Finding": "Abweichung",
            "Risk": "Risiko",
            "Control Review": "Kontrollpruefung",
        },
    }

    def __init__(self, app_context: AppContext) -> None:
        super().__init__()
        self.app_context = app_context
        self.settings = QSettings("CommunityOperationsPlatform", "GovernanceShowcase")
        self.setWindowTitle("Governance-Demo-App")
        self.resize(1320, 820)
        self.setMinimumSize(1120, 720)
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #edf2f7;
                color: #16324f;
                font-size: 13px;
            }
            QFrame#shellHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #18324d, stop:1 #214e73);
                border-radius: 24px;
            }
            QLabel#appTitle {
                color: white;
                font-size: 28px;
                font-weight: 700;
            }
            QLabel#appSubtitle {
                color: #d8e5f2;
                font-size: 13px;
            }
            QLabel#sectionTitle {
                color: #14324b;
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#sectionCaption {
                color: #5b7288;
                font-size: 13px;
            }
            QFrame#card, QFrame#metricCard {
                background: #ffffff;
                border: 1px solid #d7e2ec;
                border-radius: 18px;
            }
            QLabel#heroText {
                color: #274863;
                font-size: 14px;
                line-height: 1.4;
            }
            QLabel#metricHeading {
                color: #6b7f92;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }
            QLabel#metricValue {
                color: #14324b;
                font-size: 30px;
                font-weight: 700;
            }
            QLabel#inlineInfo, QLabel#calloutInfo, QLabel#calloutMuted, QLabel#detailPanel,
            QLabel#feedbackNeutral, QLabel#feedbackSuccess, QLabel#feedbackError {
                border-radius: 14px;
                padding: 12px 14px;
            }
            QLabel#inlineInfo {
                background: #ffffff;
                border: 1px solid #d7e2ec;
                color: #274863;
            }
            QLabel#calloutInfo {
                background: #eef6fd;
                border: 1px solid #c9ddf0;
                color: #274863;
            }
            QLabel#calloutMuted {
                background: #f8fafc;
                border: 1px solid #dbe6ef;
                color: #5d7185;
            }
            QLabel#detailPanel {
                background: #f8fbfd;
                border: 1px solid #d7e2ec;
                color: #274863;
            }
            QLabel#feedbackNeutral {
                background: #f8fafc;
                border: 1px solid #dbe6ef;
                color: #5d7185;
            }
            QLabel#feedbackSuccess {
                background: #edf9f1;
                border: 1px solid #b8e0c2;
                color: #25683c;
                font-weight: 600;
            }
            QLabel#feedbackError {
                background: #fff1f1;
                border: 1px solid #f1c4c4;
                color: #9a3030;
                font-weight: 600;
            }
            QLabel#detailTitle {
                color: #14324b;
                font-size: 22px;
                font-weight: 700;
            }
            QLabel#detailSummary {
                color: #2f4e68;
                background: #f7fafc;
                border: 1px solid #dbe6ef;
                border-radius: 14px;
                padding: 12px 14px;
            }
            QLabel#detailMeta {
                color: #274863;
                background: #ffffff;
                border: 1px solid #d7e2ec;
                border-radius: 14px;
                padding: 14px;
            }
            QLabel#pill {
                background: #e7f0fb;
                color: #1a4e7a;
                border: 1px solid #c9ddf0;
                border-radius: 999px;
                padding: 6px 12px;
                font-weight: 700;
            }
            QLabel#pill[tone="claimed"], QLabel#pill[tone="approved"], QLabel#pill[tone="mitigated"] {
                background: #e7f4ed;
                color: #25683c;
                border: 1px solid #b7dbbf;
            }
            QLabel#pill[tone="rejected"] {
                background: #fff1f1;
                color: #9a3030;
                border: 1px solid #f1c4c4;
            }
            QLabel#pill[tone="closed"] {
                background: #eef2f6;
                color: #5d7185;
                border: 1px solid #d7e2ec;
            }
            QLabel#pill[tone="open"], QLabel#pill[tone="in progress"] {
                background: #eef6fd;
                color: #1f5f99;
                border: 1px solid #c9ddf0;
            }
            QLabel#pill[tone="risk-high"] {
                background: #fff1f1;
                color: #9a3030;
                border: 1px solid #f1c4c4;
            }
            QLabel#pill[tone="risk-medium"] {
                background: #fff7e8;
                color: #9a5a00;
                border: 1px solid #edd8a8;
            }
            QLabel#pill[tone="risk-low"] {
                background: #edf9f1;
                color: #25683c;
                border: 1px solid #b8e0c2;
            }
            QListWidget {
                background: #ffffff;
                border: 1px solid #d7e2ec;
                border-radius: 18px;
                padding: 12px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 14px;
                border-radius: 12px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background: #dbe9f6;
                color: #14324b;
                font-weight: 600;
            }
            QTableView, QTableWidget {
                background: #ffffff;
                border: none;
                border-radius: 14px;
                gridline-color: #e6edf3;
                selection-background-color: #e2eef9;
                selection-color: #14324b;
                alternate-background-color: #f8fbfd;
            }
            QHeaderView::section {
                background: transparent;
                color: #617587;
                border: none;
                border-bottom: 1px solid #dbe6ef;
                padding: 10px 8px;
                font-weight: 700;
            }
            QComboBox {
                background: #ffffff;
                border: 1px solid #d7e2ec;
                border-radius: 10px;
                padding: 8px 10px;
                min-width: 160px;
                color: #16324f;
                font-weight: 600;
                selection-color: #16324f;
                selection-background-color: #ffffff;
            }
            QComboBox:hover {
                border: 1px solid #9db7cf;
                background: #f9fbfd;
            }
            QComboBox:focus {
                border: 2px solid #1f6fb2;
                padding: 7px 9px;
                background: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 28px;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                color: #16324f;
                border: 1px solid #cfdbe6;
                selection-background-color: #1f6fb2;
                selection-color: #ffffff;
                outline: 0;
                padding: 6px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 28px;
                padding: 6px 10px;
                border-radius: 8px;
                color: #16324f;
                background: transparent;
            }
            QComboBox QAbstractItemView::item:selected {
                background: #1f6fb2;
                color: #ffffff;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #e8f1f8;
                color: #16324f;
            }
            QComboBox:on {
                color: #16324f;
                background: #ffffff;
            }
            QCheckBox {
                spacing: 8px;
                color: #274863;
            }
            QCheckBox:disabled {
                color: #8ea1b3;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: 600;
                background: #286ea8;
                color: white;
            }
            QPushButton[buttonRole="primary"] {
                background: #1f6fb2;
                color: white;
            }
            QPushButton[buttonRole="secondary"] {
                background: #dfeaf4;
                color: #16324f;
            }
            QPushButton[buttonRole="warning"] {
                background: #f0b347;
                color: #4c3200;
            }
            QPushButton[buttonRole="danger"] {
                background: #c94f4f;
                color: white;
            }
            QPushButton:hover {
                background: #155e98;
            }
            QPushButton[buttonRole="secondary"]:hover {
                background: #cfdeeb;
            }
            QPushButton[buttonRole="warning"]:hover {
                background: #e0a53d;
            }
            QPushButton[buttonRole="danger"]:hover {
                background: #b84343;
            }
            QPushButton:disabled {
                background: #b8c8d8;
                color: #eef4f8;
            }
            QPushButton:focus {
                border: 2px solid #14324b;
                padding: 8px 12px;
            }
            QTableView::item {
                padding: 6px 8px;
            }
            QTableView::item:selected {
                background: #dcecf9;
                color: #14324b;
            }
            QTableView::item:hover {
                background: #f1f7fc;
            }
            QTableWidget::item:selected {
                background: #dcecf9;
                color: #14324b;
            }
            QListWidget::item:hover {
                background: #eef4fa;
                color: #14324b;
            }
            """
        )

        central = QtWidgets.QWidget()
        root_layout = QtWidgets.QVBoxLayout(central)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(16)

        header = QtWidgets.QFrame()
        header.setObjectName("shellHeader")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(18, 16, 18, 16)
        header_layout.setSpacing(18)
        title_layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Governance-Demo-App")
        title.setObjectName("appTitle")
        subtitle = QtWidgets.QLabel(
            "Kontrollierte Bearbeitung, klare Verantwortlichkeit, Massnahmenverfolgung und Laufzeitstatus in einem lokalen Desktop-Werkzeug."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("appSubtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout, 1)

        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setSpacing(10)
        controls_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        active_user_label = QtWidgets.QLabel("Aktiver Nutzer")
        active_user_label.setStyleSheet("color: white; font-weight: 500;")
        controls_layout.addWidget(active_user_label)
        self.user_combo = QtWidgets.QComboBox()
        self.user_combo.setFixedWidth(self.HEADER_COMBO_WIDTH)
        self.user_combo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.user_combo.currentIndexChanged.connect(self._handle_user_change)
        controls_layout.addWidget(self.user_combo)
        self.role_badge = QtWidgets.QLabel()
        self.role_badge.setFixedWidth(self.HEADER_ROLE_BADGE_WIDTH)
        self.role_badge.setWordWrap(False)
        self.role_badge.setAlignment(QtCore.Qt.AlignCenter)
        self.policy_badge = QtWidgets.QLabel()
        self.policy_badge.setFixedWidth(self.HEADER_POLICY_BADGE_WIDTH)
        self.policy_badge.setWordWrap(False)
        self.policy_badge.setAlignment(QtCore.Qt.AlignCenter)
        controls_layout.addWidget(self.role_badge)
        controls_layout.addWidget(self.policy_badge)
        header_layout.addLayout(controls_layout)
        root_layout.addWidget(header)

        body_layout = QtWidgets.QHBoxLayout()
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.addItems(
            [
                "Uebersicht",
                "Prueffaelle",
                "Governance-Konsole",
                "Audit & Nachweise",
                "Health & Aenderungsstatus",
            ]
        )
        self.nav_list.currentRowChanged.connect(self._handle_nav_change)
        self.nav_list.setFixedWidth(250)
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
        if self.user_combo.currentText():
            self.user_combo.setToolTip(self.user_combo.currentText())
        self.user_combo.blockSignals(False)

    def _refresh_header(self) -> None:
        current_user = self.app_context.services.session_service.get_current_user()
        roles = ", ".join(self.app_context.services.session_service.get_current_roles()) or "Keine Rollen"
        policy = self.app_context.services.governance_service.get_policy()
        self._set_compact_label(
            self.role_badge,
            prefix="Rollen:",
            value=roles,
            max_length=self.HEADER_ROLE_TEXT_MAX,
        )
        review_enabled = policy.feature_flags.get("review_cases", True)
        policy_full = f"Nur Lesen: {'an' if policy.read_only_enabled else 'aus'} | Prueffaelle: {'an' if review_enabled else 'aus'}"
        self._set_compact_label(
            self.policy_badge,
            prefix="",
            value=policy_full,
            max_length=self.HEADER_POLICY_TEXT_MAX,
        )
        self.policy_badge.setStyleSheet(
            "background: #f0b347; color: #4c3200; border: 1px solid #e0c27a; border-radius: 999px; padding: 8px 12px; font-weight: 700;"
            if policy.read_only_enabled
            else "background: #dff2e5; color: #25683c; border: 1px solid #b7dbbf; border-radius: 999px; padding: 8px 12px; font-weight: 700;"
        )
        self.setWindowTitle(f"Governance-Demo-App - {current_user.display_name}")

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
                "risk_level": self._display_label("risk_level", case.risk_level),
                "finding_status": self._display_label("finding_status", case.finding_status.replace("_", " ").title()),
                "measure_status": self._display_label("measure_status", case.measure_status.replace("_", " ").title()),
                "measure_owner_name": users.get(case.measure_owner, "Nicht zugewiesen") if case.measure_owner is not None else "Nicht zugewiesen",
                "updated_at": case.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
            for case in cases
        ]
        banner = (
            "Nutze diese Liste, um Abweichungen zu pruefen, Massnahmen nachzuverfolgen und kontrolliert zu schliessen. "
            f"Nur-Lesen ist {'aktiv' if policy.read_only_enabled else 'inaktiv'}, "
            f"Prueffaelle sind {'aktiv' if policy.feature_flags.get('review_cases', True) else 'inaktiv'}."
        )
        self.review_cases_view.refresh_case_list(rows, banner)
        if not cases:
            self.review_cases_view.clear_case_detail("Im lokalen Datenbestand sind derzeit keine Faelle vorhanden.")
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
        summary = rows[0].message if rows else "Noch keine Health-Pruefungen vorhanden."
        migration_text = (
            f"Schema version: <b>{migration.current_version}</b> | "
            f"Migrationen: <b>{migration.migration_count}</b> | "
            f"Tabellen: <b>{migration.actual_table_count}/{migration.expected_table_count}</b> | "
            f"Schema OK: <b>{'ja' if migration.schema_ok else 'nein'}</b>"
        )
        if migration.missing_items:
            migration_text += f"<br>Fehlende Elemente: <b>{', '.join(migration.missing_items)}</b>"
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
        details_text = "<br>".join(detail_lines) if detail_lines else "Noch keine detaillierten Pruefergebnisse vorhanden."
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
            "status": self._display_label("case_status", case.status.title()),
            "status_tone": case.status,
            "case_kind": self._display_label("case_kind", case.case_kind.replace("_", " ").title()),
            "risk_level": self._display_label("risk_level", case.risk_level),
            "risk_tone": case.risk_level,
            "finding_status": self._display_label("finding_status", case.finding_status.replace("_", " ").title()),
            "control_status": self._display_label("control_status", case.control_status.replace("_", " ").title()),
            "measure_title": case.measure_title,
            "measure_status": self._display_label("measure_status", case.measure_status.replace("_", " ").title()),
            "measure_owner_name": users.get(case.measure_owner, "Nicht zugewiesen") if case.measure_owner is not None else "Nicht zugewiesen",
            "due_at": case.due_at.strftime("%Y-%m-%d") if case.due_at is not None else "-",
            "evidence_note": case.evidence_note or "-",
            "priority": case.priority,
            "claimed_by_name": users.get(case.claimed_by, "Nicht uebernommen") if case.claimed_by is not None else "Nicht uebernommen",
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
            self.review_cases_view.show_feedback("Die Aktion ist fehlgeschlagen. Details stehen im Log.", ok=False)
            self.statusBar().showMessage("Aktion fehlgeschlagen. Details stehen im Log.", 5000)
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
            self.governance_view.show_feedback("Governance-Aenderung fehlgeschlagen. Details stehen im Log.", ok=False)
            self.statusBar().showMessage("Governance-Aenderung fehlgeschlagen. Details stehen im Log.", 5000)
            return
        self.governance_view.show_feedback(message, ok=ok)
        self.refresh_all()

    def _run_health_check(self) -> None:
        try:
            result = self.app_context.services.health_service.run_health_check()
        except Exception:
            log.exception("Health check failed")
            self.statusBar().showMessage("Health-Pruefung fehlgeschlagen. Details stehen im Log.", 5000)
            return
        self.statusBar().showMessage(f"Health-Pruefung gespeichert: {'OK' if result.ok else 'WARN'}", 4000)
        self.refresh_all()

    def _handle_nav_change(self, index: int) -> None:
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def _handle_user_change(self, index: int) -> None:
        user_id = self.user_combo.itemData(index)
        if user_id is None:
            return
        self.user_combo.setToolTip(self.user_combo.currentText())
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
    def _truncate_text(value: str, max_length: int) -> str:
        normalized = value.strip()
        if len(normalized) <= max_length:
            return normalized
        return f"{normalized[: max_length - 3].rstrip()}..."

    def _set_compact_label(self, label: QtWidgets.QLabel, *, prefix: str, value: str, max_length: int) -> None:
        visible_value = self._truncate_text(value, max_length)
        label_text = f"{prefix} {visible_value}".strip()
        tooltip_text = f"{prefix} {value}".strip()
        label.setText(label_text)
        label.setToolTip(tooltip_text)
        label.setObjectName("pill")

    @classmethod
    def _display_label(cls, mapping_name: str, value: str) -> str:
        return cls.DISPLAY_MAPS.get(mapping_name, {}).get(value, value)

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
