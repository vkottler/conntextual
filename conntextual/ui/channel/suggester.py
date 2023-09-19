"""
A module implementing an input suggester for the channel-environment
command widget.
"""

# built-in
from typing import Optional

# third-party
from runtimepy.channel.environment.command import ChannelCommandProcessor
from textual.suggester import Suggester


class CommandSuggester(Suggester):
    """An input suggester for channel environment commands."""

    processor: ChannelCommandProcessor

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Get an input suggestion."""
        return self.processor.get_suggestion(value)

    @staticmethod
    def create(processor: ChannelCommandProcessor) -> "CommandSuggester":
        """A method for creating a command suggester."""

        result = CommandSuggester()
        result.processor = processor
        return result
