# M11 Detailed Plan

Status date: 2026-03-17

## Milestone

M11 - Plan corrective actions and research information security best practices

## Why this milestone exists

M10 identified the remaining drift and cleanup gaps.

This milestone turns those gaps into a concrete corrective plan and overlays publication-safe, information-security-aware GitHub practices so M12 improves both quality and safety.

## Main goal

Define a prioritized corrective-action plan for the remaining repository gaps and ground those actions in official GitHub security and data-leak prevention guidance.

## Scope

- corrective action planning
- publication-safety guidance
- GitHub-native secret and leak prevention guidance
- prioritization for M12

## Out of scope

- implementing the corrective measures
- rewriting git history
- changing repository settings on GitHub

## Expected outputs

1. A corrective action plan
2. An information-security guidance note
3. A prioritized implementation scope for M12

## Acceptance criteria

- every major M10 gap has a proposed action
- security-sensitive publication concerns are addressed
- M12 implementation work is clearly scoped and ordered

## Risks

- planning actions that are too broad for one implementation milestone
- over-hardening and removing too much useful technical signal
- mixing repo-local fixes with GitHub platform settings we cannot apply from here

## Planned artifacts

- `docs/actions/corrective-action-plan.md`
- `docs/security/publication-and-repo-safety-guidance.md`
- `docs/bootstrap/m11-detailed-plan.md`
- `docs/bootstrap/m11-phase-report.md`

## Definition of done

M11 is done when M12 has a clear, prioritized corrective backlog with explicit safety guidance.

## Next planned milestone after M11

M12 - Implement the corrective measures

High-level intent:

- remove or reduce root duplication
- strengthen portfolio narrative
- normalize internal links
- tighten extract and root presentation

## Fixed fallback milestone if M11 reveals issues

M11-FIX - Corrective-plan cleanup and security-guidance correction

Trigger conditions:

- recommendations conflict with repository reality
- security guidance is too vague to implement
- M12 scope remains ambiguous after planning
