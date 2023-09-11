"""
A module implementing an input suggester for the channel-environment
command widget.
"""

# built-in
from typing import Optional

# third-party
from textual.suggester import Suggester


class CommandSuggester(Suggester):
    """An input suggester for channel environment commands."""

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Get an input suggestion."""

        return value + "test"

    @staticmethod
    def create() -> "CommandSuggester":
        """A method for creating a command suggester."""

        # connect this to channel environments

        return CommandSuggester()
