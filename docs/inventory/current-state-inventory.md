# Current-State Inventory

Status date: 2026-03-17

## Purpose

This document records the actual repository state before target-state planning and structural migration.

It treats the repository as it exists now:

- part legacy runnable showcase app
- part newly scaffolded showcase hub

## Repository shape summary

The repository currently has two coexisting layers.

### Layer 1 - Legacy runnable showcase root

These root-level paths still carry the operational weight of the old repository layout:

- `app/`
- `db/`
- `tests/`
- `evidence/`
- `config/`
- `requirements.txt`
- `pytest.ini`

This layer is still the practical runtime and test entrypoint.

### Layer 2 - New canonical showcase-hub scaffold

These paths define the intended future shape:

- `docs/bootstrap/`
- `docs/architecture/`
- `docs/research/`
- `portfolio/`
- `projects/`
- `projects/community-operations-platform/`

This layer is currently canonical for planning, but not yet canonical for the migrated project artifacts themselves.

## Current top-level artifact groups

## Repo-governance and planning documents

- `README.md`
- `docs/bootstrap/*`
- `docs/architecture/showcase-information-architecture.md`
- `docs/research/github-best-practices.md`

Role:

- define the refactor process
- define the intended repo navigation
- record milestone planning and research basis

## Legacy project framing documents

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `SANITIZATION.md`
- `RELEASE_NOTES.md`

Role:

- explain the existing showcase extract
- capture architectural value
- explain sanitization and review posture

Observation:

These are still strong candidate artifacts, but they currently live at root and compete with the new planned project-level structure.

## Runnable showcase application

- `app/`
- `db/`
- `tests/`
- `requirements.txt`
- `pytest.ini`

Role:

- runnable PySide6 governance showcase
- database migration and seed support
- automated tests

Observation:

This is the most implementation-heavy part of the repo and remains rooted in the legacy structure.

## Extract-only source artifacts

- `bot/excerpts/`
- `app/excerpts/`
- `db/migrations/*.sql`

Role:

- carry the strongest signal from the broader source system
- document guards, health, notification, session-loop, startup, and governance-relevant SQL evolution

Observation:

These artifacts already behave like curated extracts and should likely remain presented as such in the target repository.

## Evidence and curation support

- `evidence/excluded-artifacts.md`
- `evidence/feature-matrix.md`
- `evidence/relevance-for-business-roles.md`
- `evidence/renamed-domain-terms.md`

Role:

- explain what was kept, what was excluded, and why the extract is relevant

Observation:

This group is already close to a reusable `evidence/` package for the future canonical project folder.

## Current reviewer entrypoints

## Primary current entrypoint

- `README.md`

Strength:

- explains the repo is transitioning into a curated showcase hub
- points to canonical planning documents

Weakness:

- does not yet route deeply into a populated project folder because that migration is not done

## Secondary historical entrypoints

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `SANITIZATION.md`
- `RELEASE_NOTES.md`

Strength:

- high-value review context already exists

Weakness:

- these are still root-level and can make the repo feel split between old and new narratives

## Structural strengths

- the repo already contains a meaningful runnable showcase app
- extract quality is relatively disciplined and purpose-driven
- evidence and sanitization notes already exist
- the new planning layer is now explicit and reviewable
- the app tree already has reasonably clean internal separation:
  - `application/`
  - `domain/`
  - `infrastructure/`
  - `presentation/`

## Structural weaknesses

- dual structure: legacy root and new canonical scaffold coexist
- root-level project documents still compete with future project-level destinations
- `projects/community-operations-platform/` exists but is still mostly placeholder content
- reviewer navigation still depends heavily on historical root placement
- some curated extracts live under `bot/` and `app/excerpts/`, which may be sensible technically but not yet aligned with the final showcase narrative

## Ambiguities and migration-sensitive areas

## Canonical truth ambiguity

At the repo level, planning is already canonical in `docs/`, but project content is not yet canonical in `projects/community-operations-platform/`.

This is acceptable during migration, but cannot remain the final state.

## Documentation placement ambiguity

The following files likely belong in the future project overview area rather than at root:

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `SANITIZATION.md`
- `RELEASE_NOTES.md`

## Extract packaging ambiguity

The repo contains multiple extract styles:

- app-local excerpts
- bot excerpts
- SQL extracts

M5 must decide whether these remain distributed near code or get mirrored into a curated extract presentation area.

## Likely target-state mapping candidates

These are not final decisions. They are planning candidates for M5.

### Likely `projects/community-operations-platform/overview/`

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `RELEASE_NOTES.md`
- parts of `README.md` as project-level narrative

### Likely `projects/community-operations-platform/evidence/`

- `evidence/*`
- `SANITIZATION.md`

### Likely `projects/community-operations-platform/extracts/`

- `bot/excerpts/*`
- `app/excerpts/*`
- selected notes about SQL migration extracts

### Migration decision required

- whether `app/`, `db/`, `tests/`, `requirements.txt`, and `pytest.ini` move physically or remain in legacy-root form while project-level docs reference them

## Non-canonical runtime and tool artifacts

These exist locally but should not shape planning decisions:

- `.venv/`
- `.pytest_cache/`
- `var/`
- `__pycache__/`

## M5 implications

M5 should explicitly resolve:

- how quickly the project folder becomes the main reviewer entrypoint
- whether runnable code moves or is referenced in place
- how to present extracts without making the repo look fragmented
- how to reduce root-level narrative clutter while preserving technical signal
