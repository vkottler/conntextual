"""
A module implementing a basic user interface.
"""

# built-in
from asyncio import sleep

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


async def stop_after(app: AppInfo) -> int:
    """Run a textual application."""

    if "stop_after" in app.config:
        duration: float = app.config["stop_after"]  # type: ignore
        app.logger.info("Starting %f sleep.", duration)
        await sleep(duration)
        app.stop.set()
        app.logger.info("Set stop signal.")

    return 0


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    await Base.create(app)
    return 0
