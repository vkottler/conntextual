"""
A module impementing a channel-environment log widget.
"""

from textual.app import ComposeResult

# third-party
from textual.widgets import Log, Static


class ChannelEnvironmentLog(Static):
    """A channel-environment log widget."""

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        log = Log(classes="log")
        for i in range(100):
            log.write_line(f"Hello, world! {i}")

        yield log

        yield Static("input bar")
