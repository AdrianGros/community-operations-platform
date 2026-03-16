from __future__ import annotations

from app.bootstrap import create_app_context
from app.infrastructure.database import MIGRATIONS, apply_migrations, connect, seed_demo_data


def test_seed_data_and_claim_flow(app_context) -> None:
    cases = app_context.services.case_service.list_cases()
    assert len(cases) >= 6

    result = app_context.services.case_service.claim_case(1)
    assert result.ok is True
    assert result.case is not None
    assert result.case.status == "claimed"
    assert result.case.claimed_by == app_context.session.current_user_id

    decision = app_context.services.case_service.decide_case(1, "approved")
    assert decision.ok is True
    assert decision.case is not None
    assert decision.case.status == "approved"

    assign_owner = app_context.services.case_service.assign_measure_owner_to_current_user(1)
    assert assign_owner.ok is True

    start_measure = app_context.services.case_service.start_measure(1)
    assert start_measure.ok is True
    assert start_measure.case is not None
    assert start_measure.case.measure_status == "in_progress"

    mitigate = app_context.services.case_service.progress_finding(1, "mitigate")
    assert mitigate.ok is True
    assert mitigate.case is not None
    assert mitigate.case.finding_status == "mitigated"

    close_result = app_context.services.case_service.decide_case(1, "closed")
    assert close_result.ok is True
    assert close_result.case is not None
    assert close_result.case.status == "closed"


def test_auditor_cannot_claim_cases_and_block_is_audited(app_context) -> None:
    app_context.services.session_service.switch_user(3)
    before = len(app_context.services.audit_service.list_events())
    result = app_context.services.case_service.claim_case(6)
    after = len(app_context.services.audit_service.list_events())
    assert result.ok is False
    assert result.code == "role_insufficient"
    assert after == before + 1


def test_decision_requires_claim_owner_or_admin(app_context) -> None:
    app_context.services.session_service.switch_user(2)
    result = app_context.services.case_service.decide_case(1, "approved")
    assert result.ok is False
    assert result.code == "claim_required"

    claim = app_context.services.case_service.claim_case(1)
    assert claim.ok is True

    app_context.services.session_service.switch_user(1)
    admin_decision = app_context.services.case_service.decide_case(1, "approved")
    assert admin_decision.ok is True


def test_mitigate_requires_measure_owner(app_context) -> None:
    app_context.services.session_service.switch_user(2)
    claim = app_context.services.case_service.claim_case(6)
    assert claim.ok is True

    result = app_context.services.case_service.progress_finding(6, "mitigate")
    assert result.ok is False
    assert result.code == "measure_owner_required"

    owner = app_context.services.case_service.assign_measure_owner_to_current_user(6)
    assert owner.ok is True
    started = app_context.services.case_service.start_measure(6)
    assert started.ok is True
    mitigated = app_context.services.case_service.progress_finding(6, "mitigate")
    assert mitigated.ok is True
    assert mitigated.case is not None
    assert mitigated.case.measure_status == "completed"


def test_accept_risk_requires_admin(app_context) -> None:
    app_context.services.session_service.switch_user(2)
    blocked = app_context.services.case_service.progress_finding(6, "accept_risk")
    assert blocked.ok is False
    assert blocked.code == "admin_required"

    app_context.services.session_service.switch_user(1)
    accepted = app_context.services.case_service.progress_finding(6, "accept_risk")
    assert accepted.ok is True
    assert accepted.case is not None
    assert accepted.case.finding_status == "accepted"


def test_close_requires_mitigated_or_accepted_finding(app_context) -> None:
    app_context.services.session_service.switch_user(2)
    claim = app_context.services.case_service.claim_case(6)
    assert claim.ok is True
    decision = app_context.services.case_service.decide_case(6, "approved")
    assert decision.ok is True

    premature_close = app_context.services.case_service.decide_case(6, "closed")
    assert premature_close.ok is False
    assert premature_close.code == "finding_resolution_required"

    app_context.services.session_service.switch_user(1)
    accepted = app_context.services.case_service.progress_finding(6, "accept_risk")
    assert accepted.ok is True
    close_result = app_context.services.case_service.decide_case(6, "closed")
    assert close_result.ok is True


