"""
A module implementing a curses-based user interface.
"""

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import TaskFactory

# internal
from conntextual.curses.base import AppBase
from conntextual.curses.tui import Tui


class TuiApp(TaskFactory[Tui]):
    """A TUI application factory."""

    kind = Tui


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    apps = list(app.search_tasks(AppBase))
    del apps

    return 0
