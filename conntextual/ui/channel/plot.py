"""
A module implementing a plot widget.
"""

# third-party
import numpy as np
from numpy.typing import ArrayLike
import plotext as plt
from rich.text import Text
from textual.widgets import Static


class Plot(Static):
    """A plot widget."""

    theme = "pro"

    def __init__(self, x: ArrayLike, y: ArrayLike, *args, **kwargs) -> None:
        """Initialize this instance."""

        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.title = "under construction"

    def on_show(self) -> None:
        """Handle showing the plot."""

        self.on_resize()

    def on_resize(self) -> None:
        """Handle re-size."""

        plt.clf()

        # set this based on channel
        plt.plot(self.x, self.y)
        plt.title(self.title)
        plt.theme(self.theme)

        plt.plotsize(self.size.width, self.size.height)

        self.update(Text.from_ansi(plt.build()))

    def shift_data(self) -> None:
        """Shift data randomly."""

        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x + np.random.uniform(0, np.pi))
        self.set_data(x, y)

    def set_data(self, x: ArrayLike, y: ArrayLike) -> None:
        """Assign new data."""

        self.x = x
        self.y = y
        self.on_resize()
