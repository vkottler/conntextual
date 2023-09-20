"""
Test the 'commands.client' module.
"""

# built-in
from subprocess import run
from sys import executable

# module under test
from conntextual import PKG_NAME


def test_client_command_basic():
    """Test basic argument parsing."""

    run([executable, "-m", PKG_NAME, "client", "localhost", "0"], check=False)
