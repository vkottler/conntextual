"""
A module implementing user interface elements for channel environments.
"""

# built-in
import random
from typing import Dict, List, Optional, Tuple, Union

# third-party
from rich.text import Text
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment.command import ChannelCommandProcessor
from runtimepy.enum import RuntimeEnum
from runtimepy.net.arbiter import AppInfo
from runtimepy.registry.name import RegistryKey
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalScroll, ScrollableContainer
from textual.coordinate import Coordinate
from textual.widgets import Collapsible, DataTable, Pretty, Static
from vcorelib.logging import LoggerType
from vcorelib.math import to_nanos

# internal
from conntextual.ui.channel.color import bit_field_style, type_str_style
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource, Model
from conntextual.ui.channel.pattern import PatternPair
from conntextual.ui.channel.plot import Plot
from conntextual.ui.channel.selected import SelectedChannel
from conntextual.ui.channel.suggester import CommandSuggester

__all__ = ["ChannelEnvironmentDisplay"]
COLUMNS = ["type", "name", "value"]
DEFAULT_VALUE_COL_WIDTH = 22
STALE_THRESHOLD_NS = to_nanos(0.5)


def css_name(name: str) -> str:
    """Replace some characters that don't work in identifier values."""
    return name.replace(".", "_")


class ChannelEnvironmentDisplay(Static):
    """A channel-environment interface element."""

    model: Model

    by_index: List[Tuple[Coordinate, RegistryKey]]
    channels_by_row: Dict[int, SelectedChannel]

    selected: SelectedChannel
    row_idx: int

    channel_pattern: PatternPair

    def add_channel(
        self, name: str, chan: AnyChannel, enum: Optional[RuntimeEnum]
    ) -> int:
        """Add a channel to the table."""

        table = self.query_one(DataTable)
        env = self.model.env

        self.channels_by_row[self.row_idx] = SelectedChannel.create(
            name, (chan, enum)
        )

        kind_str = str(chan.type)

        # Should handle enums at some point.
        if enum is not None:
            enum_name = env.enums.names.name(enum.id)
            assert enum_name is not None
            kind_str = enum_name

        table.add_row(
            Text(kind_str, style=type_str_style(chan.type, enum)),
            name if not chan.commandable else Text(name, style="bold green"),
            " " * max(len(str(env.value(name))), DEFAULT_VALUE_COL_WIDTH),
        )
        return chan.id

    def add_field(self, name: str) -> None:
        """Add a bit-field row entry."""

        table = self.query_one(DataTable)
        env = self.model.env

        field = env.fields[name]

        table.add_row(
            Text(
                f"{'bit' if field.width == 1 else 'bits'} {field.where_str()}",
                style=bit_field_style(),
            ),
            name if not field.commandable else Text(name, style="bold green"),
            " " * max(len(str(env.value(name))), DEFAULT_VALUE_COL_WIDTH),
        )

    def on_mount(self) -> None:
        """Populate channel table."""

        table = self.query_one(DataTable)
        env = self.model.env
        assert env.finalized
        names = list(env.names)

        # Set up columns.
        table.add_columns(*COLUMNS)
        val_col = COLUMNS.index("value")

        ident: RegistryKey
        for name in names:
            if not self.channel_pattern.matches(name):
                continue

            # Add channel rows.
            chan_result = env.get(name)
            if chan_result is not None:
                chan, enum = chan_result
                ident = self.add_channel(name, chan, enum)

            # Add field and flag rows.
            else:
                self.add_field(name)
                ident = name

            self.by_index.append((Coordinate(self.row_idx, val_col), ident))
            self.row_idx += 1

    def switch_to_channel(self, row: int) -> None:
        """Switch the plot to a channel at the specified row."""

        if row in self.channels_by_row:
            # Select channel.
            self.selected = self.channels_by_row[row]

            # Update plot parameters.
            name = self.selected.name
            self.query_one(Plot).title = name
            self.model.logger.info("Switched plot to channel '%s'.", name)
            self.reset_plot()

    def random_channel(self) -> None:
        """Switch to a random channel."""

        row = -1
        while row not in self.channels_by_row:
            row = random.randint(0, self.row_idx - 1)

        self.switch_to_channel(row)

    def reset_plot(self) -> None:
        """Reset the selected plot."""

        self.selected.reset()
        self.query_one(Plot).set_data(
            self.selected.timestamps, self.selected.values
        )
        self.model.logger.info("Plot reset.")

    @on(DataTable.CellSelected)
    def handle_cell_selected(self, event: DataTable.CellSelected) -> None:
        """Handle input submission."""

        self.switch_to_channel(event.coordinate.row)

    def update_channels(self) -> None:
        """Update all channel values."""

        env = self.model.env
        table = self.query_one(DataTable)

        for coord, chan in self.by_index:
            val = env.value(chan)
            if isinstance(val, float):
                val = f"{val: 15.6f}"
            elif isinstance(val, bool):
                val = "true" if val else "false"
            elif isinstance(val, int):
                val = f"{val: 8d}       "

            # Get the age of the primitive.
            age = env.age_ns(chan)
            if age > STALE_THRESHOLD_NS:
                val = Text(val, style="yellow")  # type: ignore

            table.update_cell_at(coord, val)

        # Update logs.
        self.query_one(ChannelEnvironmentLog).dispatch()

        # Update plot.
        self.selected.poll()
        self.query_one(Plot).dispatch()

    @property
    def label(self) -> str:
        """Obtain a label string for this instance."""
        return f"({self.model.source}) {self.model.name}"

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        with HorizontalScroll(classes="channels"):
            yield DataTable[Union[str, int, float]]()

            yield Plot(
                self.selected.timestamps,
                self.selected.values,
                str(self.model.app.config.get("plot_theme", "pro")),
                str(self.model.app.config.get("plot_marker", "braille")),
                title=self.selected.name,
                id="plot",
            )

        # Create log and command widget.
        log = ChannelEnvironmentLog()
        log.parent_name = self.model.name
        log.logger = self.model.logger
        log.suggester = CommandSuggester.create(self.model.command)
        yield log

        with ScrollableContainer():
            with Collapsible(title="configuration"):
                yield Pretty(self.model.app.config.get("root", {}))

    @staticmethod
    def create(
        name: str,
        command: ChannelCommandProcessor,
        source: ChannelEnvironmentSource,
        logger: LoggerType,
        app: AppInfo,
        channel_pattern: PatternPair,
    ) -> "ChannelEnvironmentDisplay":
        """Create a channel-environment display."""

        result = ChannelEnvironmentDisplay(id=css_name(name))
        result.model = Model(name, command, source, logger, app)
        result.by_index = []
        result.channels_by_row = {}
        result.row_idx = 0
        result.channel_pattern = channel_pattern

        names = list(result.model.env.names)
        assert names

        chan = None
        while chan is None:
            name = random.choice(names)
            chan = result.model.env.get(name)

        result.selected = SelectedChannel.create(name, chan)

        return result
