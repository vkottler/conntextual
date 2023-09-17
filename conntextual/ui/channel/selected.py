"""
A module implementing an interface for channel selection.
"""

# built-in
from dataclasses import dataclass
from typing import List, Union

# third-party
from runtimepy.channel.environment.base import ChannelResult
from vcorelib.math.time import default_time_ns


@dataclass
class SelectedChannel:
    """A container for selected-channel information."""

    name: str
    channel: ChannelResult
    timestamps: List[float]
    values: List[Union[float, int, bool]]
    start_ns: int

    @staticmethod
    def create(name: str, channel: ChannelResult) -> "SelectedChannel":
        """Create a selected-channel instance."""

        return SelectedChannel(name, channel, [], [], default_time_ns())

    def reset(self) -> None:
        """Reset this channel's start time."""

        self.timestamps = []
        self.values = []
        self.start_ns = default_time_ns()

    def poll(self) -> None:
        """Poll the underlying channel."""

        chan = self.channel[0]
        last_updated = chan.raw.last_updated_ns

        # Need to handle not infinitely growing.
        if (not self.timestamps) or last_updated > self.timestamps[-1]:
            self.timestamps.append((last_updated - self.start_ns) / 1e9)
            self.values.append(chan.raw.value)
