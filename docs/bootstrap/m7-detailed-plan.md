# M7 Detailed Plan

Status date: 2026-03-17

## Milestone

M7 - Build the repository skeleton

## Why this milestone exists

M5 defined the target-state structure and M6 created a verified backup.

This milestone turns the planned project space into a real reviewer-facing skeleton so later migrations populate an already meaningful structure instead of dumping files into placeholder folders.

## Main goal

Replace placeholder project-space documents with a real canonical skeleton that explains how the project should be navigated, what belongs in each section, and how legacy-root content relates to the new structure.

## Key questions

1. What should a reviewer immediately understand inside the project folder?
2. How should each subfolder communicate its role before all real artifacts are migrated?
3. How do we build a meaningful skeleton without duplicating legacy content too early?

## Scope

- project-level landing page
- overview, extracts, evidence, and roadmap skeleton docs
- canonical navigation wording
- skeleton-stage migration guidance

## Out of scope

- moving legacy docs into new destinations
- moving runnable app assets
- full extract curation
- root cleanup

## Expected outputs

1. A project-level landing page that acts as the canonical reviewer entrypoint
2. Non-placeholder README files for `overview/`, `extracts/`, `evidence/`, and `roadmap/`
3. A consistent explanation of how legacy-root assets relate to the new project structure

## Acceptance criteria

- the project folder feels real, not empty
- each project subfolder has a clear role description
- a reviewer can understand where future migrated content will appear
- no runnable legacy assets are moved yet

## Risks

- skeleton docs can still feel too abstract if not tied to real artifact groups
- duplicating narrative too aggressively could create competing truths

## Planned artifacts

- `docs/bootstrap/m7-detailed-plan.md`
- `docs/bootstrap/m7-phase-report.md`
- `projects/community-operations-platform/README.md`
- `projects/community-operations-platform/overview/README.md`
- `projects/community-operations-platform/extracts/README.md`
- `projects/community-operations-platform/evidence/README.md`
- `projects/community-operations-platform/roadmap/README.md`

## Definition of done

M7 is done when the canonical project folder becomes a meaningful navigation surface even before M8 migrates the real artifacts.

## Next planned milestone after M7

M8 - Replace placeholders with real curated artifacts

High-level intent:

- move or rewrite the real docs and evidence into the project space
- replace skeleton narratives with actual curated project material

## Fixed fallback milestone if M7 reveals issues

M7-FIX - Skeleton cleanup and placeholder correction

Trigger conditions:

- navigation still feels unclear
- folder roles overlap
- the skeleton creates competing narratives with the root
