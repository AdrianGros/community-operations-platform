# Target-State Repository Plan

Status date: 2026-03-17

## Purpose

This document defines the intended target state for the repository after the showcase refactor.

It uses:

- M3 GitHub best-practice research
- M4 current-state inventory

## Target-state principle

The repository should present itself as a curated showcase hub first and a historical code dump never.

That means:

- the root is navigational
- project-specific narrative lives in project folders
- repository-wide planning and governance live in `docs/`
- cross-project positioning lives in `portfolio/`
- each showcased project has one canonical home under `projects/`

## Canonical top-level responsibilities

## Root

The root is responsible for:

- repository identity
- first-contact reviewer navigation
- explaining the difference between canonical content and legacy-in-transition content

The root is not responsible for:

- full project documentation
- deep architecture narrative
- duplicated evidence packages

## `docs/`

`docs/` is the canonical home for repository-wide material:

- bootstrap and milestone planning
- architecture of the showcase repository itself
- research findings
- inventories, drift analyses, and governance notes

`docs/` is not the canonical home for the narrative of a specific showcased project.

## `portfolio/`

`portfolio/` is the canonical home for cross-project narrative:

- who the showcase is for
- how the projects relate to one another
- curation standards
- future project index pages

## `projects/`

`projects/` is the canonical home for all project-specific curated content.

Each showcased project must have exactly one canonical project folder.

## Canonical project structure

For `projects/community-operations-platform/`, the canonical structure should be:

```text
projects/community-operations-platform/
  README.md
  app/
  bot/
  config/
  db/
  tests/
  requirements.txt
  pytest.ini
  overview/
  extracts/
  evidence/
  roadmap/
```

### `README.md`

Role:

- project landing page
- reviewer entrypoint for the specific project
- links to overview, extracts, evidence, and roadmap
- explains runnable versus non-runnable areas

### `overview/`

Role:

- project narrative
- project context
- architecture summary
- release framing

### `extracts/`

Role:

- curated source extracts
- packaging notes for excerpts
- explanation of what was preserved and why

### `evidence/`

Role:

- feature matrix
- business-role relevance
- renamed-domain terms
- excluded artifact explanations
- sanitization notes

### `roadmap/`

Role:

- migration maps
- target-state notes
- project-specific follow-up planning

## Canonical destination map

## Root README

Current:

- `README.md`

Target role:

- remains at root
- becomes shorter, more navigational, and more explicit about where the canonical project lives

## Legacy project framing docs

Current:

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `RELEASE_NOTES.md`
- `SANITIZATION.md`

Target:

- move their canonical narrative into `projects/community-operations-platform/overview/` and `projects/community-operations-platform/evidence/`

Decision:

- `ARCHITECTURE.md` -> `projects/community-operations-platform/overview/architecture.md`
- `PROJECT_CONTEXT.md` -> `projects/community-operations-platform/overview/project-context.md`
- `RELEASE_NOTES.md` -> `projects/community-operations-platform/overview/release-framing.md`
- `SANITIZATION.md` -> `projects/community-operations-platform/evidence/sanitization-notes.md`

## Evidence files

Current:

- `evidence/excluded-artifacts.md`
- `evidence/feature-matrix.md`
- `evidence/relevance-for-business-roles.md`
- `evidence/renamed-domain-terms.md`

Target:

- move into `projects/community-operations-platform/evidence/`

Decision:

- preserve file purposes, normalize names only if it improves navigation

## Extract artifacts

Current:

- `bot/excerpts/*`
- `app/excerpts/*`
- selected SQL migration extracts under `db/migrations/`

Target:

- curate them from `projects/community-operations-platform/extracts/`

Decision:

- create project-level extract navigation first
- later decide per artifact whether to move, mirror, or reference in place

This avoids breaking the current technical structure too early.

## Runtime and source assets

Current:

- `projects/community-operations-platform/app/`
- `projects/community-operations-platform/bot/`
- `projects/community-operations-platform/db/`
- `projects/community-operations-platform/tests/`
- `projects/community-operations-platform/requirements.txt`
- `projects/community-operations-platform/pytest.ini`
- `projects/community-operations-platform/config/`

Target:

- live inside the project folder
- be referenced from the project README, extracts, and roadmap
- stay colocated with the project unless a later packaging reason clearly justifies another split

Decision:

- project-local runtime and source assets now belong inside the project folder instead of the repository root

## Migration rules

## Rule 1 - One canonical narrative location per topic

When a topic gets a new canonical home, older locations should become transitional or be removed later.

## Rule 2 - Narrative before physical moves

First establish canonical documentation and navigation.
Only then move technical assets that could affect runs, tests, or link integrity.

## Rule 3 - Preserve run stability

Do not move runnable app assets in a way that breaks the current local workflow until the migration plan explicitly allows it.

## Rule 4 - Prefer relative internal links

Project and repo docs should link through relative paths wherever possible.

## Rule 5 - Keep extracts clearly marked as extracts

Curated excerpts must not be presented as the complete original system.

## Rule 6 - Root should get simpler over time

Every migration step should reduce root-level ambiguity, not add new root-level explanations.

## Reviewer journey design

## Repository-level reviewer path

1. land on root `README.md`
2. understand the repo is a curated showcase hub
3. enter `projects/community-operations-platform/`
4. choose between overview, extracts, evidence, and roadmap

## Project-level reviewer path

1. read project `README.md`
2. open `overview/` for context and architecture
3. open `extracts/` for technical substance
4. open `evidence/` for curation and relevance proof
5. open `roadmap/` for migration and future-state thinking

## Phased migration sequence

## Phase A - Narrative migration

- populate project `README.md`
- move or rewrite overview docs
- move or rewrite evidence docs

## Phase B - Extract curation

- build project-level extract navigation
- decide whether extract files are moved, mirrored, or referenced

## Phase C - Runtime and source asset colocation

- after backup and stable navigation, colocate the project-local runtime and source assets inside the project folder

## Phase D - Root cleanup

- remove or minimize outdated root-level duplicates
- tighten root navigation

## Deferred decisions

- whether the runnable app will ultimately move into the project folder or remain referenced in place
- whether project onboarding should later become a reusable template
- whether this repository should become the primary pinned showcase repo or sit below a broader hub

## M6 and M7 implications

M6 should back up both:

- legacy-root project assets
- newly created planning and target-state documents

M7 should implement the target skeleton and canonical narrative locations before touching the runnable app layout.
