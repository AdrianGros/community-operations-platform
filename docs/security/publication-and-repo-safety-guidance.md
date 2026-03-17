# Publication and Repo Safety Guidance

Status date: 2026-03-17

## Purpose

This note captures the publication-safety and repository-security practices most relevant to the current showcase refactor.

Primary sources are official GitHub Docs.

## Source set

- GitHub Docs: Removing sensitive data from a repository
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- GitHub Docs: About secret scanning
  - https://docs.github.com/code-security/secret-scanning/about-secret-scanning
- GitHub Docs: Enabling secret scanning for your repository
  - https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enabling-secret-scanning-for-your-repository
- GitHub Docs: Enabling secret scanning features
  - https://docs.github.com/code-security/secret-scanning/configuring-secret-scanning-for-your-repositories
- GitHub Docs: Ignoring files
  - https://docs.github.com/en/get-started/git-basics/ignoring-files
- GitHub Docs: Best practices for preventing data leaks in your organization
  - https://docs.github.com/en/enterprise-server%403.15/code-security/tutorials/secure-your-organization/best-practices-for-preventing-data-leaks-in-your-organization

## Guidance relevant to this repository

## 1. Prefer prevention over cleanup

GitHub's guidance on sensitive-data removal makes two important points:

- revoke or rotate exposed secrets first
- rewriting history has significant side effects and should be treated carefully

Implication for this repo:

- for normal cleanup work, we should avoid creating exposures in the first place
- if a secret is ever committed, immediate credential rotation matters more than aesthetic history cleanup
- history rewriting should not be used casually during this refactor

## 2. Public repositories benefit from secret scanning

GitHub documents that secret scanning runs automatically for free on public repositories, and push protection can be enabled to block pushes that contain secrets.

Implication for this repo:

- if this repository is or becomes public, secret scanning should be enabled or verified
- if push protection is available for the repo context, it should be enabled

Note:

These are GitHub-side settings and are not implemented from this local workspace.

## 3. `.gitignore` and local excludes are part of publication safety

GitHub documents both repository `.gitignore` use and local-only exclusion via `.git/info/exclude`.

Implication for this repo:

- repository `.gitignore` should keep shared local-runtime artifacts out of version control
- local-only editor or machine artifacts can be handled in `.git/info/exclude` if they should not be shared
- if a file is already tracked, ignoring it later requires untracking it first

## 4. Avoid exposing local filesystem assumptions

While not a secret leak in itself, workstation-specific paths in reviewer-facing docs reduce portability and can expose environment details unnecessarily.

Implication for this repo:

- prefer relative links in Markdown
- keep literal local paths only where operational records require them, such as the backup record

## 5. Publication-safe curation should minimize unnecessary operational detail

The GitHub guidance on preventing data leaks reinforces a conservative approach:

- remove sensitive data if exposed
- use repository hygiene to prevent accidental publication
- prefer safer review and commit habits

Implication for this repo:

- keep environment files, runtime reports, and host-specific material excluded
- maintain the current extract-first and sanitization-first curation posture
- do not add deployment or infrastructure artifacts unless they provide clear public review value and can be safely generalized

## M12 recommendations

For the next implementation milestone, the most relevant safety actions are:

1. keep root cleanup non-destructive and narrative-focused
2. do not rewrite history as part of normal cleanup
3. preserve `.gitignore` discipline
4. continue removing workstation-specific paths from Markdown where they are not operationally necessary
5. preserve sanitization and excluded-artifact notes as part of the public review package

## Residual operational recommendation

Outside this local refactor workflow, verify on GitHub that:

- secret scanning is active for the repository context
- push protection is enabled if available

These are platform settings rather than repository-file changes.
