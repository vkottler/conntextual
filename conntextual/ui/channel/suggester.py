"""
A module implementing an input suggester for the channel-environment
command widget.
"""

# built-in
from typing import Optional

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from textual.suggester import Suggester
from vcorelib.logging import LoggerType

# internal
from conntextual.ui.channel.command import CommandProcessor


class CommandSuggester(Suggester):
    """An input suggester for channel environment commands."""

    processor: CommandProcessor

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Get an input suggestion."""
        return await self.processor.get_suggestion(value)

    @staticmethod
    def create(
        env: ChannelEnvironment, logger: LoggerType
    ) -> "CommandSuggester":
        """A method for creating a command suggester."""

        result = CommandSuggester()
        result.processor = CommandProcessor(env, logger)
        return result
