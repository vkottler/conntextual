"""
A module implementing a user interface base application.
"""

# built-in
import asyncio
import logging
import os

# third-party
from runtimepy.net.arbiter import AppInfo
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.logging import TextualHandler
from textual.widgets import Footer, TabbedContent

# internal
from conntextual.ui.channel.environment import (
    ChannelEnvironmentDisplay,
    ChannelEnvironmentSource,
)
from conntextual.ui.model import Model


class Base(App[None]):
    """A simple textual application."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        Binding("tab", "tab(True)", "Next tab", priority=True),
        Binding("shift+tab", "tab(False)", "Previous tab", priority=True),
    ]

    CSS_PATH = "base.tcss"

    model: Model

    def action_tab(self, forward: bool) -> None:
        """Change the active tab."""

        tabs = self.query_one(TabbedContent)
        curr = tabs.active
        if not curr:
            return

        idx = int(curr.split("-")[1]) - 1

        idx = idx + 1 if forward else idx - 1

        num_tabs = len(self.model.environments)
        if idx >= num_tabs:
            idx -= num_tabs
        if idx < 0:
            idx += num_tabs

        tabs.active = f"tab-{idx + 1}"

    def compose_app(self) -> ComposeResult:
        """Application-specific interface creation."""

        yield Footer()

        with TabbedContent(*(x.label for x in self.model.environments)):
            yield from self.model.environments

    def dispatch(self) -> None:
        """Update channel values."""

        # Handle the stop signal.
        if self.model.app.stop.is_set():
            self.exit()

        loop = asyncio.get_running_loop()
        self.model.uptime.value = loop.time() - self.model.start

        # Only update elements under the active tab.
        tabs = self.query_one(TabbedContent)
        curr = tabs.active
        if not curr:
            return

        with self.model.metrics.measure(
            loop,
            self.model.dispatch_rate,
            self.model.dispatch_time,
            self.model.iter_time,
        ):
            env = self.query_one(
                f"#{self.model.tab_to_id[curr]}",
                expect_type=ChannelEnvironmentDisplay,
            )
            env.update_channels()

    def _init_environments(self) -> None:
        """Initialize channel-environment display instances."""

        # Channels for the UI itself.
        self.model.environments = [
            ChannelEnvironmentDisplay.create(
                "self", self.model.env, ChannelEnvironmentSource.UI
            )
        ]

        # Channels for tasks and connections.
        self.model.environments += [
            ChannelEnvironmentDisplay.create(
                name, task.env, ChannelEnvironmentSource.TASK
            )
            for name, task in self.model.app.tasks.items()
        ] + [
            ChannelEnvironmentDisplay.create(
                name, conn.env, ChannelEnvironmentSource.CONNECTION_LOCAL
            )
            for name, conn in self.model.app.connections.items()
        ]

        # One indexed tabs automatically enumerate for the tabbed environment,
        # keep a mapping of tabs index to element identifier.
        for idx, env in enumerate(self.model.environments):
            self.model.tab_to_id[f"tab-{1 + idx}"] = env.model.name

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        self._init_environments()
        yield from self.compose_app()

    @staticmethod
    def create(app: AppInfo, handle_debug: bool = True) -> "Base":
        """Create an application instance."""

        result = Base()
        result.model = Model.create(app)

        if handle_debug and app.config["debug"]:
            logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
            os.environ["TEXTUAL"] = "devtools,debug"

        rate: float = app.config["rate"]  # type: ignore
        result.set_interval(1 / rate, result.dispatch)

        return result
