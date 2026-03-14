from __future__ import annotations

from typing import Any


async def build_health_snapshot(app_state: object) -> dict[str, Any]:
    db_status = await app_state.services.health_service.check_connection()
    schema_status = await app_state.services.health_service.get_runtime_schema_compatibility()
    migration_status = await app_state.services.health_service.get_schema_version()
    cache_summary = app_state.services.tenant_config_service.cache_summary()

    return {
        "db_ok": bool(db_status.get("ok")),
        "db_latency_ms": db_status.get("latency_ms"),
        "db_error": db_status.get("error"),
        "schema_ok": bool(schema_status.get("schema_ok")),
        "schema_missing": list(schema_status.get("missing", [])),
        "latest_migration": migration_status.get("latest_version"),
        "migration_count": migration_status.get("count"),
        "config_cache": cache_summary,
    }
