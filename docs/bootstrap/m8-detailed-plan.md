# M8 Detailed Plan

Status date: 2026-03-17

## Milestone

M8 - Replace placeholders with real curated artifacts

## Why this milestone exists

M7 established a meaningful project skeleton.

This milestone replaces skeleton-only project-area descriptions with the real curated narrative and evidence artifacts that already exist in the legacy root layout.

## Main goal

Populate the canonical project space with actual overview, evidence, and extract-navigation artifacts while preserving the stability of the legacy runnable app.

## Key questions

1. Which existing root documents can now become canonical project documents?
2. Which evidence artifacts should move with minimal rewriting?
3. How should extracts be navigated before deeper code packaging decisions are made?

## Scope

- migrate overview documents into canonical project locations
- migrate evidence documents into canonical project locations
- create a real extract navigation document
- update project README references if needed

## Out of scope

- moving runnable app assets
- root cleanup and duplicate removal
- final hardening pass
- final drift analysis

## Expected outputs

1. Actual overview documents in the canonical project space
2. Actual evidence documents in the canonical project space
3. A real extract navigation document
4. A completed M8 phase report

## Acceptance criteria

- project overview and evidence folders contain real artifacts, not only skeleton notes
- extract navigation references real technical artifacts
- runnable root assets remain intact
- the canonical project space becomes the preferred reviewer entrypoint

## Risks

- duplicated content will temporarily exist at root and in the project folder
- link or naming inconsistencies can appear during migration

## Planned artifacts

- `docs/bootstrap/m8-detailed-plan.md`
- `docs/bootstrap/m8-phase-report.md`
- `projects/community-operations-platform/overview/architecture.md`
- `projects/community-operations-platform/overview/project-context.md`
- `projects/community-operations-platform/overview/release-framing.md`
- `projects/community-operations-platform/evidence/*`
- `projects/community-operations-platform/extracts/index.md`

## Definition of done

M8 is done when the project folder contains real migrated narrative and evidence artifacts and a reviewer can meaningfully stay inside the canonical project space for most of the showcase journey.

## Next planned milestone after M8

M9 - Hardening review

High-level intent:

- inspect the migrated structure for embarrassing mistakes, weak wording, bad links, and awkward presentation choices

## Fixed fallback milestone if M8 reveals issues

M8-FIX - Artifact migration correction and link cleanup

Trigger conditions:

- broken or confusing links
- duplicate files with competing authority
- migrated content landing in the wrong project subfolder
