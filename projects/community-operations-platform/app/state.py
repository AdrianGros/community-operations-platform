from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Repositories:
    user_repo: Any
    role_binding_repo: Any
    governance_repo: Any
    review_case_repo: Any
    audit_repo: Any
    health_repo: Any
    migration_repo: Any


@dataclass(slots=True)
class Services:
    dashboard_service: Any
    session_service: Any
    case_service: Any
    governance_service: Any
    audit_service: object
    health_service: object


@dataclass(slots=True)
class SessionState:
    current_user_id: int


@dataclass(slots=True)
class RuntimeState:
    data_dir: Path
    db_path: Path
    log_path: Path


@dataclass(slots=True)
class AppContext:
    repos: Repositories
    services: Services
    session: SessionState
    runtime: RuntimeState
