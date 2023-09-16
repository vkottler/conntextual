"""
A module implementing a TUI application task.
"""

# built-in
import asyncio

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask, TaskFactory

# internal
from conntextual.ui.base import Base


class TuiDispatchTask(ArbiterTask):
    """A class implementing a periodic task for a textual TUI."""

    tui: Base
    tui_task: asyncio.Task[None]

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        await super().init(app)
        self.tui = Base.create(app, self.env)

        # Create application task.
        self.tui_task = asyncio.create_task(
            self.tui.run_async(
                headless=app.config.get("headless", False),  # type: ignore
            )
        )

        # Wait for the application to be composed.
        await self.tui.composed.wait()

    async def dispatch(self) -> bool:
        """Dispatch an iteration of this task."""

        self.tui.dispatch()
        return True

    async def stop_extra(self) -> None:
        """Extra actions to perform when this task is stopping."""

        # Ensure that the app task is awaited.
        self.tui.exit()
        await self.tui_task


class TuiDispatch(TaskFactory[TuiDispatchTask]):
    """A factory for the TUI dispatch task."""

    kind = TuiDispatchTask
