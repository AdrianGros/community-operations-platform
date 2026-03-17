# M8 Phase Report

Status date: 2026-03-17
Milestone: M8 - Replace placeholders with real curated artifacts

## Discover

### Status

Completed

### Input Summary

The milestone inspected the existing root-level overview and evidence documents and selected the ones that should become canonical project-space artifacts first.

### Artifacts

- migrated overview, evidence, and extract-navigation files under [`projects/community-operations-platform`](../../projects/community-operations-platform)

### Risks and Assumptions

- assumption: duplicating narrative temporarily is acceptable during migration
- risk: root-level duplicates still exist until later cleanup milestones

### Next Step

Promote the migrated project-space artifacts as the preferred reviewer path.

## Apply

### Status

Completed

### Input Summary

The strongest available migration candidates were:

- overview documents from the root
- evidence documents from the root `evidence/` folder
- a reviewer-facing extract index built from existing technical artifact paths

### Artifacts

- canonical project-space overview, evidence, and extracts documents

### Risks and Assumptions

- risk: some file references may later need normalization to relative links during cleanup
- assumption: the chosen first-wave artifacts are enough to make the project folder materially useful

### Next Step

Persist the migrated artifacts and prepare for hardening review.

## Deploy

### Status

Completed

### Input Summary

The milestone required replacing skeleton-stage content with real curated material while leaving runnable root assets untouched.

### Artifacts

- [`docs/bootstrap/m8-detailed-plan.md`](./m8-detailed-plan.md)
- [`projects/community-operations-platform/overview/architecture.md`](../../projects/community-operations-platform/overview/architecture.md)
- [`projects/community-operations-platform/overview/project-context.md`](../../projects/community-operations-platform/overview/project-context.md)
- [`projects/community-operations-platform/overview/release-framing.md`](../../projects/community-operations-platform/overview/release-framing.md)
- [`projects/community-operations-platform/evidence/feature-matrix.md`](../../projects/community-operations-platform/evidence/feature-matrix.md)
- [`projects/community-operations-platform/evidence/relevance-for-business-roles.md`](../../projects/community-operations-platform/evidence/relevance-for-business-roles.md)
- [`projects/community-operations-platform/evidence/renamed-domain-terms.md`](../../projects/community-operations-platform/evidence/renamed-domain-terms.md)
- [`projects/community-operations-platform/evidence/excluded-artifacts.md`](../../projects/community-operations-platform/evidence/excluded-artifacts.md)
- [`projects/community-operations-platform/evidence/sanitization-notes.md`](../../projects/community-operations-platform/evidence/sanitization-notes.md)
- [`projects/community-operations-platform/extracts/index.md`](../../projects/community-operations-platform/extracts/index.md)
- [`docs/bootstrap/m8-phase-report.md`](./m8-phase-report.md)

### Risks and Assumptions

- risk: root-level duplicates can confuse reviewers until cleanup happens
- assumption: M9 will catch naming, wording, and link issues introduced during migration

### Next Step

Start M9 and review the migrated project space for weak wording, broken links, and awkward structure.

### Implementation Summary

Migrated the strongest overview and evidence documents into the canonical project space and created a real extract index that points to the existing technical artifacts.

### Files Changed

- `docs/bootstrap/m8-detailed-plan.md`
- `docs/bootstrap/m8-phase-report.md`
- `projects/community-operations-platform/overview/*`
- `projects/community-operations-platform/evidence/*`
- `projects/community-operations-platform/extracts/index.md`
- `projects/community-operations-platform/overview/README.md`
- `projects/community-operations-platform/evidence/README.md`
- `projects/community-operations-platform/extracts/README.md`
- `docs/bootstrap/milestones.md`

### Proofs

- canonical overview documents now exist
- canonical evidence documents now exist
- extract navigation points to real technical artifacts
- runnable root assets remain untouched

### Acceptance Checklist

- overview folder contains real documents
- evidence folder contains real documents
- extracts section references real artifacts
- project space is materially more useful than the old placeholder skeleton

### Next Steps

- run the hardening review
- fix weak wording and navigation issues
- prepare for later drift analysis

## Monitor

### Status

Completed

### Input Summary

Review whether the canonical project space now contains enough real content to move from migration into quality review.

### Artifacts

- milestone judgment in this file

### Risks and Assumptions

- residual risk: root-level duplicates are still present
- residual risk: extract navigation still references legacy-root technical paths by design

### Next Step

Proceed to M9.

## Monitor verdict

M8 is complete and good enough to unblock M9.

No `M8-FIX` milestone is required right now.

Reasons:

- the project space now contains real migrated narrative and evidence artifacts
- the extract layer is no longer placeholder-only
- remaining concerns are quality and cleanup issues, which belong in M9
