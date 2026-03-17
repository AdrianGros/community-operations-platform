# Corrective Action Plan

Status date: 2026-03-17

## Purpose

This document converts the M10 drift analysis into an implementation-ready corrective plan for M12.

## Action groups

## A1 - Reestablish single source of truth for project narrative

Targets:

- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`
- `RELEASE_NOTES.md`
- `SANITIZATION.md`

Problem:

These root-level files now compete with their canonical project-space versions.

Planned correction:

- reduce the root-level files to short transitional stubs that point to the canonical project-space versions

Why this action matters:

- removes ambiguity without deleting historical context too aggressively
- supports the M5 single-source-of-truth rule

Priority:

High

## A2 - Strengthen the portfolio layer

Targets:

- `portfolio/README.md`

Problem:

The portfolio layer still exists mostly as a placeholder and does not yet help the repository feel like a true multi-project showcase hub.

Planned correction:

- turn `portfolio/README.md` into a substantive positioning page that explains:
  - intended audience
  - how the repository should be reviewed
  - how future projects will fit into the hub

Priority:

Medium

## A3 - Normalize internal planning links

Targets:

- bootstrap plans
- phase reports
- other docs under `docs/`

Problem:

Many internal docs still contain absolute `/opt/...` markdown links.

Planned correction:

- convert internal docs to relative links where practical
- keep literal filesystem paths only when they are operationally relevant, such as the backup archive location in the backup record

Priority:

Medium

## A4 - Clarify extract packaging stance

Targets:

- `projects/community-operations-platform/extracts/index.md`
- related roadmap wording

Problem:

The extract layer is usable, but its long-term packaging stance is still only partially explicit.

Planned correction:

- make it clearer that the current model intentionally references artifacts in place
- note the criteria for any later move or mirroring decision

Priority:

Medium

## A5 - Tighten root navigation further

Targets:

- `README.md`

Problem:

The root README is much better than before, but it still coexists with more historical root material than the target state wants.

Planned correction:

- simplify wording where possible
- strengthen the signal that project-space docs are canonical
- reduce phrasing that sounds overly transitional if no longer needed

Priority:

Medium

## Recommended M12 execution order

1. A1 - single-source-of-truth cleanup
2. A5 - root navigation tightening
3. A2 - portfolio strengthening
4. A3 - internal link normalization
5. A4 - extract packaging clarification

## Deferred actions

The following are intentionally deferred beyond M12 unless scope stays small:

- physically moving runnable app assets
- rewriting git history
- changing GitHub repository settings

## Success criteria for M12

- canonical project-space docs clearly win over root duplicates
- portfolio layer feels intentional, not empty
- internal documentation looks less workstation-bound
- reviewer trust improves through cleaner navigation and fewer conflicting signals
