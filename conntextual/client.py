"""
A module implementing conntextual client interfaces.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from typing import Any

# third-party
from runtimepy.commands.common import arbiter_args


def client_args(
    parser: _ArgumentParser, default_factory: str = "tcp_json"
) -> None:
    """Add command-line argument options for servers."""

    parser.add_argument("host", help="hostname to connect to")
    parser.add_argument("port", type=int, help="port to connect to")
    parser.add_argument(
        "-f",
        "--factory",
        default=default_factory,
        help="connection factory to use (default: %(default)s)",
    )

    with arbiter_args(parser, nargs="*"):
        pass


def client_config(args: _Namespace) -> dict[str, Any]:
    """Get a server configuration based on command-line arguments."""

    result = {
        "includes": ["package://runtimepy/factories.yaml"],
        "clients": [
            {
                "name": "client",
                "factory": args.factory,
                "kwargs": {"host": args.host, "port": args.port},
            }
        ],
    }

    return result
