"""
A module implementing a basic TUI application.
"""

# third-party
from runtimepy.channel.environment.command import ENVIRONMENTS

# internal
from conntextual.curses.base import AppBase


class Tui(AppBase):
    """A simple TUI application."""

    def _handle_resize(self) -> None:
        """Handle the application getting re-sized."""

        super()._handle_resize()
        self.cursor.reset()

        # Draw tabs.
        # self.tabs = self.window.derwin(
        #     3, self.env.value("window.width"), 0, 0
        # )
        # self.tabs.border()
        # need a cursor for this thing

        # self.tabs.addstr(1, 1, "test")

    def draw(self) -> None:
        """Draw the application."""

        self.cursor.reset()

        window = self.window

        for env_name, env in ENVIRONMENTS.items():
            window.addstr(f"========== {env_name} ==========")
            window.clrtoeol()
            if not self.cursor.inc_y():
                break

            for name in env.env.names:
                line = name

                chan, enum = env.env[name]

                # do floats better
                line += " " + str(chan)

                # Handle enum at some point.
                del enum
                # if enum is not None:
                #     pass

                window.addstr(line)
                window.clrtoeol()
                if not self.cursor.inc_y():
                    break
