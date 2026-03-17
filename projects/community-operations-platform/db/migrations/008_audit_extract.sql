CREATE TABLE IF NOT EXISTS audit_event (
  id BIGSERIAL PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  actor_user_id BIGINT NULL,
  action TEXT NOT NULL,
  payload JSONB NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_event_tenant_created_at
  ON audit_event (tenant_id, created_at DESC);
