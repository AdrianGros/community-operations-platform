# Community Operations Platform Showcase

This repository is being refactored from a single showcase app into a curated showcase hub.

The goal is to make this repository the single source of truth for portfolio-ready project extracts, evidence, architecture notes, and runnable showcase assets around the broader `community-operations-platform` work.

The canonical project entrypoint is now [`projects/community-operations-platform`](./projects/community-operations-platform).

## Current state

Today, the runnable governance showcase app still lives in the legacy root layout:

- [`app`](./app)
- [`db`](./db)
- [`tests`](./tests)
- [`evidence`](./evidence)

That runtime layout remains intentionally untouched for now so the existing local workflow does not break during curation.

## New canonical structure

The target structure for the refactor starts at the repository root:

- [`docs/bootstrap`](./docs/bootstrap): project brief, scope boundaries, milestones
- [`docs/architecture`](./docs/architecture): showcase information architecture and repo rules
- [`portfolio`](./portfolio): cross-project positioning and curation guidance
- [`projects`](./projects): curated project folders
- [`projects/community-operations-platform`](./projects/community-operations-platform): canonical folder for this project's curated materials

## Planning baseline

This repository now follows a DAD-M-inspired bootstrap flow:

1. Define the project brief.
2. Define safety boundaries.
3. Define milestones.
4. Keep planning artifacts explicit.
5. Refactor the structure milestone by milestone instead of doing a blind big-bang move.

See:

- [`docs/bootstrap/project-brief.md`](./docs/bootstrap/project-brief.md)
- [`docs/bootstrap/safety-boundaries.md`](./docs/bootstrap/safety-boundaries.md)
- [`docs/bootstrap/milestones.md`](./docs/bootstrap/milestones.md)
- [`docs/architecture/showcase-information-architecture.md`](./docs/architecture/showcase-information-architecture.md)

## Reviewer start point

The preferred reviewer path is now:

1. this root README
2. [`projects/community-operations-platform`](./projects/community-operations-platform/)
3. one of `overview`, `extracts`, `evidence`, or `roadmap`

## Legacy local run

Until the migration milestone moves the runnable app into its new curated project folder, the existing local run path stays the same:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m app.main
```

Tests:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest tests
```
