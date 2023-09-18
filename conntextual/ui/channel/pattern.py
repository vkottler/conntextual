"""
A module implementing an include/exclude pattern matching interface.
"""

# built-in
import re
from typing import NamedTuple, Optional


class PatternPair(NamedTuple):
    """A container for managing pattern data."""

    include: Optional[re.Pattern[str]] = None
    exclude: Optional[re.Pattern[str]] = None

    def matches(self, data: str) -> bool:
        """Determine whether or not a string matches this pattern pair."""

        result = True

        if self.include is not None:
            result = self.include.search(data) is not None

        if self.exclude is not None and result:
            result = self.exclude.search(data) is not None
            result = not result

        return result

    @staticmethod
    def from_dict(data: dict[str, str]) -> "PatternPair":
        """Create a pattern pair from dictionary data."""

        include: Optional[re.Pattern[str]] = data.get(  # type: ignore
            "include",
        )
        if include:
            include = re.compile(include)

        exclude: Optional[re.Pattern[str]] = data.get(  # type: ignore
            "exclude",
        )
        if exclude:
            exclude = re.compile(exclude)

        return PatternPair(include, exclude)
