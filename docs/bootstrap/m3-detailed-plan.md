# M3 Detailed Plan

Status date: 2026-03-17

## Milestone

M3 - Research best practices for GitHub documentation and portfolio presentation

## Why this milestone exists

Before we restructure the repository further, we need an evidence-based view of how GitHub itself presents repositories and profiles, and which documentation patterns support reviewer navigation best.

This milestone is intentionally research-first. It should reduce taste-driven decisions in later structure and migration work.

## Main goal

Extract practical GitHub documentation and portfolio presentation patterns that can directly shape the target repository design for `community-operations-platform-showcase`.

## Key research questions

1. What must a repository README answer first for a reviewer landing on the repo?
2. How should a profile and pinned repositories support the repo narrative?
3. What should live in the root README versus project-level READMEs?
4. Which GitHub-native features can improve consistency and reuse?
5. Which anti-patterns make a showcase repo look cluttered, confusing, or unfinished?

## Scope

- GitHub repository README guidance
- GitHub profile README usage
- pinned repository usage on the profile page
- repository templates as a repeatable curation mechanism
- implications for a multi-project showcase repository

## Out of scope

- direct implementation of the final target structure
- full artifact migration
- final wording polish for all repository documents

## Source policy

Use official GitHub documentation as the primary source base for this milestone.

If later we want external examples from public portfolios, they should be treated as secondary inspiration, not as the rule source.

## Research findings to capture

### Repository README baseline

The root README should clearly explain:

- what the project does
- why it is useful
- how someone gets started
- where to get help
- who maintains or contributes

For GitHub repository visitors, README placement matters. GitHub surfaces a README from `.github/`, then the repository root, then `docs/`.

### Profile and portfolio presentation baseline

GitHub profiles are designed to tell the story of your work through profile information, a profile README, contributions, and pinned repositories.

Pinned repositories are a first-class reviewer-navigation tool because GitHub lets you feature up to six repositories or gists on the profile page.

### Reuse and standardization baseline

GitHub template repositories are useful if we later want repeatable project onboarding with the same structure and files.

For this repository, that means our eventual `projects/` conventions could later be turned into a template or reusable project intake pattern.

## Expected outputs

1. A concise best-practice summary document
2. A list of structure rules we will adopt for this repo
3. A list of anti-patterns we will avoid
4. A short decision note describing how M3 influences M5 target-state planning

## Acceptance criteria

- the findings are based on current official GitHub docs
- the outputs are specific enough to change our repo design decisions
- at least one concrete recommendation exists for:
  - root README structure
  - project-level README structure
  - profile and pin strategy
  - reusable repo patterns

## Risks

- collecting facts without converting them into design rules
- overfitting to GitHub mechanics and ignoring our repo's actual content
- mistaking profile optimization for repository clarity

## Planned execution steps

1. Gather current official GitHub documentation relevant to repository READMEs, profile READMEs, pinned repositories, and templates.
2. Extract stable platform-supported patterns from those docs.
3. Translate those patterns into repository curation rules for this showcase.
4. Record anti-patterns and open questions.
5. Hand off the result as design input to M4 and M5.

## Planned artifacts

- `docs/research/github-best-practices.md`
- update note in `docs/bootstrap/milestones.md` if milestone status changes

## Current progress

Research is complete and the official-doc-based findings were captured in:

- [`docs/research/github-best-practices.md`](../research/github-best-practices.md)

## Completion status

M3 is complete.

The milestone produced an evidence-based rule set for:

- root README design
- project-level README design
- portfolio positioning
- internal link strategy
- profile and pinned-repo implications
- future template and reuse considerations

## Definition of done

M3 is done when the repo contains a reusable research artifact that clearly explains which GitHub documentation and portfolio practices we will adopt, and why.

## Next planned milestone after M3

M4 - Produce a robust current-state inventory

High-level intent:

- inventory current files and folders
- classify artifacts by target destination
- detect duplication, ambiguity, and clutter

## Fixed fallback milestone if M3 reveals issues

M3-FIX - Research correction and decision hygiene

Trigger conditions:

- weak or conflicting research findings
- outdated or non-actionable recommendations
- repo decisions based on assumptions instead of evidence

High-level intent:

- correct the research base
- remove weak conclusions
- tighten the rule set before M4 proceeds
