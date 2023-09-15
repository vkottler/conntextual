"""
A module implementing a user interface base application.
"""

# built-in
import asyncio
from contextlib import suppress
import logging
import os
from pathlib import Path

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.net.arbiter import AppInfo
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.keys import Keys
from textual.logging import TextualHandler
from textual.widgets import Input, TabbedContent

# internal
from conntextual.ui.channel.environment import ChannelEnvironmentDisplay
from conntextual.ui.channel.model import ChannelEnvironmentSource
from conntextual.ui.footer import CustomFooter
from conntextual.ui.model import Model

TCSS_ROOT = Path(__file__).parent.parent.joinpath("data", "tcss")


class Base(App[None]):
    """A simple textual application."""

    BINDINGS = [
        ("q", "quit"),
        (Keys.Escape, "quit", "(or q) quit"),
        ("space", "toggle_pause", "toggle pause"),
        ("d", "toggle_dark", "toggle dark mode"),
        ("g", "screenshot", "take a screenshot"),
        Binding(Keys.Tab, "tab(True)", "Next tab", priority=True),
        Binding(Keys.BackTab, "tab(False)", "Previous tab", priority=True),
    ]

    CSS_PATH = TCSS_ROOT.joinpath("base.tcss")

    model: Model

    def action_toggle_pause(self) -> None:
        """Toggle pause state."""
        self.model.paused.toggle()

    def action_tab(self, forward: bool) -> None:
        """Change the active tab."""

        tabs = self.query_one(TabbedContent)
        curr = tabs.active
        if not curr:
            return

        # Accept an input box suggestion if an input box is highlighted.
        focus = self.focused
        if forward and focus is not None and isinstance(focus, Input):
            focus.action_cursor_right()
            return

        idx = int(curr.split("-")[1]) - 1

        idx = idx + 1 if forward else idx - 1

        num_tabs = len(self.model.environments)
        if idx >= num_tabs:
            idx -= num_tabs
        if idx < 0:
            idx += num_tabs

        tabs.active = f"tab-{idx + 1}"

        # Update footer.
        footer = self.query_one(CustomFooter)
        footer.current_tab = self.model.environments[idx].label
        footer.refresh()

    def compose_app(self) -> ComposeResult:
        """Application-specific interface creation."""

        footer = CustomFooter()
        footer.current_tab = self.model.environments[0].label
        yield footer

        with TabbedContent(*(x.model.name for x in self.model.environments)):
            yield from self.model.environments

    def dispatch(self) -> None:
        """Update channel values."""

        # Handle the stop signal.
        if self.model.app.stop.is_set():
            self.exit()

        loop = asyncio.get_running_loop()
        self.model.uptime.value = loop.time() - self.model.start

        if not self.model.paused:
            # Only update elements under the active tab.
            tabs = self.query_one(TabbedContent)
            curr = tabs.active
            if not curr:
                return

            with suppress(NoMatches):
                env = self.query_one(
                    f"#{self.model.tab_to_id[curr]}",
                    expect_type=ChannelEnvironmentDisplay,
                )
                env.update_channels()

    def _init_environments(self) -> None:
        """Initialize channel-environment display instances."""

        # Channels for tasks and connections.
        self.model.environments += [
            ChannelEnvironmentDisplay.create(
                name, task.env, ChannelEnvironmentSource.TASK, task.logger
            )
            for name, task in self.model.app.tasks.items()
        ] + [
            ChannelEnvironmentDisplay.create(
                name,
                conn.env,
                ChannelEnvironmentSource.CONNECTION_LOCAL,
                conn.logger,
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
    def create(
        app: AppInfo, env: ChannelEnvironment, handle_debug: bool = True
    ) -> "Base":
        """Create an application instance."""

        if handle_debug and app.config.get("debug"):
            logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
            os.environ["TEXTUAL"] = "devtools,debug"

        result = Base()
        result.model = Model.create(app, env)

        return result
