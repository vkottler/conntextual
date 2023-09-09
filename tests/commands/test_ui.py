"""
Test the 'commands.ui' module.
"""

# module under test
from conntextual import PKG_NAME
from conntextual.entry import main as conntextual_main


def test_ui_command_basic():
    """Test basic argument parsing."""

    args = [PKG_NAME, "-v", "ui", "--init_only"]
    assert conntextual_main(args) == 0

    args = [PKG_NAME, "ui"]
    configs = [
        "package://conntextual/json.yaml",
        "package://tests/valid/test.yaml",
    ]

    assert conntextual_main(args + configs) == 0

    for variant in ["curses"]:
        assert conntextual_main(args + ["--variant", variant] + configs) == 0
