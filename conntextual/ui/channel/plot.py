"""
A module implementing a plot widget.
"""

# third-party
from numpy.typing import ArrayLike
import plotext as plt
from rich.text import Text
from textual.widgets import Static


class Plot(Static):
    """A plot widget."""

    theme = "pro"

    def __init__(
        self,
        x: ArrayLike,
        y: ArrayLike,
        *args,
        title: str = "under construction",
        **kwargs,
    ) -> None:
        """Initialize this instance."""

        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.title = title

    def on_show(self) -> None:
        """Handle showing the plot."""

        self.dispatch()

    def on_resize(self) -> None:
        """Handle re-size."""

        self.dispatch()

    def dispatch(self) -> None:
        """Draw a new instance of the plot."""

        plt.clf()

        plt.plot(self.x, self.y)
        plt.title(self.title)
        plt.theme(self.theme)

        plt.plotsize(self.size.width, self.size.height)

        self.update(Text.from_ansi(plt.build()))

    def set_data(self, x: ArrayLike, y: ArrayLike) -> None:
        """Assign new data."""

        self.x = x
        self.y = y
        self.dispatch()
