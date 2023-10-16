"""
A module implementing a plot widget.
"""

# third-party
from numpy.typing import ArrayLike
from textual_plotext import PlotextPlot


class Plot(PlotextPlot):
    """A plot widget."""

    def __init__(
        self,
        x: ArrayLike,
        y: ArrayLike,
        theme: str,
        marker: str,
        *args,
        title: str = "under construction",
        **kwargs,
    ) -> None:
        """Initialize this instance."""

        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.title = title
        self.plot_theme = theme
        self.plot_marker = marker

    def on_show(self) -> None:
        """Handle showing the plot."""

        self.dispatch()

    def on_resize(self) -> None:
        """Handle re-size."""

        self.dispatch()

    def on_mount(self) -> None:
        """Initialize the plot."""

        self.update_title()
        self.plt.theme(self.plot_theme)

    def update_title(self, name: str = None) -> None:
        """Update the plot's title."""

        if name is not None:
            self.title = name

        self.plt.title(self.title)

    def dispatch(self) -> None:
        """Draw a new instance of the plot."""

        self.plt.clear_data()
        self.plt.plot(self.x, self.y, marker=self.plot_marker)  # type: ignore
        self.refresh()

    def set_data(self, x: ArrayLike, y: ArrayLike) -> None:
        """Assign new data."""

        self.x = x
        self.y = y
        self.dispatch()
