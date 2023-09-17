"""
A module implementing color interfaces for channel enviroments.
"""

# built-in
from typing import Optional

# third-party
from runtimepy.enum import RuntimeEnum
from runtimepy.primitives.type import AnyPrimitiveType
from textual._color_constants import COLOR_NAME_TO_RGB
from textual.color import Color


def type_str_style(kind: AnyPrimitiveType, enum: Optional[RuntimeEnum]) -> str:
    """Get a style for a given type."""

    result = ""

    if kind.is_boolean:
        result = Color(*COLOR_NAME_TO_RGB["ansi_bright_cyan"]).hex
    elif kind.is_float:
        result = Color(*COLOR_NAME_TO_RGB["indigo"]).hex
    else:
        result = Color(*COLOR_NAME_TO_RGB["purple"]).hex

    if enum is not None:
        result += " bold"

    return result
