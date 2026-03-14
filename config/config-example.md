# Config Example

The original project loads its runtime configuration from environment variables.

Example placeholder set:

```env
ENVIRONMENT=prod
DISCORD_BOT_TOKEN=REDACTED
POSTGRES_CONNECTION_STRING=REDACTED
PRIMARY_TENANT_ID_PLACEHOLDER=0
INSTANCE_ID_PLACEHOLDER=community-ops-platform-1
ALLOW_DB_MIGRATION=false
MIGRATE_ON_STARTUP=false
```

Notes:

- runtime governance lives in the database, not in this file
- production secrets are intentionally not represented here beyond placeholder names
