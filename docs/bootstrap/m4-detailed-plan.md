# M4 Detailed Plan

Status date: 2026-03-17

## Milestone

M4 - Produce a robust current-state inventory

## Why this milestone exists

Before we can define the final target repository design in M5, we need a reliable inventory of what currently exists in the repository, how it is grouped, where ambiguity or duplication already exists, and which artifacts are strong enough to preserve.

This milestone is the factual baseline for later migration and hardening work.

## Main goal

Create a documented current-state map of the repository that is specific enough to support target-state planning, artifact migration, and drift analysis.

## Key questions

1. Which files and folders currently define the real repository?
2. Which parts are legacy runnable app assets versus new canonical showcase structure?
3. Which artifacts are documentation, evidence, code, config, or migration support?
4. Where are the current reviewer entrypoints and where do they compete?
5. Which obvious structural weaknesses should influence M5?

## Scope

- top-level repository inventory
- artifact classification
- reviewer entrypoint analysis
- duplication and ambiguity analysis
- migration relevance assessment

## Out of scope

- final target-state decisions
- moving files into new destinations
- deleting legacy paths
- full hardening or sanitization remediation

## Source policy

Use the repository as the primary source of truth.

The milestone should rely on direct file-system inspection and existing repo documents, not on memory.

## Expected outputs

1. A current-state inventory document
2. A classification of major artifact groups
3. A list of structural strengths worth preserving
4. A list of weaknesses and ambiguities that M5 must resolve

## Acceptance criteria

- the inventory distinguishes canonical-new versus legacy-root structure
- major artifacts are classified by purpose
- reviewer entrypoints and structure conflicts are documented
- M5 can use the result directly without re-inventorying the repo

## Risks

- missing hidden or low-visibility artifacts
- confusing temporary scaffolding with final canonical structure
- underestimating the importance of older root-level documents

## Planned execution steps

1. Inspect the repository tree and exclude obvious non-source runtime directories.
2. Group current files into artifact families.
3. Identify current reviewer entrypoints.
4. Record strengths, weaknesses, duplication, and ambiguity.
5. Map major artifact groups to likely target-state categories without making final migration decisions.

## Planned artifacts

- `docs/inventory/current-state-inventory.md`
- `docs/bootstrap/m4-detailed-plan.md`
- `docs/bootstrap/m4-phase-report.md`

## Definition of done

M4 is done when the repo contains a clear, reviewable inventory document that explains the current state well enough to guide M5 target-state planning.

## Next planned milestone after M4

M5 - Plan the target repository using M3 and M4

High-level intent:

- define the target-state structure precisely
- assign current artifacts to canonical destinations
- specify migration rules and reviewer paths

## Fixed fallback milestone if M4 reveals issues

M4-FIX - Inventory correction and artifact classification cleanup

Trigger conditions:

- important artifacts were missed
- classifications are inconsistent or misleading
- key legacy versus canonical boundaries remain unclear
