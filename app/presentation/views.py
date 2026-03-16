from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from app.presentation.view_models import AuditTableModel, CaseTableModel


def _section_title(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setStyleSheet("font-size: 20px; font-weight: 700;")
    return label


class DashboardView(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addWidget(_section_title("Dashboard"))

        self.hero_label = QtWidgets.QLabel()
        self.hero_label.setWordWrap(True)
        self.hero_label.setStyleSheet("font-size: 15px; color: #243b53;")
        layout.addWidget(self.hero_label)

        self.cards_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.cards_layout)
        self.cards: dict[str, QtWidgets.QLabel] = {}
        for key, title in [
            ("open_cases", "Open Cases"),
            ("open_findings", "Open Findings"),
            ("overdue_measures", "Overdue Measures"),
            ("accepted_risks", "Accepted Risks"),
            ("closed_cases", "Closed"),
        ]:
            frame = QtWidgets.QFrame()
            frame.setObjectName("metricCard")
            frame.setStyleSheet(
                "#metricCard {background: white; border: 1px solid #d9e2ec; border-radius: 12px; padding: 12px;}"
            )
            card_layout = QtWidgets.QVBoxLayout(frame)
            heading = QtWidgets.QLabel(title)
            heading.setStyleSheet("color: #486581; font-size: 12px; text-transform: uppercase;")
            value = QtWidgets.QLabel("0")
            value.setStyleSheet("font-size: 28px; font-weight: 700; color: #102a43;")
            card_layout.addWidget(heading)
            card_layout.addWidget(value)
            self.cards_layout.addWidget(frame)
            self.cards[key] = value

        self.policy_label = QtWidgets.QLabel()
        self.policy_label.setWordWrap(True)
        layout.addWidget(self.policy_label)

        self.blocked_label = QtWidgets.QLabel()
        self.blocked_label.setWordWrap(True)
        layout.addWidget(self.blocked_label)

        self.health_label = QtWidgets.QLabel()
        self.health_label.setWordWrap(True)
        layout.addWidget(self.health_label)

        self.recent_audit_list = QtWidgets.QListWidget()
        self.recent_audit_list.setMaximumHeight(180)
        layout.addWidget(QtWidgets.QLabel("Recent audit highlights"))
        layout.addWidget(self.recent_audit_list, 1)

    def refresh(self, snapshot: dict[str, object]) -> None:
        user = snapshot["current_user"]
        roles = ", ".join(snapshot["current_roles"]) or "No roles"
        self.hero_label.setText(
            f"Active demo user: <b>{user.display_name}</b> | Roles: <b>{roles}</b>. "
            "This desktop tool highlights controlled processing, role responsibility, auditability, and runtime health."
        )
        for key, label in self.cards.items():
            label.setText(str(snapshot[key]))
        policy = snapshot["policy"]
        review_cases_enabled = policy.feature_flags.get("review_cases", True)
        self.policy_label.setText(
            f"Governance mode: read_only=<b>{'on' if policy.read_only_enabled else 'off'}</b>, "
            f"review_cases=<b>{'enabled' if review_cases_enabled else 'disabled'}</b>."
        )
        self.blocked_label.setText(
            f"Recent blocked actions: <b>{snapshot['recent_blocked_count']}</b>. "
            f"Open findings: <b>{snapshot['open_findings']}</b>, overdue measures: <b>{snapshot['overdue_measures']}</b>."
        )
        latest_health = snapshot["latest_health"]
        if latest_health is None:
            self.health_label.setText("Health: no snapshot recorded yet.")
        else:
            tone = "healthy" if latest_health.ok else "attention needed"
            self.health_label.setText(
                f"Latest health snapshot: <b>{tone}</b> at {latest_health.measured_at.strftime('%Y-%m-%d %H:%M')}."
            )
        self.recent_audit_list.clear()
        for audit in snapshot["recent_audits"]:
            self.recent_audit_list.addItem(
                f"{audit.occurred_at.strftime('%H:%M')} | {audit.domain}.{audit.action} | entity={audit.entity_type}:{audit.entity_id or '-'}"
            )


class ReviewCasesView(QtWidgets.QWidget):
    case_selected = QtCore.Signal(int)
    action_requested = QtCore.Signal(str, int)

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(16)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(_section_title("Review Cases"))
        self.banner = QtWidgets.QLabel()
        self.banner.setWordWrap(True)
        left.addWidget(self.banner)

        self.case_model = CaseTableModel()
        self.case_table = QtWidgets.QTableView()
        self.case_table.setModel(self.case_model)
        self.case_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.case_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.case_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.case_table.verticalHeader().setVisible(False)
        self.case_table.setAlternatingRowColors(True)
        self.case_table.clicked.connect(self._handle_clicked)
        left.addWidget(self.case_table, 1)

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        layout.addWidget(left_widget, 2)

        detail_frame = QtWidgets.QFrame()
        detail_frame.setStyleSheet("QFrame {background: white; border: 1px solid #d9e2ec; border-radius: 12px;}")
        detail_layout = QtWidgets.QVBoxLayout(detail_frame)
        detail_layout.addWidget(_section_title("Case Detail"))
        self.detail_title = QtWidgets.QLabel("Select a case")
        self.detail_title.setStyleSheet("font-size: 18px; font-weight: 700;")
        self.detail_summary = QtWidgets.QLabel("")
        self.detail_summary.setWordWrap(True)
        self.detail_meta = QtWidgets.QLabel("")
        self.detail_meta.setWordWrap(True)
        detail_layout.addWidget(self.detail_title)
        detail_layout.addWidget(self.detail_summary)
        detail_layout.addWidget(self.detail_meta)

        self.feedback_label = QtWidgets.QLabel("")
        self.feedback_label.setWordWrap(True)
        detail_layout.addWidget(self.feedback_label)

        self.rule_hint_label = QtWidgets.QLabel("")
        self.rule_hint_label.setWordWrap(True)
        self.rule_hint_label.setStyleSheet("color: #486581;")
        detail_layout.addWidget(self.rule_hint_label)

        actions_layout = QtWidgets.QGridLayout()
        self.claim_button = QtWidgets.QPushButton("Claim")
        self.unclaim_button = QtWidgets.QPushButton("Unclaim")
        self.approve_button = QtWidgets.QPushButton("Approve")
        self.reject_button = QtWidgets.QPushButton("Reject")
        self.close_button = QtWidgets.QPushButton("Close")
        self.assign_owner_button = QtWidgets.QPushButton("Assign To Me")
        self.start_measure_button = QtWidgets.QPushButton("Start Measure")
        self.mitigate_button = QtWidgets.QPushButton("Mark Mitigated")
        self.accept_risk_button = QtWidgets.QPushButton("Accept Risk")
        buttons = [
            self.claim_button,
            self.unclaim_button,
            self.approve_button,
            self.reject_button,
            self.close_button,
            self.assign_owner_button,
            self.start_measure_button,
            self.mitigate_button,
            self.accept_risk_button,
        ]
        for button in buttons:
            button.setEnabled(False)
        actions_layout.addWidget(self.claim_button, 0, 0)
        actions_layout.addWidget(self.unclaim_button, 0, 1)
        actions_layout.addWidget(self.approve_button, 1, 0)
        actions_layout.addWidget(self.reject_button, 1, 1)
        actions_layout.addWidget(self.close_button, 2, 0, 1, 2)
        actions_layout.addWidget(self.assign_owner_button, 3, 0)
        actions_layout.addWidget(self.start_measure_button, 3, 1)
        actions_layout.addWidget(self.mitigate_button, 4, 0)
        actions_layout.addWidget(self.accept_risk_button, 4, 1)
        detail_layout.addLayout(actions_layout)
        detail_layout.addStretch(1)
        layout.addWidget(detail_frame, 1)

        self._current_case_id: int | None = None
        self.claim_button.clicked.connect(lambda: self._emit_action("claim"))
        self.unclaim_button.clicked.connect(lambda: self._emit_action("unclaim"))
        self.approve_button.clicked.connect(lambda: self._emit_action("approved"))
        self.reject_button.clicked.connect(lambda: self._emit_action("rejected"))
        self.close_button.clicked.connect(lambda: self._emit_action("closed"))
        self.assign_owner_button.clicked.connect(lambda: self._emit_action("assign_measure_owner"))
        self.start_measure_button.clicked.connect(lambda: self._emit_action("start_measure"))
        self.mitigate_button.clicked.connect(lambda: self._emit_action("mitigate"))
        self.accept_risk_button.clicked.connect(lambda: self._emit_action("accept_risk"))

    def refresh_case_list(self, rows: list[dict[str, object]], banner_text: str) -> None:
        self.banner.setText(banner_text)
        self.case_model.update_items(rows)
        if not rows:
            self._current_case_id = None
            self.clear_case_detail("No cases are available right now.")
        elif self._current_case_id is None:
            self.select_case(int(rows[0]["id"]))

    def select_case(self, case_id: int) -> None:
        for row in range(self.case_model.rowCount()):
            item = self.case_model.data(self.case_model.index(row, 0), QtCore.Qt.UserRole)
            if item and int(item["id"]) == case_id:
                self.case_table.selectRow(row)
                self._current_case_id = case_id
                self.case_selected.emit(case_id)
                return

    def show_case_detail(self, payload: dict[str, object]) -> None:
        self._current_case_id = int(payload["id"])
        self.detail_title.setText(str(payload["title"]))
        self.detail_summary.setText(str(payload["summary"]))
        self.detail_meta.setText(
            f"Status: <b>{payload['status']}</b><br>"
            f"Item type: <b>{payload['case_kind']}</b><br>"
            f"Risk level: <b>{payload['risk_level']}</b><br>"
            f"Finding status: <b>{payload['finding_status']}</b><br>"
            f"Control status: <b>{payload['control_status']}</b><br>"
            f"Measure: <b>{payload['measure_title']}</b><br>"
            f"Measure status: <b>{payload['measure_status']}</b><br>"
            f"Measure owner: <b>{payload['measure_owner_name']}</b><br>"
            f"Due date: <b>{payload['due_at']}</b><br>"
            f"Priority: <b>{payload['priority']}</b><br>"
            f"Claimed by: <b>{payload['claimed_by_name']}</b><br>"
            f"Decision: <b>{payload['decision']}</b><br>"
            f"Decision reason: <b>{payload['decision_reason']}</b><br>"
            f"Evidence note: <b>{payload['evidence_note']}</b><br>"
            f"Updated: <b>{payload['updated_at']}</b>"
        )
        self.claim_button.setEnabled(bool(payload["allowed_actions"]["claim"]))
        self.unclaim_button.setEnabled(bool(payload["allowed_actions"]["unclaim"]))
        self.approve_button.setEnabled(bool(payload["allowed_actions"]["approved"]))
        self.reject_button.setEnabled(bool(payload["allowed_actions"]["rejected"]))
        self.close_button.setEnabled(bool(payload["allowed_actions"]["closed"]))
        self.assign_owner_button.setEnabled(bool(payload["allowed_actions"]["assign_measure_owner"]))
        self.start_measure_button.setEnabled(bool(payload["allowed_actions"]["start_measure"]))
        self.mitigate_button.setEnabled(bool(payload["allowed_actions"]["mitigate"]))
        self.accept_risk_button.setEnabled(bool(payload["allowed_actions"]["accept_risk"]))
        self.rule_hint_label.setText(str(payload["primary_hint"]))

    def clear_case_detail(self, message: str) -> None:
        self.detail_title.setText("Select a case")
        self.detail_summary.setText(message)
        self.detail_meta.setText("")
        self.rule_hint_label.setText("No case-specific actions are available.")
        for button in (
            self.claim_button,
            self.unclaim_button,
            self.approve_button,
            self.reject_button,
            self.close_button,
            self.assign_owner_button,
            self.start_measure_button,
            self.mitigate_button,
            self.accept_risk_button,
        ):
            button.setEnabled(False)

    def show_feedback(self, message: str, *, ok: bool) -> None:
        color = "#1f7a1f" if ok else "#9b1c1c"
        self.feedback_label.setStyleSheet(f"color: {color}; font-weight: 600;")
        self.feedback_label.setText(message)

    @property
    def current_case_id(self) -> int | None:
        return self._current_case_id

    def _handle_clicked(self, index: QtCore.QModelIndex) -> None:
        item = self.case_model.data(index, QtCore.Qt.UserRole)
        if item:
            self._current_case_id = int(item["id"])
            self.case_selected.emit(self._current_case_id)

    def _emit_action(self, action: str) -> None:
        if self._current_case_id is not None:
            self.action_requested.emit(action, self._current_case_id)


class GovernanceConsoleView(QtWidgets.QWidget):
    save_requested = QtCore.Signal(bool, bool)

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addWidget(_section_title("Governance Console"))
        self.summary_label = QtWidgets.QLabel()
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)

        form = QtWidgets.QFormLayout()
        self.read_only_checkbox = QtWidgets.QCheckBox("Enable read-only mode")
        self.review_cases_checkbox = QtWidgets.QCheckBox("Enable Review Cases workflow")
        form.addRow("Guardrails", self.read_only_checkbox)
        form.addRow("", self.review_cases_checkbox)
        layout.addLayout(form)

        self.role_matrix = QtWidgets.QTableWidget(0, 2)
        self.role_matrix.setHorizontalHeaderLabels(["User", "Roles"])
        self.role_matrix.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.role_matrix.verticalHeader().setVisible(False)
        self.role_matrix.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        layout.addWidget(QtWidgets.QLabel("Current role bindings"))
        layout.addWidget(self.role_matrix, 1)

        self.feedback_label = QtWidgets.QLabel("")
        self.feedback_label.setWordWrap(True)
        layout.addWidget(self.feedback_label)

        self.save_button = QtWidgets.QPushButton("Save governance settings")
        self.save_button.clicked.connect(self._emit_save)
        layout.addWidget(self.save_button)

    def refresh(self, *, active_user: str, active_roles: list[str], policy: dict[str, object], role_rows: list[tuple[str, str]]) -> None:
        roles_text = ", ".join(active_roles) or "No roles"
        self.summary_label.setText(
            f"Signed in as <b>{active_user}</b> with roles <b>{roles_text}</b>. "
            "Only admins can change guardrails."
        )
        self.read_only_checkbox.setChecked(bool(policy["read_only_enabled"]))
        self.review_cases_checkbox.setChecked(bool(policy["review_cases_enabled"]))
        self.role_matrix.setRowCount(len(role_rows))
        for row_index, row in enumerate(role_rows):
            self.role_matrix.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.role_matrix.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[1]))

    def show_feedback(self, message: str, *, ok: bool) -> None:
        color = "#1f7a1f" if ok else "#9b1c1c"
        self.feedback_label.setStyleSheet(f"color: {color}; font-weight: 600;")
        self.feedback_label.setText(message)

    def _emit_save(self) -> None:
        self.save_requested.emit(self.read_only_checkbox.isChecked(), self.review_cases_checkbox.isChecked())


