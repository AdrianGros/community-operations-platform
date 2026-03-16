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
        "Dashboard",
        "Review Cases",
        "Governance Console",
        "Audit & Evidence",
        "Health & Change Status",
    )

    for index, title in enumerate(expected_titles):
        _select_nav(window, index)
        assert window.stack.currentIndex() == index
        assert window.nav_list.item(index).text() != ""
        current_widget = window.stack.currentWidget()
        assert current_widget.isVisible()
        labels = current_widget.findChildren(QtWidgets.QLabel)
        assert any(title in label.text() for label in labels)


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
    assert "Risk level" in review_view.detail_meta.text()


def test_governance_read_only_toggle_blocks_review_actions_in_ui(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_nav(window, 2)
    governance_view = window.governance_view
    governance_view.read_only_checkbox.setChecked(True)
    qtbot.mouseClick(governance_view.save_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()

    assert "saved" in governance_view.feedback_label.text().lower()
    assert "Read-only: on" in window.policy_badge.text()

    _select_nav(window, 1)
    _select_case(window, 6)
    assert not window.review_cases_view.claim_button.isEnabled()
    assert "read-only" in window.review_cases_view.rule_hint_label.text().lower()


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
    assert "Severity:" in window.audit_view.detail_label.text()


def test_end_to_end_demo_flow_is_functional_from_ui(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_user_by_name(window, "Mina Patel")
    _select_nav(window, 1)
    _select_case(window, 6)

    qtbot.mouseClick(window.review_cases_view.claim_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "claimed" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.approve_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "approved" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.assign_owner_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "owner assigned" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.start_measure_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "in progress" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.mitigate_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "mitigated" in window.review_cases_view.feedback_label.text().lower()

    qtbot.mouseClick(window.review_cases_view.close_button, QtCore.Qt.LeftButton)
    QtWidgets.QApplication.processEvents()
    assert "closed" in window.review_cases_view.feedback_label.text().lower()
    assert "Closed / Closed" in window.review_cases_view.detail_status_pill.text()


def test_auditor_user_can_reach_review_module_but_not_mutate(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    _select_user_by_name(window, "Jonas Becker")
    _select_nav(window, 1)
    _select_case(window, 6)

    assert "AUDITOR" in window.role_badge.text()
    assert not window.review_cases_view.claim_button.isEnabled()
    assert "cannot change review cases" in window.review_cases_view.rule_hint_label.text().lower()
