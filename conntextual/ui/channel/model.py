"""
A module implementing a data model for channel environments.
"""

# built-in
from dataclasses import dataclass
from enum import StrEnum

from runtimepy.channel.environment import ChannelEnvironment

# third-party
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
    env: ChannelEnvironment
    source: ChannelEnvironmentSource
    logger: LoggerType
    app: AppInfo
