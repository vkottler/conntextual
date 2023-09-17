"""
A module implementing user interface elements for channel environments.
"""

# built-in
from typing import Dict

# third-party
import numpy as np
from runtimepy.channel.environment import ChannelEnvironment
from textual.app import ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.widgets import Placeholder, Static
from vcorelib.logging import LoggerType

# internal
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource, Model
from conntextual.ui.channel.plot import Plot
from conntextual.ui.channel.suggester import CommandSuggester
from conntextual.ui.channel.table import ChannelRow, ChannelTable

__all__ = ["ChannelEnvironmentDisplay"]


class ChannelList(Static):
    """A channel list widget."""

    model: Model
    table: ChannelTable
    values: Dict[ChannelRow, Static]

    def compute_grid(self) -> None:
        """Set grid parameters."""

        self.styles.grid_size_rows = self.table.height
        self.styles.grid_size_columns = len(self.table.columns)
        self.styles.grid_columns = [
            self.table.id_width + 1,
            self.table.type_width + 1,
            self.table.name_width + 1,
            self.table.value_width + 1,
        ]

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        self.compute_grid()

        for label in self.table.columns:
            yield Static(label)

        for row in self.table.rows:
            yield Static(str(row.identifier))
            yield Static(row.kind_str(self.table.env))
            yield Static(row.name)

            value = Static(row.value_str(), classes="value")
            self.values[row] = value
            yield value

    @staticmethod
    def create(model: Model, **kwargs) -> "ChannelList":
        """Create a channel list."""

        result = ChannelList(**kwargs)
        result.model = model
        result.table = ChannelTable(model.env)
        result.values = {}
        return result

    def update_channels(self) -> None:
        """Update all channel values."""

        self.table.update_values()

        for row, value in self.values.items():
            curr = value.renderable
            new = row.value_str()

            if curr != new:
                value.renderable = row.value_str()
                value.refresh()


class ChannelEnvironmentDisplay(Static):
    """A channel-environment interface element."""

    model: Model

    def update_channels(self) -> None:
        """Update all channel values."""

        self.query_one(ChannelList).update_channels()
        self.query_one(ChannelEnvironmentLog).dispatch()
        self.query_one(Plot).shift_data()

    @property
    def label(self) -> str:
        """Obtain a label string for this instance."""
        return f"({self.model.source}) {self.model.name}"

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        with HorizontalScroll(classes="channels"):
            with VerticalScroll(classes="list-container"):
                yield ChannelList.create(self.model)

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
        return result
