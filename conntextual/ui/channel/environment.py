"""
A module implementing user interface elements for channel environments.
"""

# built-in
from typing import Dict, List, Tuple, Union

# third-party
from rich.text import Text
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.net.arbiter import AppInfo
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalScroll, ScrollableContainer
from textual.coordinate import Coordinate
from textual.widgets import DataTable, Pretty, Static
from vcorelib.logging import LoggerType
from vcorelib.math import to_nanos

# internal
from conntextual.ui.channel.color import type_str_style
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource, Model
from conntextual.ui.channel.plot import Plot
from conntextual.ui.channel.selected import SelectedChannel
from conntextual.ui.channel.suggester import CommandSuggester

__all__ = ["ChannelEnvironmentDisplay"]
COLUMNS = ["id", "type", "name", "value"]
DEFAULT_VALUE_COL_WIDTH = 25
STALE_THRESHOLD_NS = to_nanos(0.5)


def css_name(name: str) -> str:
    """Replace some characters that don't work in identifier values."""
    return name.replace(".", "_")


class ChannelEnvironmentDisplay(Static):
    """A channel-environment interface element."""

    model: Model

    by_index: List[Tuple[Coordinate, AnyChannel]]
    channels_by_row: Dict[int, SelectedChannel]

    selected: SelectedChannel

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
            self.channels_by_row[row_idx] = SelectedChannel.create(
                name, (chan, enum)
            )
            row_idx += 1

    def switch_to_channel(self, row: int) -> None:
        """Switch the plot to a channel at the specified row."""

        # Select channel.
        self.selected = self.channels_by_row[row]

        # Update plot parameters.
        name = self.selected.name
        self.query_one(Plot).title = name
        self.model.logger.info("Switched plot to channel '%s'.", name)
        self.reset_plot()

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
                title=self.selected.name,
                id="plot",
            )

        # Create log and command widget.
        log = ChannelEnvironmentLog()
        log.parent_name = self.model.name
        log.logger = self.model.logger
        log.suggester = CommandSuggester.create(self.model.env, log.logger)
        yield log

        with ScrollableContainer():
            yield Pretty(self.model.app.config.get("root", {}))

    @staticmethod
    def create(
        name: str,
        env: ChannelEnvironment,
        source: ChannelEnvironmentSource,
        logger: LoggerType,
        app: AppInfo,
    ) -> "ChannelEnvironmentDisplay":
        """Create a channel-environment display."""

        result = ChannelEnvironmentDisplay(id=css_name(name))
        result.model = Model(name, env, source, logger, app)
        result.by_index = []
        result.channels_by_row = {}

        first_name = next(env.names)
        result.selected = SelectedChannel.create(first_name, env[first_name])

        return result
