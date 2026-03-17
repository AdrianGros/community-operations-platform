from __future__ import annotations

from enum import StrEnum


class RoleCode(StrEnum):
    ADMIN = "ADMIN"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"


class CaseStatus(StrEnum):
    OPEN = "open"
    CLAIMED = "claimed"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"


class FindingStatus(StrEnum):
    IDENTIFIED = "identified"
    IN_PROGRESS = "in_progress"
    MITIGATED = "mitigated"
    ACCEPTED = "accepted"
    CLOSED = "closed"


class MeasureStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ACCEPTED = "accepted"


class ControlStatus(StrEnum):
    NEEDS_ATTENTION = "needs_attention"
    PARTIALLY_EFFECTIVE = "partially_effective"
    MONITORED = "monitored"
    EFFECTIVE = "effective"


ROLE_TIERS: dict[RoleCode, int] = {
    RoleCode.AUDITOR: 10,
    RoleCode.REVIEWER: 20,
    RoleCode.ADMIN: 30,
}
