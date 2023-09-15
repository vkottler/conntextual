"""
A module implementing a data model for base applications.
"""

# built-in
import asyncio
from dataclasses import dataclass
from typing import List

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.mixins.environment import ChannelEnvironmentMixin
from runtimepy.net.arbiter import AppInfo
from runtimepy.primitives import Bool, Double

# internal
from conntextual.ui.channel.environment import ChannelEnvironmentDisplay


@dataclass
class Model(ChannelEnvironmentMixin):
    """A base application model."""

    app: AppInfo
    env: ChannelEnvironment
    environments: List[ChannelEnvironmentDisplay]

    uptime: Double
    paused: Bool
    start: float

    tab_to_id: dict[str, str]

    @staticmethod
    def create(app: AppInfo, env: ChannelEnvironment) -> "Model":
        """Create a model instance."""

        # Add environment channels.
        result = Model(
            app,
            env,
            [],
            Double(),
            Bool(),
            asyncio.get_running_loop().time(),
            {},
        )
        result.env.channel("uptime", result.uptime)

        return result
