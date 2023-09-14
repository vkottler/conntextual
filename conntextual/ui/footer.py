"""
A module implementing a custom footer widget.
"""

# built-in
from typing import Optional, cast

# third-party
from rich.console import RenderableType
from rich.text import Text
from textual.widgets import Footer


class CustomFooter(Footer):
    """An extension of the footer widget."""

    current_tab: Optional[str]

    def render(self) -> RenderableType:
        """Render the footer."""

        result: Text = cast(Text, super().render())

        # Manually add text for tab and shift tab.

        if self.current_tab:
            result = Text.assemble(
                result,
                "| ",
                Text(f"tab: {self.current_tab}", style="yellow bold"),
            )

        return result
