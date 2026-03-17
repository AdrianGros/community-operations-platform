ALTER TABLE tenant_config
  ADD COLUMN IF NOT EXISTS read_only_enabled BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE tenant_config
  ADD COLUMN IF NOT EXISTS feature_flags JSONB NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE tenant_config
  ADD COLUMN IF NOT EXISTS critical_error_channel_id BIGINT NULL;

ALTER TABLE tenant_config
  ADD COLUMN IF NOT EXISTS critical_error_notify_enabled BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE tenant_config
  ADD COLUMN IF NOT EXISTS critical_error_notify_cooldown_seconds INT NOT NULL DEFAULT 60;
