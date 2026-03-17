# Community Operations Platform

This folder is the canonical reviewer entrypoint for the `community-operations-platform` project inside the showcase repository.

The repository is currently in migration:

- the reviewer-facing project structure is now defined here
- the runnable showcase application and supporting assets now live inside this project folder

## What this project shows

This project is curated to highlight:

- runtime governance and guardrails
- service-oriented application structure
- migration discipline and persistence boundaries
- worker and claim-based processing patterns
- sanitization-aware showcase curation

## How to navigate this project

- [`overview`](./overview/README.md): context, architecture, and project framing
- [`extracts`](./extracts/README.md): curated code and source extracts
- [`evidence`](./evidence/README.md): proof artifacts, relevance notes, and sanitization support
- [`roadmap`](./roadmap/README.md): migration steps and target-state planning

## Current implementation status

The project-level skeleton is active, but the underlying legacy materials are still being migrated into it milestone by milestone.

For now:

- project narrative is becoming canonical here
- project-local implementation assets live here:
  - `app/`
  - `bot/`
  - `config/`
  - `db/`
  - `tests/`
  - `requirements.txt`
  - `pytest.ini`

## Run

From this folder, the project can be started with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m app.main
```

Tests:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest tests
```

## Reviewer guidance

If you want the high-level story first, start with [`overview`](./overview/README.md).

If you want technical substance first, continue with [`extracts`](./extracts/README.md).

If you want to understand curation, sanitization, and why certain materials were selected, open [`evidence`](./evidence/README.md).

If you want to understand how the repo is being transformed into its target shape, use [`roadmap`](./roadmap/README.md).
