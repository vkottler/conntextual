"""
A module implementing a user interface base application.
"""

# built-in
import logging
import os
from typing import List

# third-party
from runtimepy.net.arbiter import AppInfo
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.logging import TextualHandler
from textual.widgets import Footer, Header

# internal
from conntextual.ui.channel.environment import (
    ChannelEnvironmentDisplay,
    ChannelEnvironmentSource,
)


class Base(App[None]):
    """A simple textual application."""

    app_info: AppInfo
    environments: List[ChannelEnvironmentDisplay]

    def compose_app(self) -> ComposeResult:
        """Application-specific interface creation."""

        yield Header()
        yield Footer()

        yield ScrollableContainer(
            *self.environments, id="channel_environments"
        )

    def dispatch(self) -> None:
        """Update channel values."""

        for env in self.environments:
            env.update_channels()

    def _init_environments(self) -> None:
        """Initialize channel-environment display instances."""

        self.environments = [
            ChannelEnvironmentDisplay.create(
                task.name, task.env, ChannelEnvironmentSource.TASK
            )
            for task in self.app_info.tasks
        ] + [
            ChannelEnvironmentDisplay.create(
                name, conn.env, ChannelEnvironmentSource.CONNECTION_LOCAL
            )
            for name, conn in self.app_info.connections.items()
        ]

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        self._init_environments()
        yield from self.compose_app()

    @staticmethod
    async def create(
        app: AppInfo, handle_debug: bool = True, run: bool = True
    ) -> "Base":
        """Create an application instance."""

        result = Base()
        result.app_info = app

        if handle_debug and app.config["debug"]:
            logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
            os.environ["TEXTUAL"] = "devtools,debug"

        rate: float = app.config["rate"]  # type: ignore
        result.set_interval(1 / rate, result.dispatch)

        if run:
            await result.run_async()

        return result
