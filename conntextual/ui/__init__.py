"""
A module implementing a basic user interface.
"""

# third-party
from runtimepy.net.arbiter import AppInfo

# internal
from conntextual.ui.base import Base
from conntextual.ui.channel.environment import (
    ChannelEnvironmentDisplay,
    ChannelEnvironmentSource,
)

__all__ = [
    "Base",
    "run",
    "ChannelEnvironmentDisplay",
    "ChannelEnvironmentSource",
]


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    await Base.create(app)
    return 0
