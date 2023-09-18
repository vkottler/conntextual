"""
A module implementing a user interface base application.
"""

# built-in
import asyncio
from contextlib import suppress
import logging
import os
from pathlib import Path
from typing import Optional

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
        ("r", "refresh_plot", "refresh plot"),
        ("R", "random_channel", "plot random channel"),
        Binding(Keys.Tab, "tab(True)", "Next tab", priority=True),
        Binding(Keys.BackTab, "tab(False)", "Previous tab", priority=True),
    ]

    CSS_PATH = TCSS_ROOT.joinpath("base.tcss")

    model: Model
    composed: asyncio.Event

    def action_toggle_pause(self) -> None:
        """Toggle pause state."""
        self.model.paused.toggle()

    def action_tab(self, forward: bool) -> None:
        """Change the active tab."""

        tabs = self.tabs
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

        with TabbedContent(
            *(x.model.name for x in self.model.environments), classes="tabs"
        ):
            yield from self.model.environments

    @property
    def tabs(self) -> TabbedContent:
        """Get the tab container."""
        return self.query_one(".tabs", expect_type=TabbedContent)

    def dispatch(self) -> None:
        """Update channel values."""

        self.model.uptime.value = (
            asyncio.get_running_loop().time() - self.model.start
        )

        if not self.model.paused:
            env = self.current_channel_environment
            if env is not None:
                env.update_channels()

    @property
    def current_channel_environment(
        self,
    ) -> Optional[ChannelEnvironmentDisplay]:
        """Get the current channel-environment display."""

        env = None

        with suppress(NoMatches):
            curr = self.tabs.active
            if curr:
                env = self.query_one(
                    f"#{self.model.tab_to_id[curr]}",
                    expect_type=ChannelEnvironmentDisplay,
                )

        return env

    def action_random_channel(self) -> None:
        """Randomize the channel on the current tab."""

        env = self.current_channel_environment
        if env is not None:
            env.random_channel()

    def action_refresh_plot(self) -> None:
        """Refresh the current plot."""

        env = self.current_channel_environment
        if env is not None:
            env.reset_plot()

    def _init_environments(self) -> None:
        """Initialize channel-environment display instances."""

        # Channels for tasks and connections.
        self.model.environments += [
            ChannelEnvironmentDisplay.create(
                name,
                task.env,
                ChannelEnvironmentSource.TASK,
                task.logger,
                self.model.app,
            )
            for name, task in self.model.app.tasks.items()
        ] + [
            ChannelEnvironmentDisplay.create(
                name,
                conn.env,
                ChannelEnvironmentSource.CONNECTION_LOCAL,
                conn.logger,
                self.model.app,
            )
            for name, conn in self.model.app.connections.items()
        ]

        # One indexed tabs automatically enumerate for the tabbed environment,
        # keep a mapping of tabs index to element identifier.
        for idx, env in enumerate(self.model.environments):
            assert env.id is not None
            self.model.tab_to_id[f"tab-{1 + idx}"] = env.id

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        self._init_environments()
        yield from self.compose_app()
        self.composed.set()

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
        result.composed = asyncio.Event()

        return result

    async def action_quit(self) -> None:
        """Stop the rest of the application when quitting."""
        await super().action_quit()
        self.model.app.stop.set()
