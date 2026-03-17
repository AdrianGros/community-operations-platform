# Renamed Domain Terms

| Source term | Showcase term | Reason |
|---|---|---|
| guild | tenant | Keeps the multi-tenant concept while avoiding chat-platform-specific naming where it is not needed. |
| guild_config | tenant_config | Same reason as above. |
| embed_jobs | scheduled_jobs | Describes the worker pattern without exposing feature-specific naming. |
| discord_role_id | platform_role_id | Keeps the RBAC idea while reducing platform-specific detail in the guard excerpt. |
| verify / public ticket setup labels | omitted from extract | These UI-specific terms add little value to the architecture story. |
| internal project name | Community Operations Platform | Neutral public name for the extract. |
