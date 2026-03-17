# Migration Map

Status date: 2026-03-17

## Purpose

This document translates the current repository artifact families into their planned target destinations for the `community-operations-platform` project space.

## Planned destination map

## Project landing

- `projects/community-operations-platform/README.md`
  - becomes the canonical project entrypoint

## Overview

- `ARCHITECTURE.md` -> `projects/community-operations-platform/overview/architecture.md`
- `PROJECT_CONTEXT.md` -> `projects/community-operations-platform/overview/project-context.md`
- `RELEASE_NOTES.md` -> `projects/community-operations-platform/overview/release-framing.md`

## Evidence

- `SANITIZATION.md` -> `projects/community-operations-platform/evidence/sanitization-notes.md`
- `evidence/excluded-artifacts.md` -> `projects/community-operations-platform/evidence/excluded-artifacts.md`
- `evidence/feature-matrix.md` -> `projects/community-operations-platform/evidence/feature-matrix.md`
- `evidence/relevance-for-business-roles.md` -> `projects/community-operations-platform/evidence/relevance-for-business-roles.md`
- `evidence/renamed-domain-terms.md` -> `projects/community-operations-platform/evidence/renamed-domain-terms.md`

## Extracts

- `bot/excerpts/*` -> curated through `projects/community-operations-platform/extracts/`
- `app/excerpts/*` -> curated through `projects/community-operations-platform/extracts/`
- selected `db/migrations/*.sql` -> referenced or mirrored from `projects/community-operations-platform/extracts/`

## Runnable app assets

- `app/` -> moved into `projects/community-operations-platform/`
- `bot/` -> moved into `projects/community-operations-platform/`
- `db/` -> moved into `projects/community-operations-platform/`
- `tests/` -> moved into `projects/community-operations-platform/`
- `requirements.txt` -> moved into `projects/community-operations-platform/`
- `pytest.ini` -> moved into `projects/community-operations-platform/`
- `config/` -> moved into `projects/community-operations-platform/`

## Migration order recommendation

1. populate project-level narrative and evidence first
2. establish extract navigation second
3. colocate project-local runtime assets inside the project folder
4. clean up root-level duplicates last

## Guardrails

- do not break the current local run path during narrative migration
- do not create two equally authoritative copies of the same narrative
- do not move technical assets before links and reviewer flow are stable
