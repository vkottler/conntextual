"""
A module impementing a channel-environment log widget.
"""

# built-in
from logging import Logger, LoggerAdapter, LogRecord
from logging.handlers import QueueHandler
from queue import SimpleQueue
from typing import Tuple

# third-party
from textual.app import ComposeResult
from textual.widgets import Log, Static
from vcorelib.logging import LoggerType

LogRecordQueue = SimpleQueue[LogRecord]


def queue_handler(
    logger: LoggerType,
    queue: LogRecordQueue = None,
    handler: QueueHandler = None,
    root_formatter: bool = True,
) -> Tuple[LogRecordQueue, QueueHandler]:
    """
    Set up and return a simple queue and logging queue handler. Use the
    provided objects if they already exist.
    """

    if queue is None:
        queue = SimpleQueue()
    if handler is None:
        handler = QueueHandler(queue)

        # Initialize the handler if it should be tied to the root logger.
        if root_formatter:
            handler.setFormatter(Logger.root.handlers[0].formatter)

        if isinstance(logger, LoggerAdapter):
            logger = logger.logger

        assert isinstance(logger, Logger)
        logger.addHandler(handler)

    return queue, handler


class ChannelEnvironmentLog(Static):
    """A channel-environment log widget."""

    logger: LoggerType
    queue: LogRecordQueue

    def dispatch(self) -> None:
        """Dispatch the log updater."""

        log = self.query_one(Log)
        while not self.queue.empty():
            log.write_line(self.queue.get_nowait().getMessage())

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        # Initialize logger handling.
        self.queue, _ = queue_handler(self.logger)
        self.logger.info("Queue handler initialized.")

        yield Log(classes="log")

        yield Static("input bar")
