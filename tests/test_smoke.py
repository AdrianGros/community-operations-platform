from __future__ import annotations

from app.presentation.main_window import MainWindow


def test_main_window_smoke(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    assert window.nav_list.count() == 5
    assert window.user_combo.count() >= 3
    assert window.review_cases_view.case_model.rowCount() >= 1
    assert window.review_cases_view.rule_hint_label.text() != ""
    assert window.review_cases_view.detail_meta.text() != ""
    assert window.health_view.detail_label.text() != ""
    assert "Governance Showcase App" in window.windowTitle()


def test_main_window_refresh_keeps_case_detail_stable_after_action(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    window.review_cases_view.select_case(1)
    before_title = window.review_cases_view.detail_title.text()
    window._perform_case_action("claim", 1)

    assert window.review_cases_view.current_case_id == 1
    assert window.review_cases_view.detail_title.text() == before_title
    assert "Case claimed." in window.review_cases_view.feedback_label.text()


def test_main_window_shows_isms_context_in_case_detail(qtbot, app_context) -> None:
    window = MainWindow(app_context)
    qtbot.addWidget(window)
    window.show()

    window.review_cases_view.select_case(2)

    detail = window.review_cases_view.detail_meta.text()
    assert "Risk level" in detail
    assert "Finding status" in detail
    assert "Measure status" in detail
    assert "Measure owner" in detail
