# Target-State Versus Current-State Analysis

Status date: 2026-03-17

## Purpose

This document compares the implemented repository state after M9 with the target-state design defined in M5.

It distinguishes:

- completed target-state elements
- intentional transitional states
- unaddressed drift that still needs corrective action

## Summary verdict

The repository is on-track but not yet fully aligned with the target state.

### What is already aligned

- the root README is now primarily navigational
- `docs/` is functioning as the canonical planning and architecture area
- `projects/community-operations-platform/` is now a real canonical project-space entrypoint
- `overview/`, `extracts/`, `evidence/`, and `roadmap/` all exist and contain meaningful content
- relative links have been introduced in the main reviewer-facing navigation layer

### What is intentionally transitional

- legacy root narrative documents still exist alongside their migrated project-space versions
- runnable app assets remain at root by design
- extract artifacts are still referenced in place rather than physically reorganized into the project folder

### What still drifts from target state

- the root still contains duplicate narrative documents that weaken the single-source-of-truth rule
- the `portfolio/` layer is still only lightly populated
- internal planning and phase-report docs still contain many absolute `/opt/...` links
- the project extract layer is navigable, but still depends on legacy-root technical locations rather than a final curated extract packaging strategy

## Comparison by target-state area

## Root

### Target

- concise repository identity
- explicit reviewer navigation
- no deep project narrative duplication

### Current

- repository identity and navigation are present
- reviewer path is explicit
- root still contains legacy project narrative files:
  - `ARCHITECTURE.md`
  - `PROJECT_CONTEXT.md`
  - `RELEASE_NOTES.md`
  - `SANITIZATION.md`

### Drift judgment

Partial alignment.

The root is much closer to the target than before, but duplicate project narrative remains.

## `docs/`

### Target

- canonical home for planning, research, architecture, inventory, drift, and governance

### Current

- bootstrap plans exist
- research exists
- inventory exists
- drift analysis now exists
- backup and operations note exists

### Drift judgment

Strong alignment.

Residual issue:

- internal documentation still uses environment-specific absolute links in many phase reports

## `portfolio/`

### Target

- cross-project narrative and future project index

### Current

- only a minimal placeholder-style README exists

### Drift judgment

Meaningful drift remains.

The layer exists structurally but is not yet substantively curated.

## `projects/community-operations-platform/`

### Target

- canonical project landing page
- meaningful overview, extracts, evidence, and roadmap areas

### Current

- project landing page exists and is reviewer-usable
- overview contains real migrated documents
- evidence contains real migrated documents
- roadmap contains migration planning
- extracts contain a real index

### Drift judgment

Strong alignment.

Residual issue:

- extracts are navigationally good, but still operationally dependent on legacy-root paths

## Runnable app assets

### Target

- remain stable until later decision point

### Current

- still at root
- still referenced as legacy runtime structure

### Drift judgment

Aligned with the current phased plan.

This is a deferred design decision, not a defect.

## Gap list

## G1 - Duplicate narrative at root

Severity: medium

Description:

Legacy root narrative documents still coexist with the canonical project-space versions.

Impact:

- weakens the single-source-of-truth rule
- risks reviewer confusion about which copy is canonical

Recommended action:

- decide whether to remove, replace with stubs, or reduce root files in M11/M12

## G2 - Thin portfolio layer

Severity: medium

Description:

`portfolio/` exists structurally but has almost no substantive cross-project narrative yet.

Impact:

- the repository is not yet fully convincing as a multi-project showcase hub

Recommended action:

- add a first substantive portfolio positioning document

## G3 - Absolute links in internal docs

Severity: low

Description:

Many bootstrap and phase-report documents still use `/opt/...` markdown links.

Impact:

- low impact for a reviewer entering through the main project path
- moderate quality smell for anyone reading the planning layer on GitHub

Recommended action:

- normalize internal docs to relative links during corrective cleanup

## G4 - Extract packaging still transitional

Severity: medium

Description:

The extract layer is reviewer-friendly, but artifacts remain in legacy-root technical locations.

Impact:

- the presentation is better, but the final packaging strategy is still unresolved

Recommended action:

- decide whether to keep referencing in place or to mirror selected extracts in a later milestone

## G5 - Root cleanup still pending

Severity: medium

Description:

The root still contains more historical material than the target state ultimately wants.

Impact:

- the repo can still feel partially historical instead of fully curated

Recommended action:

- perform a targeted root cleanup after corrective planning

## Corrective-action basis for M11

M11 should plan actions in four groups:

1. single-source-of-truth cleanup
2. portfolio-layer strengthening
3. internal-doc link normalization
4. extract packaging decision and root cleanup sequencing

## Overall readiness judgment

The repository is good enough to continue.

It already behaves like a real showcase project, but it does not yet fully satisfy the end-state standard of "one clean curated hub with minimal transitional noise."
