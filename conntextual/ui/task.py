"""
A module implementing a TUI application task.
"""

# built-in
import asyncio

# third-party
import psutil
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask, TaskFactory

# internal
from conntextual.ui.base import Base


class TuiDispatchTask(ArbiterTask):
    """A class implementing a periodic task for a textual TUI."""

    tui: Base
    tui_task: asyncio.Task[None]
    process: psutil.Process

    def _add_housekeeping_metrics(self) -> None:
        """Initialize housekeeping metrics."""

        with self.env.names_pushed("system"):
            self.env.float_channel("memory_percent")
            self.env.float_channel("cpu_percent")

        self.process = psutil.Process()

    def poll_housekeeping(self) -> None:
        """Update housekeeping metrics."""

        self.env.set("system.memory_percent", psutil.virtual_memory().percent)

        with self.process.oneshot():
            self.env.set("system.cpu_percent", self.process.cpu_percent())

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        await super().init(app)
        self.tui = Base.create(app, self.env)

        self._add_housekeeping_metrics()

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

        self.poll_housekeeping()
        self.tui.dispatch()

        return True

    async def stop_extra(self) -> None:
        """Extra actions to perform when this task is stopping."""

        # Ensure that the app task is awaited.
        await self.tui.action_quit()
        await self.tui_task


class TuiDispatch(TaskFactory[TuiDispatchTask]):
    """A factory for the TUI dispatch task."""

    kind = TuiDispatchTask
