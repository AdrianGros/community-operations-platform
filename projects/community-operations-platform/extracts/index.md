# Extract Index

This index points to the real technical artifacts that currently carry the strongest engineering signal for the project.

The artifacts now live inside the project folder itself, so this page is both the canonical reviewer-facing navigation layer and the local extract map.

## Application structure and wiring

- [`app/excerpts/startup_wiring.py`](../app/excerpts/startup_wiring.py)
  - startup composition and dependency boundaries
- [`app/state.py`](../app/state.py)
  - shared runtime state and repository wiring
- [`app/application/services.py`](../app/application/services.py)
  - service-layer orchestration
- [`app/infrastructure/repositories.py`](../app/infrastructure/repositories.py)
  - persistence-facing repository layer

## Governance and runtime controls

- [`bot/excerpts/guards_extract.py`](../bot/excerpts/guards_extract.py)
  - centralized guard and role-check logic
- [`db/migrations/026_governance_extract.sql`](../db/migrations/026_governance_extract.sql)
  - governance-related schema support

## Background processing and job handling

- [`bot/excerpts/session_loop_extract.py`](../bot/excerpts/session_loop_extract.py)
  - loop and worker-oriented runtime behavior
- [`db/migrations/028_jobs_extract.sql`](../db/migrations/028_jobs_extract.sql)
  - job claiming and related persistence structures

## Monitoring and failure signaling

- [`bot/excerpts/health_extract.py`](../bot/excerpts/health_extract.py)
  - health visibility and runtime checks
- [`bot/excerpts/error_notify_extract.py`](../bot/excerpts/error_notify_extract.py)
  - in-platform error routing and notification handling

## Migration discipline

- [`db/migrate.py`](../db/migrate.py)
  - SQL-first migration execution and checksum validation
- [`db/migrations/001_init_extract.sql`](../db/migrations/001_init_extract.sql)
- [`db/migrations/008_audit_extract.sql`](../db/migrations/008_audit_extract.sql)
- [`db/migrations/026_governance_extract.sql`](../db/migrations/026_governance_extract.sql)
- [`db/migrations/028_jobs_extract.sql`](../db/migrations/028_jobs_extract.sql)

## Navigation note

M8 intentionally builds reviewer-facing extract navigation before deciding whether each underlying artifact should later be moved, mirrored, or remain referenced in place.

Current stance:

- reviewer navigation is canonical here
- underlying technical artifacts are now colocated with the project instead of being split across the repository root
