# DAD-M Metrics Plan

Status date: 2026-03-17

## Purpose

This document defines which DAD-M effectiveness metrics should be measured in future runs and which data should already be collected now even if formal measurement is implemented later.

The goal is not vanity metrics.

The goal is to make DAD-M effectiveness observable across:

- delivery control
- artifact quality
- rework
- reviewability
- safety

## Measurement principles

- prefer metrics that can be collected from repo artifacts and milestone logs
- distinguish process health from output quality
- avoid metrics that reward paperwork for its own sake
- pair quantitative metrics with a small number of qualitative judgments

## Metric groups

## 1. Flow control metrics

These measure whether DAD-M actually improved execution discipline.

Suggested metrics:

- milestone completion rate
- milestone cycle time
- average time from detailed plan to deploy completion
- fix-milestone rate
- percentage of milestones completed without reopening

Why it matters:

- shows whether the framework reduces drift and rework

## 2. Artifact production metrics

These measure whether DAD-M creates useful, reviewable outputs.

Suggested metrics:

- number of milestone artifacts created
- percentage of milestones with both detailed plan and phase report
- proof coverage rate
- ratio of planned artifacts to delivered artifacts

Why it matters:

- shows whether the process produces reviewable evidence instead of only chat discussion

## 3. Change-quality metrics

These measure how cleanly milestones translate into repository improvements.

Suggested metrics:

- number of navigation issues fixed
- number of duplicate-authority documents reduced
- broken-link count before and after hardening
- number of absolute local-path links removed
- drift-gap count before and after corrective implementation

Why it matters:

- directly measures structural and documentation improvement

## 4. Rework and drift metrics

These measure whether DAD-M reduces late surprises.

Suggested metrics:

- count of unintended drift findings per milestone
- count of corrective actions caused by missed earlier decisions
- ratio of intentional transitional states to unintended drift
- count of residual risks after each monitor phase

Why it matters:

- shows whether the phased model is actually containing uncertainty

## 5. Safety and publication metrics

These measure whether the repo becomes safer to publish and easier to review.

Suggested metrics:

- count of sensitive-path or workstation-specific references in reviewer-facing docs
- count of publication-risk artifacts excluded or redirected
- count of root-level docs reduced to canonical stubs
- `.gitignore` coverage for known local artifacts

Why it matters:

- reflects information-hygiene quality, not just structure quality

## 6. Reviewability metrics

These measure whether another person can actually navigate and assess the work.

Suggested metrics:

- number of clear reviewer entrypoints
- average click depth from root README to project evidence or extracts
- presence of canonical project landing page
- qualitative reviewer clarity score

Why it matters:

- DAD-M should improve not just internal control, but external comprehensibility

## Recommended qualitative ratings

Use a simple `1-5` score after each major milestone for:

- clarity of current state
- clarity of target state
- confidence in next step
- confidence in publication safety
- reviewer navigability

## Data we should collect now

Even before formal automation, these fields should be logged for each milestone:

- milestone id
- milestone title
- start date
- end date
- status
- fix milestone triggered: yes/no
- number of files changed
- number of artifacts created
- proof types produced
- main residual risks
- main drift items
- main corrective actions created

## Suggested future logging format

Recommended file:

- `docs/method/dadm-metrics-log.csv`

Suggested columns:

```text
milestone_id,milestone_title,start_date,end_date,status,fix_triggered,files_changed_count,artifacts_created_count,proof_count,residual_risk_count,drift_gap_count,corrective_action_count,reviewer_clarity_score,publication_safety_score
```

## Metrics that are already partially recoverable from this project

The current project already contains enough data to backfill some metrics later:

- milestone count
- detailed plan count
- phase report count
- fix milestone usage
- drift-gap categories
- corrective action groups

## Metrics that are not reliably recoverable without explicit logging

- exact milestone cycle time
- exact prompt count
- exact human review time
- exact number of defects discovered per phase in real time

## Practical next step

Do not block current repo work on metric automation.

Instead:

1. add a lightweight milestone metrics log later
2. backfill only the high-confidence fields from existing artifacts
3. start collecting fresh metrics prospectively from the next DAD-M project or the next major repo cycle
