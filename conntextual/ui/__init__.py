"""
A module implementing a basic user interface.
"""

# built-in
from asyncio import gather, sleep
from dataclasses import dataclass

# third-party
from runtimepy.net.arbiter import AppInfo

# internal
from conntextual.ui.base import Base
from conntextual.ui.channel.environment import ChannelEnvironmentDisplay
from conntextual.ui.channel.log import ChannelEnvironmentLog
from conntextual.ui.channel.model import ChannelEnvironmentSource

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


@dataclass
class MockEvent:
    """A mock event class."""

    value: str


async def test(tui: Base) -> None:
    """Test the UI."""

    await sleep(0.05)

    iterations = 2 * len(tui.model.environments)

    # Cycle through tabs.
    for direction in [True, False]:
        for _ in range(iterations):
            tui.action_tab(direction)
            await sleep(0.05)

    # Send some commands.
    for command in ["test"]:
        for env in tui.model.environments:
            env.query_one(ChannelEnvironmentLog).handle_submit(
                MockEvent(command)  # type: ignore
            )
            await sleep(0.05)

    tui.model.app.stop.set()


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    tui = Base.create(app)

    tasks = [
        tui.run_async(
            headless=app.config.get("headless", False),  # type: ignore
        ),
    ]

    if "test" in app.config and app.config["test"]:
        tasks.append(test(tui))

    await gather(*tasks)

    return 0
