from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from app.presentation.main_window import MainWindow


def _select_nav(window: MainWindow, index: int) -> None:
    window.nav_list.setCurrentRow(index)
    QtWidgets.QApplication.processEvents()


def _select_user_by_name(window: MainWindow, name: str) -> None:
    index = window.user_combo.findText(name)
    if index < 0:
        raise AssertionError(f"User {name} not found in combo box")
    window.user_combo.setCurrentIndex(index)
    QtWidgets.QApplication.processEvents()


def _select_case(window: MainWindow, case_id: int) -> None:
    window.review_cases_view.select_case(case_id)
    QtWidgets.QApplication.processEvents()


def test_all_core_modules_are_visible_and_reachable(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    expected_titles = (
        "Uebersicht",
        "Prueffaelle",
        "Governance-Konsole",
        "Audit & Nachweise",
        "Systemzustand & Aenderungsstatus",
    )

    for index, title in enumerate(expected_titles):
        _select_nav(window, index)
        assert window.stack.currentIndex() == index
        assert window.nav_list.item(index).text() != ""
        current_widget = window.stack.currentWidget()
        assert current_widget.isVisible()
        labels = current_widget.findChildren(QtWidgets.QLabel)
        assert any(title in label.text() for label in labels)


def test_active_user_dropdown_is_reachable_and_switchable(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    combo = window.user_combo
    assert combo.isVisible()
    assert combo.count() >= 3
    initial_width = combo.width()
    initial_role_x = window.role_badge.x()

    combo.showPopup()
    QtWidgets.QApplication.processEvents()
    assert combo.view().isVisible()

    _select_user_by_name(window, "Mina Patel")
    assert "Mina Patel" in window.windowTitle()
    assert combo.width() == initial_width
    assert window.role_badge.x() == initial_role_x
    assert combo.toolTip() == "Mina Patel"


def test_header_badges_use_stable_text_constraints_and_tooltips(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    window.role_badge.setText("")
    window.role_badge.setToolTip("")
    long_roles = "ADMIN, REVIEWER, AUDITOR, GOVERNANCE-OWNER"
    truncated = window._truncate_text(long_roles, 20)

    assert len(truncated) <= 20
    assert truncated.endswith("...")

    window.refresh_all()
    assert window.role_badge.toolTip().startswith("Rollen:")
    assert len(window.role_badge.text()) <= len("Rollen: ") + 20
    assert window.policy_badge.toolTip().startswith("Nur Lesen:")


def test_header_compact_elements_keep_fixed_width_across_all_demo_roles(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    combo_width = window.user_combo.width()
    role_width = window.role_badge.width()
    policy_width = window.policy_badge.width()

    positions: list[tuple[int, int]] = []
    for user_name in ("Avery Stone", "Mina Patel", "Jonas Becker"):
        _select_user_by_name(window, user_name)
        positions.append((window.role_badge.x(), window.policy_badge.x()))
        assert window.user_combo.width() == combo_width
        assert window.role_badge.width() == role_width
        assert window.policy_badge.width() == policy_width

    assert len(set(positions)) == 1


def test_review_case_actions_are_visible_and_stateful(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_nav(window, 1)
    _select_case(window, 6)

    review_view = window.review_cases_view
    for button in (
        review_view.claim_button,
        review_view.unclaim_button,
        review_view.approve_button,
        review_view.reject_button,
        review_view.close_button,
        review_view.assign_owner_button,
        review_view.start_measure_button,
        review_view.mitigate_button,
        review_view.accept_risk_button,
    ):
        assert button.isVisible()

    assert review_view.claim_button.isEnabled()
    assert not review_view.close_button.isEnabled()
    assert "Risikostufe" in review_view.detail_meta.text()


def test_governance_read_only_toggle_blocks_review_actions_in_ui(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_nav(window, 2)
    governance_view = window.governance_view
    governance_view.read_only_checkbox.setChecked(True)
    qtbot.mouseClick(governance_view.save_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()

    assert "gespeichert" in governance_view.feedback_label.text().lower()
    assert "Nur Lesen: an" in window.policy_badge.text()

    _select_nav(window, 1)
    _select_case(window, 6)
    assert not window.review_cases_view.claim_button.isEnabled()
    assert "nur-lesen" in window.review_cases_view.rule_hint_label.text().lower()


def test_audit_and_health_views_update_interactively(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_nav(window, 4)
    before_count = window.health_view.history_list.count()
    qtbot.mouseClick(window.health_view.run_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert window.health_view.history_list.count() >= before_count
    assert window.health_view.detail_label.text() != ""

    _select_nav(window, 3)
    assert window.audit_view.audit_model.rowCount() >= 1
    index = window.audit_view.audit_model.index(0, 0)
    window.audit_view._handle_clicked(index)
    assert "Schweregrad:" in window.audit_view.detail_label.text()


def test_end_to_end_demo_flow_is_functional_from_ui(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_user_by_name(window, "Mina Patel")
    _select_nav(window, 1)
    _select_case(window, 6)

    qtbot.mouseClick(window.review_cases_view.claim_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "uebernommen" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.approve_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "freigegeben" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.assign_owner_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "massnahmenverantwortung" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.start_measure_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "in bearbeitung" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.mitigate_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "mitigiert" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.close_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "geschlossen" in window.review_cases_view.feedback_label.text().lower()
    assert "Geschlossen / Geschlossen" in window.review_cases_view.detail_status_pill.text()


def test_auditor_user_can_reach_review_module_but_not_mutate(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_user_by_name(window, "Jonas Becker")
    _select_nav(window, 1)
    _select_case(window, 6)

    assert "AUDITOR" in window.role_badge.text()
    assert not window.review_cases_view.claim_button.isEnabled()
    assert "darf prueffaelle nicht veraendern" in window.review_cases_view.rule_hint_label.text().lower()
