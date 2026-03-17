from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class User:
    id: int
    display_name: str
    is_active: bool = True


@dataclass(slots=True)
class RoleBinding:
    user_id: int
    role_code: str
    assigned_at: datetime


@dataclass(slots=True)
class GovernancePolicy:
    id: int
    read_only_enabled: bool
    feature_flags: dict[str, bool]
    updated_at: datetime
    updated_by: int | None


@dataclass(slots=True)
class ReviewCase:
    id: int
    title: str
    summary: str
    case_kind: str
    risk_level: str
    status: str
    priority: str
    finding_status: str
    control_status: str
    measure_title: str
    measure_status: str
    measure_owner: int | None
    due_at: datetime | None
    evidence_note: str | None
    claimed_by: int | None
    claimed_at: datetime | None
    decision: str | None
    decision_reason: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class CaseActionState:
    case_id: int
    allowed_actions: dict[str, bool]
    primary_hint: str
    blocker_code: str | None = None


@dataclass(slots=True)
class AuditEvent:
    id: int
    occurred_at: datetime
    actor_user_id: int | None
    severity: str
    domain: str
    action: str
    entity_type: str
    entity_id: int | None
    payload_json: str


@dataclass(slots=True)
class HealthCheckResult:
    id: int
    check_type: str
    ok: bool
    message: str
    measured_at: datetime
    details_json: str


@dataclass(slots=True)
class MigrationStatus:
    current_version: str
    migration_count: int
    latest_applied_at: datetime | None
    schema_ok: bool
    expected_table_count: int = 0
    actual_table_count: int = 0
    missing_items: list[str] = field(default_factory=list)
