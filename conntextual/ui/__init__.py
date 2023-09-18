"""
A module implementing a basic user interface.
"""

# built-in
from asyncio import sleep
from dataclasses import dataclass

# third-party
from runtimepy.net.arbiter import AppInfo

# internal
from conntextual.ui.base import Base
from conntextual.ui.channel.environment import ChannelEnvironmentDisplay
from conntextual.ui.channel.log import ChannelEnvironmentLog, InputWithHistory
from conntextual.ui.channel.model import ChannelEnvironmentSource
from conntextual.ui.task import TuiDispatchTask

__all__ = [
    "Base",
    "test",
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


@dataclass
class MockCoordinate:
    """A mock coordinate class."""

    row: int


@dataclass
class MockCellEvent:
    """A mock cell-selection event class."""

    coordinate: MockCoordinate


async def tui_test(tui: Base) -> None:
    """Test the UI."""

    await tui.composed.wait()

    iterations = 2 * len(tui.model.environments)

    # Cycle through tabs.
    for direction in [True, False]:
        for _ in range(iterations):
            tui.action_tab(direction)
            await sleep(0.05)

    tui.action_toggle_pause()
    tui.action_toggle_pause()

    # Test input tab handling.
    await tui.action_focus("tui-input")
    tui.action_tab(True)

    # Send some commands.
    for env in tui.model.environments:
        log = env.query_one(ChannelEnvironmentLog)
        input_box = env.query_one(InputWithHistory)

        assert log.suggester is not None
        processor = log.suggester.processor
        processor.parser.exit(message="null")

        processor.get_suggestion("set m")
        processor.get_suggestion("set e")

        env.handle_cell_selected(
            MockCellEvent(MockCoordinate(1)),  # type: ignore
        )

        tui.action_refresh_plot()
        tui.action_random_channel()

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
            input_box.value = command
            log.handle_submit(MockEvent(command))  # type: ignore

            input_box.action_previous_command()

        await sleep(0.05)

    tui.model.app.stop.set()


async def test(app: AppInfo) -> int:
    """Run a textual application."""

    if not app.stop.is_set():
        periodics = list(app.search_tasks(kind=TuiDispatchTask))
        assert (
            len(periodics) == 1
        ), f"{len(periodics)} application tasks found!"

        await tui_test(periodics[0].tui)
        app.logger.info("Test complete, stopping application.")
        app.stop.set()

    return 0
