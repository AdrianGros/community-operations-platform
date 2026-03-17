# M10 Detailed Plan

Status date: 2026-03-17

## Milestone

M10 - Compare current state and target state, then perform drift analysis

## Why this milestone exists

The repository now has:

- a defined target state from M5
- a materially populated canonical project space from M8
- a first hardening pass from M9

This milestone measures where the repository still differs from the intended target state so later corrective work is driven by explicit gaps instead of intuition.

## Main goal

Produce a concrete target-state versus current-state comparison, a drift list, and a proposed corrective action set.

## Scope

- compare planned and implemented canonical structure
- identify remaining mismatches
- classify gaps by severity and type
- suggest follow-up actions

## Out of scope

- implementing corrective actions
- major file moves
- final release preparation

## Expected outputs

1. A drift analysis document
2. A structured gap list
3. A corrective-action basis for M11

## Acceptance criteria

- major target-state gaps are explicit
- temporary transitional states are distinguished from unintended drift
- the output is actionable enough for M11 planning

## Risks

- misclassifying intentional transitional states as defects
- overlooking low-visibility documentation drift

## Planned artifacts

- `docs/drift/target-vs-current-analysis.md`
- `docs/bootstrap/m10-detailed-plan.md`
- `docs/bootstrap/m10-phase-report.md`

## Definition of done

M10 is done when the repository has a clear drift record that explains what is complete, what is transitional, and what still needs correction.

## Next planned milestone after M10

M11 - Plan corrective actions and research information security best practices

High-level intent:

- turn drift findings into a concrete action plan
- integrate publication-safe and info-security-aware cleanup guidance

## Fixed fallback milestone if M10 reveals issues

M10-FIX - Drift analysis correction and gap-list cleanup

Trigger conditions:

- important gaps were missed
- transitional states were classified incorrectly
- follow-up actions are too vague to guide M11
