CREATE TABLE IF NOT EXISTS scheduled_jobs (
  id BIGSERIAL PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  target_channel_id BIGINT NOT NULL,
  mode TEXT NOT NULL CHECK (mode IN ('once', 'repeat')),
  schedule_json JSONB NOT NULL,
  next_run_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'sent', 'failed', 'cancelled')),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_by_user_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  claimed_by TEXT NULL,
  claimed_at TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS idx_scheduled_jobs_due_pending
  ON scheduled_jobs (tenant_id, next_run_at)
  WHERE status IN ('pending', 'processing') AND enabled = TRUE;

CREATE INDEX IF NOT EXISTS idx_scheduled_jobs_claimed_at
  ON scheduled_jobs (claimed_at);
