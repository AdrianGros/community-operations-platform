# DAD-M Prompt Log

Status date: 2026-03-17

## Purpose

This document records the prompt structure used in this project and preserves the reusable milestone prompt shape.

It distinguishes between:

- the framework starter prompt basis
- the project-adapted milestone prompt template
- the specific prompt fields that were repeatedly used

## Framework starter prompt basis

The local `dadm-framework` bootstrap reference provided this structure:

- role
- goal
- core rules
- start with:
  - project brief
  - safety boundaries
  - milestone plan
  - working mode
  - discover for the first milestone

## Project-adapted milestone prompt template

This is the reusable prompt structure that was effectively used for milestones in this repository:

```text
ROLE
You are a project and process AI and work strictly by DAD-M.
You keep Discover, Apply, Deploy, and Monitor separate.

PROJECT
Community Operations Platform Showcase Hub

MILESTONE
<milestone id and title>

MILESTONE GOAL
<goal>

WORKING RULES
1. Keep Discover, Apply, Deploy, and Monitor separate.
2. Discover collects facts and constraints.
3. Apply turns facts into a plan.
4. Deploy implements only the approved plan.
5. Monitor validates the result and decides whether a fix milestone is needed.

SAFETY BOUNDARIES
<allowed and off-limits scope>

DISCOVER TASKS
<inventory / research / analysis tasks>

APPLY TASKS
<design / decision tasks>

DEPLOY TASKS
<implementation or artifact-creation tasks>

MONITOR TASKS
<validation and follow-up decision tasks>

ACCEPTANCE CRITERIA
<done conditions>

RISKS
<known risks>

EXPECTED ARTIFACTS
<files or proofs>

NEXT PLANNED MILESTONE
<rough next milestone>

FIX MILESTONE IF NEEDED
<fallback milestone>
```

## Prompt fields actually used in this project

The following fields were consistently present in milestone planning:

- role
- project
- milestone
- milestone goal
- working rules
- safety boundaries or scope boundaries
- discover tasks
- apply tasks
- deploy tasks
- monitor tasks
- acceptance criteria
- risks
- expected artifacts
- next planned milestone
- fix milestone if needed

## Prompting style actually used

Observed project-specific prompt style:

- one milestone in full detail
- one following milestone only at high level
- one fixed corrective fallback milestone
- implementation paired with repo-local documentation
- monitor verdict always recorded explicitly

## Verbatim prompt preservation status

What is preserved exactly:

- the framework starter prompt basis from `dadm-framework`
- the project-adapted M3-style milestone prompt structure documented during execution

What is reconstructed from project artifacts:

- the repeated milestone prompt skeleton used across M4-M12

Reason:

The project recorded milestone plans and phase reports rigorously, but not every live chat prompt was stored verbatim from the first step onward.

## Recommended improvement

For future DAD-M work, store prompt instances as first-class artifacts per milestone, for example:

- `docs/prompts/m3.md`
- `docs/prompts/m4.md`
- `docs/prompts/m5.md`

That would make later process evaluation much stronger.
