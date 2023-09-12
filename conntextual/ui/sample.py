"""
A module implementing a sample task for UI testing purposes.
"""

# built-in
from random import random

# third-party
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask, TaskFactory


class SampleTask(ArbiterTask):
    """A base TUI application."""

    app: AppInfo

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        self.app = app

        # Register an enum.
        self.env.enum(
            "SampleEnum",
            "int",
            items={
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
                "ten": 10,
            },
        )

        for name in ["a", "b", "c"]:
            with self.env.names_pushed(name):
                for i in range(10):
                    with self.env.names_pushed(str(i)):
                        self.env.float_channel("random", "double")
                        self.env.int_channel("enum", enum="SampleEnum")
                        self.env.bool_channel("bool")

    async def dispatch(self) -> bool:
        """Dispatch an iteration of this task."""

        with self.log_time("dispatch"):
            dispatches = self.metrics.dispatches.value % 10

            for name in ["a", "b", "c"]:
                for i in range(10):
                    self.env.set(f"{name}.{i}.random", random())
                    self.env.set(
                        f"{name}.{i}.enum", ((dispatches + i) % 10) + 1
                    )
                    self.env.set(f"{name}.{i}.bool", i % 2 == 0)

        return True


class Sample(TaskFactory[SampleTask]):
    """A TUI application factory."""

    kind = SampleTask
