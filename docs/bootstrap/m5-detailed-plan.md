# M5 Detailed Plan

Status date: 2026-03-17

## Milestone

M5 - Plan the target repository using M3 and M4

## Why this milestone exists

M3 defined what good GitHub repository curation should look like.
M4 documented the actual current state of this repository.

This milestone converts those two inputs into a precise target-state design that later migration work can implement without improvising architecture in the middle of file moves.

## Main goal

Define the target repository structure, migration rules, artifact destinations, and reviewer navigation model for the curated showcase repository.

## Key questions

1. What is the canonical target state for the repository root?
2. What belongs in `docs/`, `portfolio/`, and `projects/`?
3. What should move into `projects/community-operations-platform/` and what should remain temporarily at root?
4. How should runnable assets, curated extracts, and evidence be presented differently?
5. What migration sequence minimizes risk and confusion?

## Scope

- target-state repository design
- artifact destination planning
- canonical-path decisions
- migration rules
- reviewer journey planning

## Out of scope

- physical migration of files
- backup implementation
- final wording cleanup
- hardening and drift remediation

## Source policy

Use only established repository-local inputs for design decisions:

- M3 research
- M4 current-state inventory
- existing architecture and planning documents

## Expected outputs

1. A target-state design document
2. A migration mapping for major artifact groups
3. A decision on root versus project-level responsibilities
4. A phased migration sequence for later implementation milestones

## Acceptance criteria

- every major artifact family has a canonical target destination
- root responsibilities are clearly separated from project responsibilities
- the plan supports reviewer navigation and future multi-project growth
- the plan is implementation-ready enough for M6 and M7

## Risks

- designing a target state that is too idealized for the current repository reality
- introducing too many layers and weakening readability
- planning moves that could break the still-runnable legacy app if executed too early

## Planned execution steps

1. Combine M3 rules with M4 inventory findings.
2. Define the target-state responsibilities of root, `docs/`, `portfolio/`, and `projects/`.
3. Assign each major current artifact group to a canonical target destination.
4. Define migration rules and sequencing constraints.
5. Capture open decisions that later milestones must implement carefully.

## Planned artifacts

- `docs/architecture/target-state-repository-plan.md`
- `projects/community-operations-platform/roadmap/migration-map.md`
- `docs/bootstrap/m5-detailed-plan.md`
- `docs/bootstrap/m5-phase-report.md`

## Definition of done

M5 is done when the repository contains a clear target-state design and a migration map that later milestones can implement without re-planning the structure from scratch.

## Next planned milestone after M5

M6 - Back up the current repository state

High-level intent:

- create a restorable safety point
- verify that untracked planning artifacts are included in the backup strategy

## Fixed fallback milestone if M5 reveals issues

M5-FIX - Target-state design correction and migration rule cleanup

Trigger conditions:

- target destinations remain ambiguous
- migration rules conflict with actual repo constraints
- reviewer journey remains unclear after planning
