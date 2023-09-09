"""
A module implementing a curses-based user interface.
"""

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import TaskFactory

# internal
from conntextual.curses.testing import Testing
from conntextual.curses.tui import Tui


class TuiApp(TaskFactory[Tui]):
    """A TUI application factory."""

    kind = Tui


class TestApp(TaskFactory[Testing]):
    """A TUI application factory."""

    kind = Testing


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    del app

    return 0
