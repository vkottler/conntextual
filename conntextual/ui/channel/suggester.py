"""
A module implementing an input suggester for the channel-environment
command widget.
"""

# built-in
from typing import Optional

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.channel.environment.command import ChannelCommandProcessor
from textual.suggester import Suggester
from vcorelib.logging import LoggerType


class CommandSuggester(Suggester):
    """An input suggester for channel environment commands."""

    processor: ChannelCommandProcessor

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Get an input suggestion."""
        return self.processor.get_suggestion(value)

    @staticmethod
    def create(
        env: ChannelEnvironment, logger: LoggerType
    ) -> "CommandSuggester":
        """A method for creating a command suggester."""

        result = CommandSuggester()
        result.processor = ChannelCommandProcessor(env, logger)
        return result
