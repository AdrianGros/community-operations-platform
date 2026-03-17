# M6 Detailed Plan

Status date: 2026-03-17

## Milestone

M6 - Back up the current repository state

## Why this milestone exists

M5 produced an implementation-ready target-state design.

Before physical migration work starts, we need a verified backup of the current repository state so later structure changes are reversible and reviewable.

## Main goal

Create a restorable backup of the repository that captures the current working tree, including uncommitted planning artifacts, and record how it can be verified and restored.

## Key questions

1. What exactly should the backup include?
2. How do we avoid backing up irrelevant local runtime artifacts?
3. How will we verify that the backup exists and is usable?
4. How will a future restore be performed if needed?

## Scope

- backup planning
- backup creation
- backup verification
- restore-note documentation

## Out of scope

- structural migration
- file moves
- hardening changes
- commit and push

## Source policy

Use the repository working tree as it exists now, including uncommitted planning documents.

Exclude obviously local-only runtime and cache artifacts that are not part of the curated repository state.

## Expected outputs

1. A backup archive
2. A checksum for the archive
3. A backup record document
4. A restore note

## Acceptance criteria

- backup artifact exists on disk
- backup verification data exists
- the backup record identifies timestamp and source state
- a future restore path is documented

## Risks

- excluding something important by mistake
- creating a backup that cannot be clearly tied to a repo state
- treating backup creation as sufficient without verification

## Planned execution steps

1. Record the current repo status and source revision.
2. Define inclusion and exclusion rules.
3. Create a compressed archive backup.
4. Generate checksum and size metadata.
5. Write a backup record and restore note.

## Planned artifacts

- `docs/bootstrap/m6-detailed-plan.md`
- `docs/operations/backup-record.md`
- `docs/bootstrap/m6-phase-report.md`

## Definition of done

M6 is done when the repo has a verified backup artifact and a written restore note that future milestones can rely on.

## Next planned milestone after M6

M7 - Build the repository skeleton

High-level intent:

- replace placeholder project-level documents with canonical narrative structure
- create the stable reviewer-facing skeleton before physical asset moves

## Fixed fallback milestone if M6 reveals issues

M6-FIX - Backup verification and recovery-note correction

Trigger conditions:

- archive missing or incomplete
- checksum missing
- restore note unclear or unsafe
