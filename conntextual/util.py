"""
A module containing miscellaneous.
"""


def css_name(name: str) -> str:
    """Replace some characters that don't work in identifier values."""
    return name.replace(".", "_")
