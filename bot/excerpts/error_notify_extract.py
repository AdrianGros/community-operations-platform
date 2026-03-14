from __future__ import annotations

import time
from datetime import UTC, datetime


class ErrorNotifyService:
    def __init__(self, *, bot: object, tenant_config_service: object, audit_service: object | None) -> None:
        self.bot = bot
        self.tenant_config_service = tenant_config_service
        self.audit_service = audit_service
        self._last_notify_at: dict[int, float] = {}

    async def notify_critical_error(
        self,
        tenant_id: int,
        *,
        title: str,
        details: str,
        exception: Exception | None = None,
        domain: str | None = None,
        action: str | None = None,
        correlation_id: str | None = None,
    ) -> bool:
        config = await self.tenant_config_service.load_error_notification_config(tenant_id)

        enabled = bool(config.get("enabled"))
        channel_id = config.get("channel_id")
        cooldown = max(1, int(config.get("cooldown_seconds") or 60))
        if not enabled or channel_id is None:
            return False

        now_mono = time.monotonic()
        last_sent = self._last_notify_at.get(tenant_id)
        if last_sent is not None and (now_mono - last_sent) < cooldown:
            return False

        lines = [
            f"domain/action: `{domain or '-'} / {action or '-'}`",
            f"tenant_id: `{tenant_id}`",
            f"timestamp: `{datetime.now(tz=UTC).isoformat()}`",
            f"correlation_id: `{correlation_id or f'{tenant_id}-{int(now_mono * 1000)}'}`",
            f"details: {details}",
            f"exception: `{exception.__class__.__name__}: {exception}`" if exception else "exception: `-`",
        ]

        channel = await self.bot.resolve_channel(channel_id)
        await channel.send("\n".join(lines))
        self._last_notify_at[tenant_id] = now_mono

        if self.audit_service is not None:
            await self.audit_service.log_event(
                tenant_id=tenant_id,
                actor_user_id=None,
                action="critical_error.notified",
                payload={"domain": domain, "action": action, "channel_id": channel_id},
            )

        return True
