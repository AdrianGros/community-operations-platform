from __future__ import annotations

from dataclasses import dataclass

import asyncpg


@dataclass(slots=True)
class Repositories:
    audit_repo: object
    tenant_config_repo: object
    membership_repo: object
    session_repo: object
    session_reminder_repo: object
    scheduled_message_repo: object


@dataclass(slots=True)
class Services:
    audit_service: object
    tenant_config_service: object
    health_service: object
    reminder_service: object
    error_notify_service: object


@dataclass(slots=True)
class AppState:
    pool: asyncpg.Pool
    repos: Repositories
    services: Services
