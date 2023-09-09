"""
An application module for curses testing.
"""

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.tui.mixin import CursesWindow

# internal
from conntextual.curses.base import AppBase


class Testing(AppBase):
    """A simple test application."""

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        await super().init(app)

        # more stuff

    def draw(self, window: CursesWindow) -> None:
        """Draw the application."""

        self.cursor.reset()

        can_continue = True

        idx = 0
        while can_continue:
            window.addstr(str(idx))

            window.addch("\u2588")
            window.addch("\u2591")
            window.addch("\u2592")
            window.addch("\u25A0")

            window.clrtoeol()
            can_continue = self.cursor.inc_y()
            idx += 1
