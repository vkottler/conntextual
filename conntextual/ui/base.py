"""
A module implementing a user interface base application.
"""

# built-in
from typing import List

# third-party
from runtimepy.net.arbiter import AppInfo
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
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

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        yield Header()
        yield Footer()

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

        yield ScrollableContainer(
            *self.environments, id="channel_environments"
        )

    def update(self) -> None:
        """Update channel values."""

        for env in self.environments:
            env.update_channels()

    @staticmethod
    def create(app: AppInfo) -> "Base":
        """Create an application instance."""

        result = Base()
        result.app_info = app

        rate: float = app.config["rate"]  # type: ignore
        result.set_interval(1 / rate, result.update)

        return result
