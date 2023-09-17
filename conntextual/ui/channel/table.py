"""
A module implementing a channel-table data model.
"""

# built-in
from dataclasses import dataclass
from typing import List, NamedTuple, Optional

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.channel.environment.base import ChannelValue
from runtimepy.enum import RuntimeEnum
from runtimepy.primitives.type import AnyPrimitiveType


class ChannelType(NamedTuple):
    """A container for channel-type information."""

    underlying: AnyPrimitiveType
    enum: Optional[RuntimeEnum]


@dataclass
class ChannelRow:
    """A container for channel rows."""

    identifier: int
    kind: ChannelType
    name: str
    value: ChannelValue

    def __hash__(self) -> int:
        """Get a hash for this row."""
        return self.identifier

    def __eq__(self, other) -> bool:
        """Determine if two rows are the same."""
        return hash(self) == hash(other)

    def kind_str(self, env: ChannelEnvironment) -> str:
        """Get a channel row's type string."""

        kind_str = str(self.kind.underlying)
        if self.kind.enum is not None:
            result = env.enums.names.name(self.kind.enum.id)
            assert result is not None
            kind_str = result

        return kind_str

    def value_str(self) -> str:
        """Get this row's value as a string."""

        if isinstance(self.value, bool):
            return "true" if self.value else "false"

        if isinstance(self.value, float):
            return f"{self.value: 15.6f}"

        if isinstance(self.value, int):
            return f"{self.value: 8d}       "

        return self.value


ID_COL_LABEL = "id"
NAME_COL_LABEL = "name"
TYPE_COL_LABEL = "type"
VALUE_COL_LABEL = "value"


class ChannelTable:
    """A channel table implementation."""

    columns = [ID_COL_LABEL, TYPE_COL_LABEL, NAME_COL_LABEL, VALUE_COL_LABEL]

    def __init__(self, env: ChannelEnvironment) -> None:
        """Initialize this channel table."""

        self.env = env

        # Underlying storage.
        self.rows: List[ChannelRow] = []

        for name in self.env.names:
            chan, enum = env[name]

            self.rows.append(
                ChannelRow(
                    chan.id,
                    ChannelType(chan.type, enum),
                    name,
                    self.env.value(name),
                )
            )

        self.compute_size()

    def update_values(self) -> None:
        """Update underlying values."""

        for row in self.rows:
            row.value = self.env.value(row.name)

    def compute_size(self) -> None:
        """Compute sizes of entities."""

        self.id_width = self.widest_id_len()
        self.type_width = self.widest_type_len()
        self.name_width = self.widest_name_len()
        self.value_width = self.widest_value_len()

        self.width = sum(
            (self.id_width, self.type_width, self.name_width, self.value_width)
        )

        self.height = len(self.rows) + 1

    def widest_id_len(self) -> int:
        """Get the widest identifier column width."""

        return max(
            max(len(str(x.identifier)) for x in self.rows), len(ID_COL_LABEL)
        )

    def widest_type_len(self) -> int:
        """Get the widest type column width."""

        return max(
            max(len(str(x.kind_str(self.env))) for x in self.rows),
            len(TYPE_COL_LABEL),
        )

    def widest_name_len(self) -> int:
        """Get the widest name column width."""

        return max(
            max(len(str(x.name)) for x in self.rows), len(NAME_COL_LABEL)
        )

    def widest_value_len(self) -> int:
        """Get the widest value column width."""

        return max(
            max(len(str(x.value_str())) for x in self.rows),
            len(VALUE_COL_LABEL),
        )
