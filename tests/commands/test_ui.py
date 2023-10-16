"""
Test the 'commands.ui' module.
"""

# built-in
from unittest.mock import patch

# third-party
from runtimepy.tui.mock import wrapper_mock

# module under test
from conntextual import PKG_NAME
from conntextual.entry import main as conntextual_main

CONFIGS = ["package://conntextual/json.yaml"]


def test_ui_curses():
    """Test user interfaces that require curses mode."""

    with patch("runtimepy.commands.common._curses.wrapper", new=wrapper_mock):
        args = [PKG_NAME, "--curses", "ui"]
        for variant in ["curses"]:
            assert (
                conntextual_main(
                    args
                    + ["--variant", variant]
                    + CONFIGS
                    + ["package://tests/valid/test.yaml"]
                )
                == 0
            )


def test_ui_command_basic():
    """Test basic argument parsing."""

    args = [PKG_NAME, "--no-uvloop", "ui"]
    test_input = "package://tests/valid/textual_ui_test.yaml"

    assert conntextual_main(args + CONFIGS + [test_input]) == 0

    args = [PKG_NAME, "-v", "ui", "--init_only", test_input]
    assert conntextual_main(args) == 0
