# Backup Record

Status date: 2026-03-17

This file records the current repository backup created in milestone M6.

## Backup artifact

- archive: `/tmp/community-operations-platform-showcase-backups/community-operations-platform-showcase_20260317_193029Z.tar.gz`
- checksum file: `/tmp/community-operations-platform-showcase-backups/community-operations-platform-showcase_20260317_193029Z.tar.gz.sha256`
- size: `376K`

## Source state

- repository path: `/opt/community-operations-platform-showcase`
- git `HEAD`: `5170244`
- working tree note: backup includes uncommitted planning and refactor documents present at backup time

## Inclusion rules

Included:

- repository working tree
- `.git/`
- tracked files
- untracked planning and showcase-structure files

Excluded:

- `.venv/`
- `.pytest_cache/`
- `var/`
- `__pycache__/`

## Verification

- sha256: `6b208217daeaaf269a1d7dc2e2e14720c89eae153879a7bb5c07196fd29c4778`
- archive listing was checked successfully

## Restore note

Example restore flow:

```bash
mkdir -p /tmp/restore-community-operations-platform-showcase
tar -C /tmp/restore-community-operations-platform-showcase -xzf /tmp/community-operations-platform-showcase-backups/community-operations-platform-showcase_20260317_193029Z.tar.gz
```

After extraction, the repository content will be available under:

```text
/tmp/restore-community-operations-platform-showcase/community-operations-platform-showcase
```

## Constraint note

The backup was written to `/tmp` because this environment did not allow creating a new backup directory under `/opt/backups` or `/opt` top level during execution.

For local long-term retention outside this session, the archive should later be copied to a durable backup location.
