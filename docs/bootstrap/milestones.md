# Milestone Plan

This repository now has two milestone layers:

- `M1-M2` define the bootstrap and structure baseline
- `M3-M14` define the operational repo-refactor program

The numbering keeps the earlier bootstrap work intact and extends it with the milestone sequence you defined.

## M1 - Bootstrap the showcase hub

### Goal

Define the single source of truth for the repository refactor and scaffold the first canonical folder structure.

### Scope

- project brief
- safety boundaries
- milestone definitions
- showcase information architecture
- root README repositioning
- initial `docs/`, `portfolio/`, and `projects/` folders

### Deliverables

- bootstrap documents under `docs/bootstrap/`
- information architecture document
- updated root README
- scaffolded project folder for `community-operations-platform`

### Acceptance criteria

- a contributor can understand the target repo shape from the repository itself
- the new structure exists without breaking the current root app workflow
- planning decisions are recorded in files instead of only chat history

### Status

Completed in the current planning phase.

## M2 - Stabilize the canonical project entrypoint

### Goal

Make `projects/community-operations-platform/` the planned canonical home for the first curated project without forcing a risky big-bang move.

### Scope

- create canonical project subfolders
- define migration intent
- keep legacy root folders temporarily intact

### Deliverables

- project folder scaffold
- transition-safe repo navigation

### Acceptance criteria

- the intended canonical project location is obvious
- the repo can continue into research and migration milestones without structural ambiguity

### Status

Started through scaffolding; full migration belongs to later milestones.

## M3 - Research best practices for GitHub documentation and portfolio presentation

### Goal

Understand how strong GitHub showcase repositories are structured, documented, and curated.

### Scope

- repository landing pages
- project index patterns
- project-level README structures
- evidence and architecture note patterns
- portfolio presentation conventions

### Deliverables

- best-practice findings
- candidate patterns to adopt
- anti-pattern list to avoid

### Acceptance criteria

- we can justify the target repo structure using external best-practice evidence instead of taste alone

### Risks

- collecting too many examples without extracting actionable structure rules

## M4 - Produce a robust current-state inventory

### Goal

Create a reliable view of the current repository as it actually exists.

### Scope

- file and folder inventory
- artifact classification
- duplicate or ambiguous content
- existing reviewer entrypoints
- current pain points

### Deliverables

- current-state map
- artifact inventory
- known structural weaknesses

### Acceptance criteria

- we know what exists, what matters, and what should not survive into the curated target state

### Risks

- hidden duplication between legacy root content and newly scaffolded canonical paths

## M5 - Plan the target repository using M3 and M4

### Goal

Turn research findings and current-state facts into the target repository design.

### Scope

- naming conventions
- canonical paths
- migration rules
- project reviewer journeys
- legacy-to-target mapping

### Deliverables

- target-state repository design
- mapping from current artifacts to target destinations
- migration sequence proposal

### Acceptance criteria

- every important current artifact has a planned destination in the target repo

### Risks

- overdesign before we verify the actual inventory

## M6 - Back up the current repository state

### Goal

Create a restorable backup before structural migration begins.

### Scope

- git-level safety
- local snapshot or archive
- backup verification

### Deliverables

- confirmed backup artifact
- short restore note

### Acceptance criteria

- we can proceed with structural moves without relying on memory or luck

### Risks

- incomplete backup that misses untracked but important files

## M7 - Build the repository skeleton

### Goal

Create the full target folder framework for the curated repository.

### Scope

- root navigation
- portfolio-level structure
- project-level structure
- templates or placeholder docs where needed

### Deliverables

- skeleton tree
- canonical entry docs
- placeholder files for target locations

### Acceptance criteria

- the target repo shape exists even before all real artifacts are migrated

### Risks

- placeholders may linger too long and look unfinished if M8 is delayed

## M8 - Replace placeholders with real curated artifacts

### Goal

Populate the skeleton with the actual repository content that deserves to be showcased.

### Scope

- move or rewrite key docs
- move or rewrite evidence files
- move or package code extracts
- update links and navigation

### Deliverables

- populated project folders
- reduced placeholder usage
- clearer reviewer flow

### Acceptance criteria

- a reviewer can meaningfully navigate the project without relying on placeholder documents

### Risks

- artifact quality may vary and require additional polishing

