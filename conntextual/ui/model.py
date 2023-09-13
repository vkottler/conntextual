"""
A module implementing a data model for base applications.
"""

# built-in
import asyncio
from dataclasses import dataclass
from typing import List

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.metrics import PeriodicTaskMetrics
from runtimepy.mixins.environment import ChannelEnvironmentMixin
from runtimepy.net.arbiter import AppInfo
from runtimepy.primitives import Bool, Double
from vcorelib.math import MovingAverage, RateTracker

# internal
from conntextual.ui.channel.environment import ChannelEnvironmentDisplay


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
    paused: Bool
    start: float

    tab_to_id: dict[str, str]

    @staticmethod
    def create(app: AppInfo) -> "Model":
        """Create a model instance."""

        # Add environment channels.
        result = Model(
            app,
            ChannelEnvironment(),
            [],
            PeriodicTaskMetrics.create(),
            RateTracker(),
            MovingAverage(),
            Double(),
            Double(),
            Bool(),
            asyncio.get_running_loop().time(),
            {},
        )

        # Add channels.
        result.register_task_metrics(result.metrics)
        result.env.channel("uptime", result.uptime)
        result.env.channel("paused", result.paused, commandable=True)

        return result
