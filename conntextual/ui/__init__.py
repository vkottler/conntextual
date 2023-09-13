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

    tui.action_toggle_pause()
    tui.action_toggle_pause()

    # Send some commands.
    for env in tui.model.environments:
        log = env.query_one(ChannelEnvironmentLog)

        processor = log.suggester.processor
        processor.parser.exit(message="null")

        await processor.get_suggestion("set m")
        await processor.get_suggestion("set e")

        for command in [
            "test",
            "help",
            "set a.0.random",
            "set a.0.random -f",
            "set a.0.random 0.5 -f",
            "set a.0.enum three -f",
            "set a.0.enum 2.8 -f",
            "set a.0.bool true -f",
            "set a.0.bool 1.1 -f",
            "toggle a.0.bool -f",
            "toggle a.0.bool -f",
            "toggle a.0.enum -f",
        ]:
            processor.command(command)
            log.handle_submit(MockEvent(command))  # type: ignore

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
