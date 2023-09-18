"""
A module impementing a channel-environment log widget.
"""

# built-in
from logging import ERROR, INFO, Formatter, Logger
from typing import Optional

# third-party
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Input, Log, Static
from vcorelib.logging import (
    DEFAULT_TIME_FORMAT,
    LoggerType,
    LogRecordQueue,
    queue_handler,
)

# internal
from conntextual.ui.channel.suggester import CommandSuggester

MAX_LINES = 1000


class InputWithHistory(Input):
    """An input with last-command history."""

    BINDINGS = [Binding("up", "previous_command", "previous command")]

    previous: str

    def action_previous_command(self) -> None:
        """Go back to the previous command."""

        if self.previous:
            self.value = self.previous
            self.action_end()
            self.refresh()


class ChannelEnvironmentLog(Static):
    """A channel-environment log widget."""

    parent_name: str
    logger: LoggerType
    queue: LogRecordQueue
    suggester: Optional[CommandSuggester]

    def dispatch(self) -> None:
        """Dispatch the log updater."""

        log = self.query_one(Log)
        while not self.queue.empty():
            log.write_line(self.queue.get_nowait().getMessage())

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        """Handle input submission."""

        self.query_one(InputWithHistory).previous = event.value
        assert self.suggester is not None
        result = self.suggester.processor.command(event.value)

        self.logger.log(
            INFO if result else ERROR, "%s: %s", event.value, result
        )

        # Reset input.
        node = self.query_one(Input)
        node.action_home()
        node.action_delete_right_all()

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        # Initialize logger handling.
        self.queue, handler = queue_handler(self.logger, root_formatter=False)
        handler.setFormatter(Formatter(DEFAULT_TIME_FORMAT))
        if self.logger is not Logger.root:
            self.logger.info("Queue handler initialized.")

        if self.suggester is not None:
            input_box = InputWithHistory(
                "set ",
                classes="command_input",
                suggester=self.suggester,
                id=f"{self.parent_name}-input",
            )
            input_box.previous = ""
            yield input_box

        yield Log(classes="log", max_lines=MAX_LINES)