def test_read_only_blocks_case_updates(app_context) -> None:
    ok, _message, policy = app_context.services.governance_service.update_policy(
        read_only_enabled=True,
        review_cases_enabled=True,
    )
    assert ok is True
    assert policy.read_only_enabled is True

    app_context.services.session_service.switch_user(2)
    result = app_context.services.case_service.claim_case(6)
    assert result.ok is False
    assert "read-only" in result.message
    assert result.code == "read_only"


def test_health_snapshot_records_history(app_context) -> None:
    before = len(app_context.services.health_service.list_results())
    result = app_context.services.health_service.run_health_check()
    after = len(app_context.services.health_service.list_results())
    assert result.ok is True
    assert after == before + 1
    assert '"checks"' in result.details_json


def test_seed_demo_data_is_idempotent(tmp_path) -> None:
    db_path = tmp_path / "seed-idempotent.db"
    conn = connect(db_path)
    try:
        apply_migrations(conn)
        seed_demo_data(conn)
        first_users = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
        first_cases = conn.execute("SELECT COUNT(*) AS count FROM review_cases").fetchone()["count"]
        first_audits = conn.execute("SELECT COUNT(*) AS count FROM audit_events").fetchone()["count"]

        seed_demo_data(conn)

        second_users = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
        second_cases = conn.execute("SELECT COUNT(*) AS count FROM review_cases").fetchone()["count"]
        second_audits = conn.execute("SELECT COUNT(*) AS count FROM audit_events").fetchone()["count"]
        assert (first_users, first_cases, first_audits) == (3, 6, 5)
        assert (second_users, second_cases, second_audits) == (first_users, first_cases, first_audits)
    finally:
        conn.close()


def test_apply_migrations_handles_preexisting_added_columns(tmp_path) -> None:
    db_path = tmp_path / "partial-migration.db"
    conn = connect(db_path)
    try:
        with conn:
            conn.executescript(MIGRATIONS[0].sql)
            conn.execute("ALTER TABLE audit_events ADD COLUMN severity TEXT NOT NULL DEFAULT 'info'")

        apply_migrations(conn)

        versions = [
            row["version"]
            for row in conn.execute("SELECT version FROM schema_migrations ORDER BY version ASC").fetchall()
        ]
        health_columns = {row["name"] for row in conn.execute("PRAGMA table_info(health_check_results)").fetchall()}
        audit_columns = {row["name"] for row in conn.execute("PRAGMA table_info(audit_events)").fetchall()}
        review_case_columns = {row["name"] for row in conn.execute("PRAGMA table_info(review_cases)").fetchall()}
        assert versions == ["001_init", "002_audit_health_enrichment", "003_review_case_governance_context"]
        assert "severity" in audit_columns
        assert "details_json" in health_columns
        assert "finding_status" in review_case_columns
    finally:
        conn.close()


def test_create_app_context_repairs_partial_seed_baseline(tmp_path) -> None:
    context, conn = create_app_context(base_dir=tmp_path)
    conn.close()

    repaired = connect(context.runtime.db_path)
    try:
        with repaired:
            repaired.execute("DELETE FROM role_bindings WHERE user_id = 3 AND role_code = 'AUDITOR'")
            repaired.execute("DELETE FROM governance_policy WHERE id = 1")
            repaired.execute("DELETE FROM review_cases WHERE id = 6")
        repaired.close()

        context2, conn2 = create_app_context(base_dir=tmp_path)
        try:
            roles = context2.repos.role_binding_repo.get_roles_for_user(3)
            policy = context2.services.governance_service.get_policy()
            case = context2.services.case_service.get_case(6)
            assert roles == ["AUDITOR"]
            assert policy.id == 1
            assert case is not None
            assert case.measure_title != ""
        finally:
            conn2.close()
    finally:
        if repaired:
            try:
                repaired.close()
            except Exception:
                pass
