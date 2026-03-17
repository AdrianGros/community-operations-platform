# Sanitization Notes

This extract was built with an extract-first approach.

Rules applied here:

- excerpts are preferred over full file copies
- new documentation is preferred over sanitized production docs
- runtime and business logic are kept, environment-specific details are removed
- if a value or term looked risky and did not improve the technical story, it was dropped

Generalization rules used in this directory:

- real IDs became typed placeholders
- internal project and community names were replaced with neutral names
- infrastructure references were removed instead of softened
- user-facing command names with community fingerprinting value were excluded when they were not needed for the architecture story

The list of renamed domain terms lives in `renamed-domain-terms.md`.
The list of excluded source areas lives in `excluded-artifacts.md`.
