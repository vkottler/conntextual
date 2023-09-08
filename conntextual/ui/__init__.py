"""
A module implementing a basic user interface.
"""

# built-in
import logging
import os

# third-party
from runtimepy.net.arbiter import AppInfo
from textual.logging import TextualHandler

# internal
from conntextual.ui.base import Base


async def run(app: AppInfo) -> int:
    """Run a textual application."""

    if app.config["debug"]:
        logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
        os.environ["TEXTUAL"] = "devtools,debug"

    await Base.create(app).run_async()

    return 0
