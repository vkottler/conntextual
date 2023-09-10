"""
A module implementing a user interface base application.
"""

# built-in
import asyncio
from dataclasses import dataclass
import logging
import os
from pathlib import Path
from typing import List

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.metrics import PeriodicTaskMetrics
from runtimepy.mixins.environment import ChannelEnvironmentMixin
from runtimepy.net.arbiter import AppInfo
from runtimepy.primitives import Double
from textual.app import App, ComposeResult
from textual.logging import TextualHandler
from textual.widgets import Footer, TabbedContent
from vcorelib.math import MovingAverage, RateTracker

# internal
from conntextual.ui.channel.environment import (
    ChannelEnvironmentDisplay,
    ChannelEnvironmentSource,
)


class Base(App[None]):
    """A simple textual application."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    CSS_PATH = "base.tcss"

    @dataclass
    class Model(ChannelEnvironmentMixin):
        """A base application model."""

        app: AppInfo
        env: ChannelEnvironment
        environments: List[ChannelEnvironmentDisplay]

        metrics: PeriodicTaskMetrics
        dispatch_rate: RateTracker
        dispatch_time: MovingAverage

        iter_time: Double
        uptime: Double
        start: float

        @staticmethod
        def create(app: AppInfo) -> "Base.Model":
            """Create a model instance."""

            # Add environment channels.
            result = Base.Model(
                app,
                ChannelEnvironment(),
                [],
                PeriodicTaskMetrics.create(),
                RateTracker(),
                MovingAverage(),
                Double(),
                Double(),
                asyncio.get_running_loop().time(),
            )
            result.register_task_metrics(result.metrics)
            result.env.channel("uptime", result.uptime)

            return result

    model: Model

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

        with self.model.metrics.measure(
            loop,
            self.model.dispatch_rate,
            self.model.dispatch_time,
            self.model.iter_time,
        ):
            for env in self.model.environments:
                env.update_channels()

    def _init_environments(self) -> None:
        """Initialize channel-environment display instances."""

        # Add channels to UI environment.

        self.model.environments = [
            ChannelEnvironmentDisplay.create(
                "self", self.model.env, ChannelEnvironmentSource.UI
            )
        ]

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

    def compose(self) -> ComposeResult:
        """Create child nodes."""

        self._init_environments()
        yield from self.compose_app()

    @staticmethod
    async def create(
        app: AppInfo,
        handle_debug: bool = True,
        run: bool = True,
    ) -> "Base":
        """Create an application instance."""

        result = Base()
        result.model = Base.Model.create(app)

        if handle_debug and app.config["debug"]:
            logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
            os.environ["TEXTUAL"] = "devtools,debug"

        rate: float = app.config["rate"]  # type: ignore
        result.set_interval(1 / rate, result.dispatch)

        if run:
            await result.run_async(
                headless=app.config.get("headless", False),  # type: ignore
            )

        return result
