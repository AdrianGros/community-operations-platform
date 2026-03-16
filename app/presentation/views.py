from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from app.presentation.view_models import AuditTableModel, CaseTableModel


def _section_title(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName("sectionTitle")
    return label


def _section_caption(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName("sectionCaption")
    label.setWordWrap(True)
    return label


def _card() -> QtWidgets.QFrame:
    frame = QtWidgets.QFrame()
    frame.setObjectName("card")
    return frame


def _pill_label() -> QtWidgets.QLabel:
    label = QtWidgets.QLabel()
    label.setObjectName("pill")
    label.setAlignment(QtCore.Qt.AlignCenter)
    return label


class DashboardView(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(18)
        layout.addWidget(_section_title("Uebersicht"))
        layout.addWidget(_section_caption("Kompakter Ueberblick ueber Arbeitslast, Governance-Zustand und Laufzeitstatus."))

        hero_card = _card()
        hero_layout = QtWidgets.QVBoxLayout(hero_card)
        hero_layout.setContentsMargins(18, 18, 18, 18)
        hero_layout.setSpacing(10)
        self.hero_label = QtWidgets.QLabel()
        self.hero_label.setWordWrap(True)
        self.hero_label.setObjectName("heroText")
        hero_layout.addWidget(self.hero_label)
        layout.addWidget(hero_card)

        self.cards_layout = QtWidgets.QHBoxLayout()
        self.cards_layout.setSpacing(14)
        layout.addLayout(self.cards_layout)
        self.cards: dict[str, QtWidgets.QLabel] = {}
        for key, title in [
            ("open_cases", "Offene Faelle"),
            ("open_findings", "Offene Abweichungen"),
            ("overdue_measures", "Ueberfaellige Massnahmen"),
            ("accepted_risks", "Akzeptierte Restrisiken"),
            ("closed_cases", "Geschlossen"),
        ]:
            frame = _card()
            frame.setObjectName("metricCard")
            card_layout = QtWidgets.QVBoxLayout(frame)
            card_layout.setContentsMargins(16, 16, 16, 16)
            heading = QtWidgets.QLabel(title)
            heading.setObjectName("metricHeading")
            value = QtWidgets.QLabel("0")
            value.setObjectName("metricValue")
            card_layout.addWidget(heading)
            card_layout.addWidget(value)
            self.cards_layout.addWidget(frame)
            self.cards[key] = value

        status_row = QtWidgets.QHBoxLayout()
        status_row.setSpacing(14)
        self.policy_label = QtWidgets.QLabel()
        self.policy_label.setWordWrap(True)
        self.policy_label.setObjectName("inlineInfo")
        self.blocked_label = QtWidgets.QLabel()
        self.blocked_label.setWordWrap(True)
        self.blocked_label.setObjectName("inlineInfo")
        self.health_label = QtWidgets.QLabel()
        self.health_label.setWordWrap(True)
        self.health_label.setObjectName("inlineInfo")
        status_row.addWidget(self.policy_label, 1)
        status_row.addWidget(self.blocked_label, 1)
        status_row.addWidget(self.health_label, 1)
        layout.addLayout(status_row)

        audit_card = _card()
        audit_layout = QtWidgets.QVBoxLayout(audit_card)
        audit_layout.setContentsMargins(16, 16, 16, 16)
        audit_layout.addWidget(_section_caption("Letzte Audit-Ereignisse"))
        self.recent_audit_list = QtWidgets.QListWidget()
        self.recent_audit_list.setMaximumHeight(180)
        audit_layout.addWidget(self.recent_audit_list, 1)
        layout.addWidget(audit_card, 1)

    def refresh(self, snapshot: dict[str, object]) -> None:
        user = snapshot["current_user"]
        roles = ", ".join(snapshot["current_roles"]) or "Keine Rollen"
        self.hero_label.setText(
            f"Aktiver Demo-Nutzer: <b>{user.display_name}</b> | Rollen: <b>{roles}</b>. "
            "Dieses Desktop-Werkzeug zeigt kontrollierte Bearbeitung, klare Verantwortlichkeit, Auditierbarkeit und Laufzeitstatus."
        )
        for key, label in self.cards.items():
            label.setText(str(snapshot[key]))
        policy = snapshot["policy"]
        review_cases_enabled = policy.feature_flags.get("review_cases", True)
        self.policy_label.setText(
            f"Governance-Modus: nur_lesen=<b>{'an' if policy.read_only_enabled else 'aus'}</b>, "
            f"prueffaelle=<b>{'aktiv' if review_cases_enabled else 'inaktiv'}</b>."
        )
        self.blocked_label.setText(
            f"Zuletzt blockierte Aktionen: <b>{snapshot['recent_blocked_count']}</b>. "
            f"Offene Abweichungen: <b>{snapshot['open_findings']}</b>, ueberfaellige Massnahmen: <b>{snapshot['overdue_measures']}</b>."
        )
        latest_health = snapshot["latest_health"]
        if latest_health is None:
            self.health_label.setText("Health: Noch kein Snapshot vorhanden.")
        else:
            tone = "stabil" if latest_health.ok else "Aufmerksamkeit noetig"
            self.health_label.setText(
                f"Letzter Health-Snapshot: <b>{tone}</b> um {latest_health.measured_at.strftime('%Y-%m-%d %H:%M')}."
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
        layout.setSpacing(18)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(_section_title("Prueffaelle"))
        left.addWidget(_section_caption("Bearbeite Abweichungen, verfolge Massnahmen und schliesse Faelle kontrolliert ab."))
        self.banner = QtWidgets.QLabel()
        self.banner.setWordWrap(True)
        self.banner.setObjectName("calloutInfo")
        left.addWidget(self.banner)

        self.case_model = CaseTableModel()
        table_card = _card()
        table_layout = QtWidgets.QVBoxLayout(table_card)
        table_layout.setContentsMargins(10, 10, 10, 10)
        self.case_table = QtWidgets.QTableView()
        self.case_table.setModel(self.case_model)
        self.case_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.case_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.case_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.case_table.verticalHeader().setVisible(False)
        self.case_table.setAlternatingRowColors(True)
        self.case_table.setShowGrid(False)
        self.case_table.setSortingEnabled(False)
        self.case_table.clicked.connect(self._handle_clicked)
        table_layout.addWidget(self.case_table, 1)
        left.addWidget(table_card, 1)

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        layout.addWidget(left_widget, 2)

        detail_frame = _card()
        detail_layout = QtWidgets.QVBoxLayout(detail_frame)
        detail_layout.setContentsMargins(16, 16, 16, 16)
        detail_layout.setSpacing(12)
        detail_layout.addWidget(_section_title("Falldetail"))
        detail_layout.addWidget(_section_caption("Der ausgewaehlte Fall ist in Status, Verantwortlichkeit und Nachweiskontext gegliedert."))
        self.detail_title = QtWidgets.QLabel("Fall auswaehlen")
        self.detail_title.setObjectName("detailTitle")
        self.detail_status_pill = _pill_label()
        self.detail_risk_pill = _pill_label()
        self.detail_status_pill.hide()
        self.detail_risk_pill.hide()
        self.detail_summary = QtWidgets.QLabel("")
        self.detail_summary.setWordWrap(True)
        self.detail_summary.setObjectName("detailSummary")
        self.detail_meta = QtWidgets.QLabel("")
        self.detail_meta.setWordWrap(True)
        self.detail_meta.setObjectName("detailMeta")
        detail_layout.addWidget(self.detail_title)
        pill_row = QtWidgets.QHBoxLayout()
        pill_row.setSpacing(8)
        pill_row.addWidget(self.detail_status_pill, 0, QtCore.Qt.AlignLeft)
        pill_row.addWidget(self.detail_risk_pill, 0, QtCore.Qt.AlignLeft)
        pill_row.addStretch(1)
        detail_layout.addLayout(pill_row)
        detail_layout.addWidget(self.detail_summary)
        detail_layout.addWidget(self.detail_meta)

        self.feedback_label = QtWidgets.QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setObjectName("feedbackNeutral")
        detail_layout.addWidget(self.feedback_label)

        self.rule_hint_label = QtWidgets.QLabel("")
        self.rule_hint_label.setWordWrap(True)
        self.rule_hint_label.setObjectName("calloutMuted")
        detail_layout.addWidget(self.rule_hint_label)

        actions_layout = QtWidgets.QGridLayout()
        actions_layout.setHorizontalSpacing(10)
        actions_layout.setVerticalSpacing(10)
        self.claim_button = QtWidgets.QPushButton("Uebernehmen")
        self.unclaim_button = QtWidgets.QPushButton("Freigeben")
        self.approve_button = QtWidgets.QPushButton("Freigeben")
        self.reject_button = QtWidgets.QPushButton("Ablehnen")
        self.close_button = QtWidgets.QPushButton("Schliessen")
        self.assign_owner_button = QtWidgets.QPushButton("Mir zuweisen")
        self.start_measure_button = QtWidgets.QPushButton("Massnahme starten")
        self.mitigate_button = QtWidgets.QPushButton("Als mitigiert markieren")
        self.accept_risk_button = QtWidgets.QPushButton("Restrisiko akzeptieren")
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
            button.setMinimumHeight(38)
        self.claim_button.setProperty("buttonRole", "secondary")
        self.unclaim_button.setProperty("buttonRole", "primary")
        self.approve_button.setProperty("buttonRole", "primary")
        self.reject_button.setProperty("buttonRole", "danger")
        self.close_button.setProperty("buttonRole", "secondary")
        self.assign_owner_button.setProperty("buttonRole", "secondary")
        self.start_measure_button.setProperty("buttonRole", "primary")
        self.mitigate_button.setProperty("buttonRole", "primary")
        self.accept_risk_button.setProperty("buttonRole", "warning")
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
            self.clear_case_detail("Derzeit sind keine Faelle verfuegbar.")
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
        status_text = f"{payload['status']} / {payload['finding_status']}"
        self.detail_status_pill.setText(status_text)
        self.detail_status_pill.setProperty("tone", str(payload["status_tone"]).lower())
        self.detail_status_pill.show()
        self.detail_status_pill.style().unpolish(self.detail_status_pill)
        self.detail_status_pill.style().polish(self.detail_status_pill)
        self.detail_risk_pill.setText(f"Risiko {payload['risk_level']}")
        self.detail_risk_pill.setProperty("tone", f"risk-{str(payload['risk_tone']).lower()}")
        self.detail_risk_pill.show()
        self.detail_risk_pill.style().unpolish(self.detail_risk_pill)
        self.detail_risk_pill.style().polish(self.detail_risk_pill)
        self.detail_meta.setText(
            f"<b>Governance-Kontext</b><br>"
            f"Elementtyp: <b>{payload['case_kind']}</b> &nbsp;&nbsp; Risikostufe: <b>{payload['risk_level']}</b> &nbsp;&nbsp; Prioritaet: <b>{payload['priority']}</b><br>"
            f"Abweichungsstatus: <b>{payload['finding_status']}</b> &nbsp;&nbsp; Kontrollstatus: <b>{payload['control_status']}</b><br><br>"
            f"<b>Verantwortlichkeit und Massnahme</b><br>"
            f"Massnahme: <b>{payload['measure_title']}</b><br>"
            f"Massnahmenstatus: <b>{payload['measure_status']}</b> &nbsp;&nbsp; Owner: <b>{payload['measure_owner_name']}</b> &nbsp;&nbsp; Faellig am: <b>{payload['due_at']}</b><br>"
            f"Uebernommen von: <b>{payload['claimed_by_name']}</b><br><br>"
            f"<b>Entscheidung und Nachweis</b><br>"
            f"Entscheidung: <b>{payload['decision']}</b><br>"
            f"Begruendung: <b>{payload['decision_reason']}</b><br>"
            f"Nachweishinweis: <b>{payload['evidence_note']}</b><br>"
            f"Aktualisiert: <b>{payload['updated_at']}</b>"
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
        self.detail_title.setText("Fall auswaehlen")
        self.detail_status_pill.hide()
        self.detail_risk_pill.hide()
        self.detail_summary.setText(message)
        self.detail_meta.setText("")
        self.rule_hint_label.setText("Derzeit sind keine fallspezifischen Aktionen verfuegbar.")
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
        self.feedback_label.setObjectName("feedbackSuccess" if ok else "feedbackError")
        self.feedback_label.style().unpolish(self.feedback_label)
        self.feedback_label.style().polish(self.feedback_label)
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
        layout.addWidget(_section_title("Governance-Konsole"))
        layout.addWidget(_section_caption("Steuere globale Guardrails und pruefe, welche Nutzer aktuell welche Rollen tragen."))
        self.summary_label = QtWidgets.QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setObjectName("calloutInfo")
        layout.addWidget(self.summary_label)

        controls_card = _card()
        controls_layout = QtWidgets.QVBoxLayout(controls_card)
        controls_layout.setContentsMargins(16, 16, 16, 16)
        form = QtWidgets.QFormLayout()
        self.read_only_checkbox = QtWidgets.QCheckBox("Nur-Lesen-Modus aktivieren")
        self.review_cases_checkbox = QtWidgets.QCheckBox("Workflow fuer Prueffaelle aktivieren")
        form.addRow("Guardrails", self.read_only_checkbox)
        form.addRow("", self.review_cases_checkbox)
        controls_layout.addLayout(form)
        layout.addWidget(controls_card)

        role_card = _card()
        role_layout = QtWidgets.QVBoxLayout(role_card)
        role_layout.setContentsMargins(16, 16, 16, 16)
        self.role_matrix = QtWidgets.QTableWidget(0, 2)
        self.role_matrix.setHorizontalHeaderLabels(["Nutzer", "Rollen"])
        self.role_matrix.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.role_matrix.verticalHeader().setVisible(False)
        self.role_matrix.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        role_layout.addWidget(_section_caption("Aktuelle Rollenzuordnungen"))
        role_layout.addWidget(self.role_matrix, 1)
        layout.addWidget(role_card, 1)

        self.feedback_label = QtWidgets.QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setObjectName("feedbackNeutral")
        layout.addWidget(self.feedback_label)

        self.save_button = QtWidgets.QPushButton("Governance-Einstellungen speichern")
        self.save_button.setProperty("buttonRole", "primary")
        self.save_button.clicked.connect(self._emit_save)
        layout.addWidget(self.save_button)

    def refresh(self, *, active_user: str, active_roles: list[str], policy: dict[str, object], role_rows: list[tuple[str, str]]) -> None:
        roles_text = ", ".join(active_roles) or "Keine Rollen"
        self.summary_label.setText(
            f"Angemeldet als <b>{active_user}</b> mit Rollen <b>{roles_text}</b>. "
            "Nur Admins duerfen Guardrails aendern."
        )
        self.read_only_checkbox.setChecked(bool(policy["read_only_enabled"]))
        self.review_cases_checkbox.setChecked(bool(policy["review_cases_enabled"]))
        self.role_matrix.setRowCount(len(role_rows))
        for row_index, row in enumerate(role_rows):
            self.role_matrix.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.role_matrix.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[1]))

    def show_feedback(self, message: str, *, ok: bool) -> None:
        self.feedback_label.setObjectName("feedbackSuccess" if ok else "feedbackError")
        self.feedback_label.style().unpolish(self.feedback_label)
        self.feedback_label.style().polish(self.feedback_label)
        self.feedback_label.setText(message)

    def _emit_save(self) -> None:
        self.save_requested.emit(self.read_only_checkbox.isChecked(), self.review_cases_checkbox.isChecked())


class AuditView(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addWidget(_section_title("Audit & Nachweise"))
        self.summary_label = QtWidgets.QLabel("Wichtige Ereignisse werden lokal fuer Nachvollziehbarkeit gespeichert.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setObjectName("calloutInfo")
        layout.addWidget(self.summary_label)

        table_card = _card()
        table_layout = QtWidgets.QVBoxLayout(table_card)
        table_layout.setContentsMargins(10, 10, 10, 10)
        self.audit_model = AuditTableModel()
        self.audit_table = QtWidgets.QTableView()
        self.audit_table.setModel(self.audit_model)
        self.audit_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.audit_table.verticalHeader().setVisible(False)
        self.audit_table.setAlternatingRowColors(True)
        self.audit_table.setShowGrid(False)
        self.audit_table.clicked.connect(self._handle_clicked)
        table_layout.addWidget(self.audit_table, 1)
        layout.addWidget(table_card, 1)

        self.detail_label = QtWidgets.QLabel("Waehle ein Audit-Ereignis aus, um seine Details zu sehen.")
        self.detail_label.setWordWrap(True)
        self.detail_label.setObjectName("detailPanel")
        layout.addWidget(self.detail_label)

    def refresh(self, rows: list[dict[str, object]]) -> None:
        self.audit_model.update_items(rows)
        self.detail_label.setText(
            "Waehle ein Audit-Ereignis aus, um seine Details zu sehen." if rows else "Es wurden noch keine Audit-Ereignisse erfasst."
        )

    def _handle_clicked(self, index: QtCore.QModelIndex) -> None:
        item = self.audit_model.data(index, QtCore.Qt.UserRole)
        if item:
            self.detail_label.setText(
                f"Schweregrad: <b>{item['severity']}</b><br>"
                f"Akteur: <b>{item['actor_name']}</b><br>"
                f"Aktion: <b>{item['action']}</b><br>"
                f"Objekt: <b>{item['entity_label']}</b><br>"
                f"Payload:<br><pre>{item['payload_pretty']}</pre>"
            )


class HealthStatusView(QtWidgets.QWidget):
    run_requested = QtCore.Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addWidget(_section_title("Systemzustand & Aenderungsstatus"))
        layout.addWidget(_section_caption("Behalte Migrationsstand, Laufzeitpruefungen und lokale Betriebssignale im Blick."))

        self.summary_label = QtWidgets.QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setObjectName("calloutInfo")
        layout.addWidget(self.summary_label)

        self.migration_label = QtWidgets.QLabel()
        self.migration_label.setWordWrap(True)
        self.migration_label.setObjectName("detailPanel")
        layout.addWidget(self.migration_label)

        history_card = _card()
        history_layout = QtWidgets.QVBoxLayout(history_card)
        history_layout.setContentsMargins(16, 16, 16, 16)
        self.history_list = QtWidgets.QListWidget()
        history_layout.addWidget(_section_caption("Letzte Health-Snapshots"))
        history_layout.addWidget(self.history_list, 1)
        layout.addWidget(history_card, 1)

        self.detail_label = QtWidgets.QLabel()
        self.detail_label.setWordWrap(True)
        self.detail_label.setObjectName("detailPanel")
        layout.addWidget(self.detail_label)

        self.run_button = QtWidgets.QPushButton("Health-Pruefung starten")
        self.run_button.setProperty("buttonRole", "primary")
        self.run_button.clicked.connect(self.run_requested.emit)
        layout.addWidget(self.run_button)

    def refresh(self, *, migration_text: str, summary_text: str, rows: list[str], details_text: str) -> None:
        self.summary_label.setText(summary_text)
        self.migration_label.setText(migration_text)
        self.history_list.clear()
        self.history_list.addItems(rows or ["Es sind noch keine Health-Snapshots vorhanden."])
        self.detail_label.setText(details_text)
