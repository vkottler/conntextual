"""
A module implementing some useful mocks.
"""

# built-in
import curses
from os import environ
from sys import platform


def wrapper_mock(*args, **kwargs) -> None:
    """Create a virtual window."""

    # Set some environment variables if they're not set.
    if platform in ["linux", "darwin"]:
        if "TERM" not in environ:
            environ["TERM"] = "linux"
        if "TERMINFO" not in environ:
            environ["TERMINFO"] = "/etc/terminfo"

    # Initialize the library (else curses won't work at all).
    getattr(curses, "initscr")()  # curses.initscr()
    getattr(curses, "start_color")()  # curses.start_color()

    # Send a re-size event.
    # curses.ungetch(curses.KEY_RESIZE)
    getattr(curses, "ungetch")(getattr(curses, "KEY_RESIZE"))

    # Create a virtual window for the application to use.
    window = getattr(curses, "newwin")(24, 80)  # curses.newwin(24, 80)

    args[0](window, *args[1:], **kwargs)
