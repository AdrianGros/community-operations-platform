from __future__ import annotations

from dataclasses import dataclass

from app.state import AppState, Repositories, Services


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    database_url: str
    primary_tenant_id: int | None

    @property
    def is_dev(self) -> bool:
        return self.environment == "dev"


async def build_app_state(pool: object, bot: object, settings: Settings) -> AppState:
    repos = Repositories(
        audit_repo=object(),
        tenant_config_repo=object(),
        membership_repo=object(),
        session_repo=object(),
        session_reminder_repo=object(),
        scheduled_message_repo=object(),
    )

    services = Services(
        audit_service=object(),
        tenant_config_service=object(),
        health_service=object(),
        reminder_service=object(),
        error_notify_service=object(),
    )

    # Shared dependencies are created once and attached to the bot root.
    # That keeps command handlers thin and avoids ad-hoc repository wiring.
    app_state = AppState(pool=pool, repos=repos, services=services)
    setattr(bot, "app_state", app_state)

    if settings.is_dev and settings.primary_tenant_id is not None:
        setattr(bot, "command_sync_mode", "tenant_only")
    else:
        setattr(bot, "command_sync_mode", "global")

    return app_state
