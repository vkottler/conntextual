"""
A module implementing shared argument parsing interfaces.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser


def server_args(parser: _ArgumentParser) -> None:
    """Add command-line argument options for servers."""

    parser.add_argument(
        "--udp",
        default=0,
        type=int,
        help="JSON message server UDP port (default: %(default)d)",
    )
    parser.add_argument(
        "--tcp",
        default=0,
        type=int,
        help="JSON message server TCP port (default: %(default)d)",
    )
    parser.add_argument(
        "--websocket",
        default=0,
        type=int,
        help="JSON message server WebSocket port (default: %(default)d)",
    )
