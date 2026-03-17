# Showcase Information Architecture

## Intent

The repository should evolve from "one app extract with supporting files" into "one curated showcase hub with multiple project spaces".

## Canonical top-level layout

```text
community-operations-platform-showcase/
  docs/
    bootstrap/
    architecture/
  portfolio/
  projects/
    community-operations-platform/
      app/
      bot/
      config/
      db/
      tests/
      requirements.txt
      pytest.ini
      overview/
      extracts/
      evidence/
      roadmap/
```

## Structural rules

### Root

The root should answer three questions quickly:

1. What is this repository?
2. How should a reviewer navigate it?
3. Which parts are canonical versus legacy-in-transition?

### `docs/`

This folder holds repository-wide planning, architecture, operating rules, and migration decisions.

### `portfolio/`

This folder is for cross-project narrative:

- positioning
- audience fit
- curation rules
- future project index pages

### `projects/`

Every showcased project gets one canonical folder here. Over time, reviewers should be able to ignore the legacy root and navigate primarily through `projects/`.

### Project subfolders

Use a stable split:

- project-local runtime and source assets
- `overview/` for project narrative, architecture summary, and reviewer entry docs
- `extracts/` for curated code or non-runnable source packages
- `evidence/` for proof artifacts and relevance notes
- `roadmap/` for project-specific migration or enhancement plans

## Migration strategy

Use staged migration:

1. Establish the canonical structure.
2. Route new documentation into canonical folders immediately.
3. Migrate project-local runtime and source assets into the project folder when the reviewer path is stable.
4. Remove or archive legacy root paths only after links, runs, and review flow are stable.

## Single source of truth rule

For every planning or narrative topic, there should be one canonical file path. Redirect from old locations if needed, but avoid parallel "latest" descriptions in multiple places.
