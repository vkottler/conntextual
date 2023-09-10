"""
A module implementing user interface elements for channel environments.
"""

# built-in
from dataclasses import dataclass
from enum import StrEnum
from typing import List, Tuple, Union

# third-party
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment import ChannelEnvironment
from textual.app import ComposeResult
from textual.coordinate import Coordinate
from textual.widgets import DataTable, Static

# internal
from conntextual.ui.channel.log import ChannelEnvironmentLog


class ChannelEnvironmentSource(StrEnum):
    """Possible sources of channel environments."""

    UI = "ui"
    TASK = "task"
    CONNECTION_LOCAL = "local connection"
    CONNECTION_REMOTE = "remote connection"


class ChannelEnvironmentDisplay(Static):
    """A channel-environment interface element."""

    @dataclass
    class Model:
        """A model for channel environment displays."""

        name: str
        env: ChannelEnvironment
        source: ChannelEnvironmentSource

    model: Model

    by_index: List[Tuple[Coordinate, AnyChannel]]

    def on_mount(self) -> None:
        """Populate channel table."""

        table = self.query_one(DataTable)
        env = self.model.env
        names = list(env.names)

        # Set up columns.
        table.add_columns("id", "type", "name", "value")
        value_column = 3

        row_idx = 0

        for name in names:
            chan, enum = env[name]

            kind_str = str(chan.type)

            # Should handle enums at some point.
            del enum
            # if enum is not None:
            #     enum_name = env.enums.names.name(enum.id)
            #     assert enum_name is not None
            #     kind_str = enum_name

            table.add_row(chan.id, kind_str, name, env.value(chan.id))
            self.by_index.append((Coordinate(row_idx, value_column), chan))
            row_idx += 1

    def update_channels(self) -> None:
        """Update all channel values."""

        env = self.model.env
        table = self.query_one(DataTable)

        for coord, chan in self.by_index:
            table.update_cell_at(coord, env.value(chan.id))

    @property
    def label(self) -> str:
        """Obtain a label string for this instance."""
        return f"{self.model.source} - {self.model.name}"

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        # this should go in a container
        yield DataTable[Union[str, int, float]](classes="channels")

        yield Static("plot", classes="plot")

        yield ChannelEnvironmentLog()

        yield Static("util", classes="util")

    @staticmethod
    def create(
        name: str, env: ChannelEnvironment, source: ChannelEnvironmentSource
    ) -> "ChannelEnvironmentDisplay":
        """Create a channel-environment display."""

        result = ChannelEnvironmentDisplay()
        result.model = ChannelEnvironmentDisplay.Model(name, env, source)
        result.by_index = []
        return result
