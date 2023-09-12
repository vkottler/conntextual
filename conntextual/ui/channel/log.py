"""
A module impementing a channel-environment log widget.
"""

# built-in
from logging import ERROR, INFO, Formatter, Logger

# third-party
from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Log, Static
from vcorelib.logging import LoggerType, LogRecordQueue, queue_handler

# internal
from conntextual.ui.channel.suggester import CommandSuggester

MAX_LINES = 1000
DEFAULT_FORMAT = Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ChannelEnvironmentLog(Static):
    """A channel-environment log widget."""

    logger: LoggerType
    queue: LogRecordQueue
    suggester: CommandSuggester

    def dispatch(self) -> None:
        """Dispatch the log updater."""

        log = self.query_one(Log)
        while not self.queue.empty():
            log.write_line(self.queue.get_nowait().getMessage())

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        """Handle input submission."""

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
        handler.setFormatter(DEFAULT_FORMAT)
        if self.logger is not Logger.root:
            self.logger.info("Queue handler initialized.")

        yield Log(classes="log", max_lines=MAX_LINES)

        yield Input("set ", classes="command_input", suggester=self.suggester)
