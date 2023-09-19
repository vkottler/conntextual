"""
A module implementing a data model for channel environments.
"""

# built-in
from dataclasses import dataclass
from enum import StrEnum

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.channel.environment.command import ChannelCommandProcessor
from runtimepy.net.arbiter import AppInfo
from vcorelib.logging import LoggerType


class ChannelEnvironmentSource(StrEnum):
    """Possible sources of channel environments."""

    TASK = "task"
    CONNECTION_LOCAL = "local connection"
    CONNECTION_REMOTE = "remote connection"


@dataclass
class Model:
    """A model for channel environment displays."""

    name: str
    command: ChannelCommandProcessor
    source: ChannelEnvironmentSource
    logger: LoggerType
    app: AppInfo

    @property
    def env(self) -> ChannelEnvironment:
        """Get the channel environment."""
        return self.command.env
