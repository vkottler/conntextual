"""
A module implementing a base application.
"""

# built-in
import asyncio
import curses

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask
from runtimepy.tui.cursor import Cursor
from runtimepy.tui.mixin import CursesWindow


class AppBase(ArbiterTask):
    """A base TUI application."""

    app: AppInfo
    input_queue: asyncio.Queue[int]

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        self.app = app
        self.input_queue = asyncio.Queue()

        cursor = self.cursor

        with self.env.names_pushed("cursor"):
            self.env.channel("x", cursor.x)
            self.env.channel("y", cursor.y)

        with self.env.names_pushed("window"):
            self.env.channel("width", cursor.max_x)
            self.env.channel("height", cursor.max_y)

        self._handle_resize()

    def _handle_resize(self) -> None:
        """Handle the application getting re-sized."""

        self.cursor.poll_max()

    async def handle_char(self, char: int) -> None:
        """Handle user input."""

        if char == curses.KEY_RESIZE:
            self._handle_resize()
        else:  # pragma: nocover
            # trigger this with 'q'
            self.app.stop.set()

        # Handle this at some point.
        # elif char == curses.KEY_MOUSE:
        #     pass

    def draw(self) -> None:
        """Draw the application."""

    async def dispatch(self) -> bool:
        """Dispatch an iteration of this task."""

        window = self.window

        # Check for user input.
        keep_reading = True
        while keep_reading:
            data = window.getch()
            keep_reading = data != -1
            if keep_reading:
                self.input_queue.put_nowait(data)

        # Process inputs.
        while not self.input_queue.empty():
            await self.handle_char(self.input_queue.get_nowait())

        # Update state.
        self.draw()
        window.noutrefresh()
        curses.doupdate()

        return True

    @property
    def cursor(self) -> Cursor:
        """Get this instance's cursor."""
        return self.app.tui.cursor

    @property
    def window(self) -> CursesWindow:
        """Get this instance's window."""
        return self.app.tui.window
