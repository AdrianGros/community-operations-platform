from __future__ import annotations

import asyncio
import logging

log = logging.getLogger(__name__)


class SessionReminderLoop:
    def __init__(self, bot: object) -> None:
        self.bot = bot
        self._task: asyncio.Task[None] | None = None
        self._schema_drift_warned = False

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run(), name="session-reminder-loop")

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            self._task = None

    async def _run(self) -> None:
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                reminder_service = self.bot.app_state.services.reminder_service
                processed = await reminder_service.run_due_reminders(bot=self.bot)
                self._schema_drift_warned = False
                if processed > 0:
                    log.info("Session reminder loop processed=%s", processed)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                error_type = exc.__class__.__name__
                if error_type in {"UndefinedTableError", "UndefinedColumnError"}:
                    if not self._schema_drift_warned:
                        log.warning("Reminder loop paused due to schema drift: %s", error_type)
                        self._schema_drift_warned = True
                    await asyncio.sleep(300)
                    continue
                log.exception("Session reminder loop failed")
            await asyncio.sleep(60)
