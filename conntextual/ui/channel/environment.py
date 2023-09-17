"""
A module implementing user interface elements for channel environments.
"""

# built-in
from typing import List, Optional, Tuple, Union

# third-party
import numpy as np
from rich.text import Text
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.enum import RuntimeEnum
from runtimepy.primitives.type import AnyPrimitiveType
from textual._color_constants import COLOR_NAME_TO_RGB
from textual.app import ComposeResult
from textual.color import Color
from textual.containers import HorizontalScroll
from textual.coordinate import Coordinate
from textual.widgets import DataTable, Placeholder, Static
from vcorelib.logging import LoggerType

# internal
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource, Model
from conntextual.ui.channel.plot import Plot
from conntextual.ui.channel.suggester import CommandSuggester

__all__ = ["ChannelEnvironmentDisplay"]
COLUMNS = ["id", "type", "name", "value"]
DEFAULT_VALUE_COL_WIDTH = 25
STALE_THRESHOLD_NS = 500000000


def type_str_style(kind: AnyPrimitiveType, enum: Optional[RuntimeEnum]) -> str:
    """Get a style for a given type."""

    result = ""

    if kind.is_boolean:
        result = Color(*COLOR_NAME_TO_RGB["ansi_bright_cyan"]).hex
    elif kind.is_float:
        result = Color(*COLOR_NAME_TO_RGB["indigo"]).hex
    else:
        result = Color(*COLOR_NAME_TO_RGB["purple"]).hex

    if enum is not None:
        result += " bold"

    return result


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
                Text(kind_str, style=type_str_style(chan.type, enum)),
                name
                if not chan.commandable
                else Text(name, style="bold green"),
                " "
                * max(len(str(env.value(chan.id))), DEFAULT_VALUE_COL_WIDTH),
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
                val = f"{val: 15.6f}"
            elif isinstance(val, bool):
                val = "true" if val else "false"
            elif isinstance(val, int):
                val = f"{val: 8d}       "

            # Get the age of the primitive.
            age = env[chan.id][0].raw.age_ns()
            if age > STALE_THRESHOLD_NS:
                val = Text(val, style="yellow")  # type: ignore

            table.update_cell_at(coord, val)

        # Update logs.
        self.query_one(ChannelEnvironmentLog).dispatch()

        self.query_one(Plot).shift_data()

    @property
    def label(self) -> str:
        """Obtain a label string for this instance."""
        return f"({self.model.source}) {self.model.name}"

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        with HorizontalScroll(classes="channels"):
            yield DataTable[Union[str, int, float]]()

            # change this out for something else
            x = np.linspace(0, 2 * np.pi, 100)
            yield Plot(x, np.sin(x), id="plot")

        # Create log and command widget.
        log = ChannelEnvironmentLog()
        log.parent_name = self.model.name
        log.logger = self.model.logger
        log.suggester = CommandSuggester.create(self.model.env, log.logger)
        yield log

        yield Placeholder("util (under construction)", classes="util")

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
