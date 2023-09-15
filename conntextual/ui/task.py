"""
A module implementing a TUI application task.
"""

# built-in
from typing import Optional

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask, TaskFactory

# internal
from conntextual.ui.base import Base


class TuiDispatchTask(ArbiterTask):
    """A class implementing a periodic task for a textual TUI."""

    tui: Optional[Base]

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        await super().init(app)
        self.tui = None

    async def dispatch(self) -> bool:
        """Dispatch an iteration of this task."""

        if self.tui is not None:
            self.tui.dispatch()

        return True


class TuiDispatch(TaskFactory[TuiDispatchTask]):
    """A factory for the TUI dispatch task."""

    kind = TuiDispatchTask
