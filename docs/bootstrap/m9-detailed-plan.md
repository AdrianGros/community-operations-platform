# M9 Detailed Plan

Status date: 2026-03-17

## Milestone

M9 - Hardening review

## Why this milestone exists

M8 populated the canonical project space with real curated artifacts.

Before we move on to drift analysis, we need a quality pass focused on obvious presentation mistakes, weak navigation, and implementation choices that would look careless in a public GitHub showcase.

## Main goal

Identify and correct obvious quality issues in the migrated repository presentation, especially issues that would harm reviewer trust or make the repository feel clumsy.

## Review focus

- absolute local filesystem links in Markdown
- unclear or weak reviewer navigation
- project-space documentation rough edges
- wording that feels transitional or unnecessarily awkward
- obvious duplication or conflicting authority signals

## Scope

- reviewer-facing markdown documents
- core navigation documents
- project-space presentation quality

## Out of scope

- large structural migration
- runnable asset relocation
- final drift analysis

## Expected outputs

1. A findings list
2. Immediate fixes for clear issues
3. A hardening phase report

## Acceptance criteria

- obvious broken or environment-specific links are removed from reviewer-facing docs
- project navigation becomes more GitHub-friendly
- no major embarrassing presentation issue remains in the core entrypoints

## Risks

- fixing too little and leaving obvious rough edges behind
- overediting internal planning documents without improving external readability

## Planned artifacts

- `docs/bootstrap/m9-detailed-plan.md`
- `docs/bootstrap/m9-phase-report.md`

## Definition of done

M9 is done when the most visible presentation and navigation issues have either been fixed or explicitly recorded as residual follow-up work.

## Next planned milestone after M9

M10 - Compare current state and target state, then perform drift analysis

High-level intent:

- compare the implemented structure against the planned target state
- record remaining mismatches and corrective actions

## Fixed fallback milestone if M9 reveals issues

M9-FIX - Hardening correction and presentation cleanup

Trigger conditions:

- hardening introduces new inconsistencies
- important broken links remain
- reviewer-facing docs still feel low quality after first-pass fixes
