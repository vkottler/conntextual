"""
A module implementing user interface elements for channel environments.
"""

# built-in
from typing import List, Tuple, Union

# third-party
from rich.text import Text
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment import ChannelEnvironment
from textual.app import ComposeResult
from textual.coordinate import Coordinate
from textual.widgets import DataTable, Static
from vcorelib.logging import LoggerType

# internal
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource, Model
from conntextual.ui.channel.suggester import CommandSuggester

__all__ = ["ChannelEnvironmentDisplay"]
COLUMNS = ["id", "type", "name", "value"]


class ChannelEnvironmentDisplay(Static):
    """A channel-environment interface element."""

    model: Model

    by_index: List[Tuple[Coordinate, AnyChannel]]

    def on_mount(self) -> None:
        """Populate channel table."""

        table = self.query_one(DataTable)
        env = self.model.env
        names = list(env.names)

        # Set up columns.
        table.add_columns(*COLUMNS)
        value_column: int = COLUMNS.index("value")

        row_idx = 0

        for name in names:
            chan, enum = env[name]

            kind_str = str(chan.type)

            # Should handle enums at some point.
            if enum is not None:
                enum_name = env.enums.names.name(enum.id)
                assert enum_name is not None
                kind_str = enum_name

            table.add_row(
                chan.id,
                kind_str,
                name
                if not chan.commandable
                else Text(name, style="bold green"),
                env.value(chan.id),
            )
            self.by_index.append((Coordinate(row_idx, value_column), chan))
            row_idx += 1

    def update_channels(self) -> None:
        """Update all channel values."""

        env = self.model.env
        table = self.query_one(DataTable)

        for coord, chan in self.by_index:
            val = env.value(chan.id)
            if isinstance(val, float):
                val = f"{val:.3f}"
            table.update_cell_at(coord, val)

        # Update logs.
        self.query_one(ChannelEnvironmentLog).dispatch()

    @property
    def label(self) -> str:
        """Obtain a label string for this instance."""
        return f"({self.model.source}) {self.model.name}"

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        yield DataTable[Union[str, int, float]](
            fixed_columns=len(COLUMNS), classes="channels"
        )

        # Create log and command widget.
        log = ChannelEnvironmentLog()
        log.parent_name = self.model.name
        log.logger = self.model.logger
        log.suggester = CommandSuggester.create(self.model.env, log.logger)
        yield log

        # yield Placeholder("util (under construction)", classes="util")

    @staticmethod
    def create(
        name: str,
        env: ChannelEnvironment,
        source: ChannelEnvironmentSource,
        logger: LoggerType,
    ) -> "ChannelEnvironmentDisplay":
        """Create a channel-environment display."""

        result = ChannelEnvironmentDisplay(id=name)
        result.model = Model(name, env, source, logger)
        result.by_index = []
        return result
