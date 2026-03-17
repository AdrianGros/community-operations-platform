# GitHub Best Practices Research

Status date: 2026-03-17

## Purpose

This document captures current GitHub-native best practices that matter for a curated showcase repository and portfolio presentation.

Primary sources are official GitHub Docs.

## Source set

- GitHub Docs: About the repository README file
  - https://docs.github.com/articles/about-readmes/
- GitHub Docs: About your profile
  - https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile
- GitHub Docs: Managing your profile README
  - https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
- GitHub Docs: Pinning items to your profile
  - https://docs.github.com/articles/pinning-repositories-to-your-profile
- GitHub Docs: Creating a template repository
  - https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository

## Stable GitHub rules we should adopt

## 1. The repository README is the primary landing artifact

GitHub states that the README is often the first thing a visitor sees in a repository.

Practical rule for this repo:

- the root README must explain what this repo is
- it must explain why the repo exists
- it must explain how a reviewer should navigate it
- it must not assume prior context

Recommended root README questions:

- What is this repository?
- Why is it worth looking at?
- Where should a reviewer start?
- Which folders are canonical?
- Which parts are legacy or transitional?

## 2. README placement matters

GitHub recognizes and surfaces READMEs from `.github/`, repository root, and `docs/`.
If more than one README exists, GitHub prefers `.github/`, then root, then `docs/`.

Implication for this repo:

- the root README should remain the main landing page
- project-specific READMEs should live inside their project folders
- we should avoid competing top-level README narratives in multiple locations

## 3. Root README should stay concise and navigational

GitHub recommends a README for essential project information, while longer documentation belongs elsewhere.

Implication for this repo:

- keep the root README short enough to scan quickly
- move deeper explanation into `docs/`, `portfolio/`, and `projects/`
- use links, not walls of text, to guide the reviewer journey

## 4. Relative links are the safer internal linking standard

GitHub recommends relative links for linking to files within the repository.

Implication for this repo:

- internal Markdown navigation should prefer relative links
- absolute GitHub URLs should be reserved for external sharing contexts
- migration work should update links as paths change

## 5. The GitHub profile is part of the portfolio story

GitHub describes the profile page as the place where people tell the story of their work through shared information, contributions, and showcased projects.

Implication for your portfolio strategy:

- the repository should be designed to be pinnable
- the repository name, description, and README opening should make sense from the profile page
- the repository should complement a profile README, not duplicate it blindly

## 6. Profile README is a routing layer, not a dump

GitHub supports a profile README through a public repository named exactly like the username.

Implication for your portfolio strategy:

- your profile README should route visitors to the most important repositories
- the detailed repository narrative should stay in the repository itself
- the profile should connect projects into one coherent story

## 7. Pins are a deliberate showcase mechanism

GitHub allows up to six pinned repositories or gists on the profile.

Implication for your portfolio strategy:

- we should think in terms of a small set of flagship repos
- this repo should be designed as one of those flagship pins if it represents the showcase hub
- pin order should support your intended narrative, not just popularity

## 8. Reusable repo structure can later become a template

GitHub supports template repositories for repeating the same structure, branches, and files.

Implication for this repo:

- our `projects/` conventions should be explicit and repeatable
- if the curation approach works, it could later evolve into a reusable project template

## Recommended practices for this repository

## Root-level practices

- use the root README as the canonical landing page
- keep the root README focused on navigation, structure, and positioning
- clearly mark canonical versus legacy paths during migration
- avoid large historical explanations in the root README

## Project-level practices

- give each project one canonical folder under `projects/`
- give each project a dedicated README
- separate overview, extracts, evidence, and roadmap content
- make it obvious which artifacts are runnable and which are curated extracts

## Portfolio-level practices

- use `portfolio/` for cross-project narrative and reviewer guidance
- align repo presentation with profile README and pinned repo strategy
- treat the repo as a curated experience, not a raw dump of engineering history

## Anti-patterns to avoid

- multiple competing descriptions of what the repository is
- overlong root README files that bury navigation
- placeholders that persist without migration plans
- root-level clutter that makes the repo look historically accumulated
- mixing repo-governance docs with project-facing narrative without clear boundaries
- assuming profile visitors already understand the context

## Decisions this research supports

The current direction remains valid:

- `docs/` should hold repo-level planning and architecture
- `portfolio/` should hold cross-project narrative
- `projects/` should be the canonical home for curated project content
- the root README should function as a reviewer entrypoint, not as a full documentation dump

## M5 design impact

When we reach target-state planning in M5, the design should explicitly account for:

- one clear root landing page
- one canonical project folder per showcased project
- stable internal relative linking
- a profile and pin strategy that supports the repo's role as a flagship showcase

## Open questions for later milestones

- should this repo become the primary pinned showcase repo, or should an even higher-level hub play that role?
- which existing artifacts deserve to stay at root during migration, and which should move immediately?
- do we eventually want a template for adding future showcased projects?
