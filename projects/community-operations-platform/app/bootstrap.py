from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from app.application.services import AuditService, CaseService, DashboardService, GovernanceService, HealthService, SessionService
from app.infrastructure.database import apply_migrations, connect, ensure_runtime_dirs, seed_demo_data
from app.infrastructure.logging_config import configure_logging
from app.infrastructure.repositories import (
    AuditRepository,
    GovernanceRepository,
    HealthRepository,
    MigrationRepository,
    ReviewCaseRepository,
    RoleBindingRepository,
    UserRepository,
)
from app.state import AppContext, Repositories, RuntimeState, Services, SessionState

log = logging.getLogger(__name__)


class BootstrapError(RuntimeError):
    pass


def create_app_context(base_dir: Path | None = None) -> tuple[AppContext, sqlite3.Connection]:
    project_root = Path(__file__).resolve().parent.parent if base_dir is None else base_dir
    db_path, log_path = ensure_runtime_dirs(project_root)
    configure_logging(log_path)
    log.info("Bootstrapping application context", extra={"db_path": str(db_path)})
    try:
        conn = connect(db_path)
        apply_migrations(conn)
        seed_demo_data(conn)
    except Exception as exc:
        log.exception("Bootstrap failed", extra={"db_path": str(db_path)})
        raise BootstrapError(f"Bootstrap failed for database {db_path}") from exc

    repos = Repositories(
        user_repo=UserRepository(conn),
        role_binding_repo=RoleBindingRepository(conn),
        governance_repo=GovernanceRepository(conn),
        review_case_repo=ReviewCaseRepository(conn),
        audit_repo=AuditRepository(conn),
        health_repo=HealthRepository(conn),
        migration_repo=MigrationRepository(conn),
    )
    session = SessionState(current_user_id=1)
    session_service = SessionService(repos.user_repo, repos.role_binding_repo, session)
    audit_service = AuditService(repos.audit_repo)
    governance_service = GovernanceService(repos.governance_repo, audit_service, session_service)
    case_service = CaseService(repos.review_case_repo, governance_service, session_service, audit_service)
    health_service = HealthService(
        repos.health_repo,
        repos.migration_repo,
        repos.governance_repo,
        repos.user_repo,
        repos.review_case_repo,
        audit_service,
    )
    dashboard_service = DashboardService(case_service, governance_service, audit_service, health_service, session_service)
    services = Services(
        dashboard_service=dashboard_service,
        session_service=session_service,
        case_service=case_service,
        governance_service=governance_service,
        audit_service=audit_service,
        health_service=health_service,
    )
    context = AppContext(
        repos=repos,
        services=services,
        session=session,
        runtime=RuntimeState(data_dir=db_path.parent, db_path=db_path, log_path=log_path),
    )
    log.info("Application context ready", extra={"db_path": str(db_path)})
    return context, conn