class AuditView(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(_section_title("Audit & Evidence"))
        self.summary_label = QtWidgets.QLabel("Recent high-value events are stored locally for traceability.")
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)
        self.audit_model = AuditTableModel()
        self.audit_table = QtWidgets.QTableView()
        self.audit_table.setModel(self.audit_model)
        self.audit_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.audit_table.verticalHeader().setVisible(False)
        self.audit_table.setAlternatingRowColors(True)
        self.audit_table.clicked.connect(self._handle_clicked)
        layout.addWidget(self.audit_table, 1)

        self.detail_label = QtWidgets.QLabel("Select an audit event to inspect its payload.")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("background: white; border: 1px solid #d9e2ec; border-radius: 12px; padding: 12px;")
        layout.addWidget(self.detail_label)

    def refresh(self, rows: list[dict[str, object]]) -> None:
        self.audit_model.update_items(rows)
        self.detail_label.setText(
            "Select an audit event to inspect its payload." if rows else "No audit events have been recorded yet."
        )

    def _handle_clicked(self, index: QtCore.QModelIndex) -> None:
        item = self.audit_model.data(index, QtCore.Qt.UserRole)
        if item:
            self.detail_label.setText(
                f"Severity: <b>{item['severity']}</b><br>"
                f"Actor: <b>{item['actor_name']}</b><br>"
                f"Action: <b>{item['action']}</b><br>"
                f"Entity: <b>{item['entity_label']}</b><br>"
                f"Payload:<br><pre>{item['payload_pretty']}</pre>"
            )


class HealthStatusView(QtWidgets.QWidget):
    run_requested = QtCore.Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addWidget(_section_title("Health & Change Status"))

        self.summary_label = QtWidgets.QLabel()
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)

        self.migration_label = QtWidgets.QLabel()
        self.migration_label.setWordWrap(True)
        layout.addWidget(self.migration_label)

        self.history_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Recent health snapshots"))
        layout.addWidget(self.history_list, 1)

        self.detail_label = QtWidgets.QLabel()
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("background: white; border: 1px solid #d9e2ec; border-radius: 12px; padding: 12px;")
        layout.addWidget(self.detail_label)

        self.run_button = QtWidgets.QPushButton("Run health check")
        self.run_button.clicked.connect(self.run_requested.emit)
        layout.addWidget(self.run_button)

    def refresh(self, *, migration_text: str, summary_text: str, rows: list[str], details_text: str) -> None:
        self.summary_label.setText(summary_text)
        self.migration_label.setText(migration_text)
        self.history_list.clear()
        self.history_list.addItems(rows or ["No health snapshots recorded yet."])
        self.detail_label.setText(details_text)
