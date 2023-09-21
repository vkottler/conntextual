"""
A module implementing an include/exclude pattern matching interface.
"""

# built-in
import re
from typing import List, NamedTuple, Optional, Union

PatternList = List[re.Pattern[str]]
StringOrList = Union[str, List[str]]


class PatternPair(NamedTuple):
    """A container for managing pattern data."""

    includes: PatternList
    excludes: PatternList

    def matches(self, data: str) -> bool:
        """Determine whether or not a string matches this pattern pair."""

        include_result = True

        if self.includes:
            include_result = any(
                include.search(data) is not None for include in self.includes
            )

        exclude_result = False

        if include_result:
            exclude_result = any(
                exclude.search(data) is not None for exclude in self.excludes
            )

        return include_result and not exclude_result

    @staticmethod
    def from_dict(data: dict[str, StringOrList]) -> "PatternPair":
        """Create a pattern pair from dictionary data."""

        includes: PatternList = []
        excludes: PatternList = []

        for patterns, keys in zip(
            [includes, excludes],
            [
                ["include", "includes", "included"],
                ["exclude", "excludes", "excluded"],
            ],
        ):
            for key in keys:
                pattern: Optional[StringOrList] = data.get(key)
                if pattern:
                    if isinstance(pattern, str):
                        patterns.append(re.compile(pattern))
                    else:
                        patterns += [re.compile(x) for x in pattern]

        return PatternPair(includes, excludes)