## M9 - Hardening review

### Goal

Check whether the repository still contains embarrassing errors, weak decisions, or obviously poor presentation choices.

### Scope

- wording quality
- structural awkwardness
- broken links or confusing navigation
- suspicious artifacts
- low-quality or misleading claims

### Deliverables

- hardening findings list
- prioritized fix list

### Acceptance criteria

- obvious quality issues are identified before the repo is treated as publication-ready

### Risks

- "looks fine" bias if review is too close to implementation work

## M10 - Compare current state and target state, then perform drift analysis

### Goal

Measure how far the repository still deviates from the planned target design.

### Scope

- path-level comparison
- content-level comparison
- reviewer-flow comparison
- unresolved gaps and leftovers

### Deliverables

- drift analysis
- gap list
- recommended corrective actions

### Acceptance criteria

- remaining differences are explicit instead of implicit

### Risks

- target-state definition may need refinement if reality exposes new constraints

## M11 - Plan corrective actions and research information security best practices

### Goal

Translate drift findings into concrete measures and validate them against information-security-minded publication practices.

### Scope

- sanitization posture
- evidence exposure rules
- metadata hygiene
- reviewable but safe documentation choices

### Deliverables

- corrective action plan
- info-security guidance relevant to the repo

### Acceptance criteria

- proposed fixes are not only aesthetic but also publication-safe

### Risks

- over-hardening may remove too much useful technical signal

## M12 - Implement the corrective measures

### Goal

Apply the approved improvements to the repository.

### Scope

- structural fixes
- documentation fixes
- sanitization fixes
- evidence cleanup

### Deliverables

- updated repository
- proof of completed measures

### Acceptance criteria

- the repo reflects the planned corrective actions with visible artifacts

### Risks

- late-stage fixes may create new drift if not tracked carefully

## M13 - Final current-state versus target-state comparison

### Goal

Run one final validation pass before release preparation.

### Scope

- final structure review
- final quality review
- final drift check

### Deliverables

- final comparison note
- residual risks
- go or no-go recommendation

### Acceptance criteria

- the repository is judged against the target state in a concrete, documented way

### Risks

- unresolved minor issues may still require a final polish round

## M14 - Prepare commit and push

### Goal

Package the finished milestone work into a clean terminal-driven git workflow.

### Scope

- review changed files
- organize commit boundaries
- prepare commit messages
- prepare push sequence

### Deliverables

- commit plan
- push-ready repository state

### Acceptance criteria

- the repository changes can be committed and pushed in a disciplined, understandable sequence

### Risks

- poor commit grouping can make the refactor harder to review later

## Recommended execution order

1. `M3`: learn what good looks like
2. `M4`: understand what currently exists
3. `M5`: design the target state from those facts
4. `M6`: create the safety net
5. `M7`: build the structure
6. `M8`: populate it with curated artifacts
7. `M9`: perform the embarrassment and quality pass
8. `M10`: run the drift analysis
9. `M11`: plan corrections and info-security measures
10. `M12`: implement corrections
11. `M13`: do the final target-state comparison
12. `M14`: prepare commit and push

## Planning cadence rule

For active execution, use a rolling three-milestone view:

1. fully specify the next milestone in detail
2. outline the immediately following planned milestone only at a high level
3. outline one fixed fallback milestone for known errors, weak implementation, or cleanup if the active milestone reveals issues

This keeps planning concrete without overcommitting too far ahead.

## Fallback milestone rule

Every actively executed milestone should carry one reserved corrective follow-up milestone.

That fallback milestone is used only if one or more of these appear:

- implementation mistakes
- broken links or paths
- low-quality curation decisions
- weak wording or presentation
- structural regressions
- newly discovered sanitization or publication concerns

If no such issues appear, the fallback milestone can be closed quickly or merged into the next planned milestone.

## Current active planning window

### Detailed next milestone

- `M14` - Prepare commit and push

### Rough next planned milestone

- none currently planned beyond commit and push preparation

### Fixed fallback milestone

- `M14-FIX` - Commit-plan cleanup and packaging correction

## Working interpretation note

Your original list contained two milestones labeled `M8`. To keep the program consistent, this plan interprets:

- `M8` as placeholder replacement and artifact migration
- the second `M8` as `M9` hardening review

All later milestones were shifted by one number accordingly.
