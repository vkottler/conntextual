"""
An entry-point for the 'ui' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
import socket
from typing import Any

# third-party
from runtimepy.commands.common import arbiter_args
from runtimepy.entry import main as runtimepy_main
from runtimepy.net import IPv4Host, get_free_socket_name
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.io import ARBITER
from vcorelib.logging import forward_flags
from vcorelib.paths.context import tempfile

# internal
from conntextual import PKG_NAME
from conntextual.commands.common import server_args

DEFAULT_VARIANT = "app"


def server_config(args: _Namespace) -> dict[str, Any]:
    """Get a server configuration based on command-line arguments."""

    IPv4Host(port=args.tcp)

    tcp = get_free_socket_name(IPv4Host(port=args.tcp)).port
    websocket = get_free_socket_name(IPv4Host(port=args.tcp)).port
    udp = get_free_socket_name(
        IPv4Host(port=args.tcp), kind=socket.SOCK_DGRAM
    ).port

    return {
        "includes": ["package://runtimepy/factories.yaml"],
        "servers": [
            {"factory": "tcp_json", "kwargs": {"port": tcp}},
            {
                "factory": "websocket_json",
                "kwargs": {"port": websocket, "host": "0.0.0.0"},
            },
        ],
        "clients": [
            {
                "factory": "udp_json",
                "name": "udp_server",
                "kwargs": {"local_addr": ["0.0.0.0", udp]},
            }
        ],
        "config": {
            "udp_server": udp,
            "tcp_server": tcp,
            "websocket_server": websocket,
        },
    }


def ui_cmd(args: _Namespace) -> int:
    """Execute the ui command."""

    cli_args = ["runtimepy"]

    flags = set(forward_flags(args, ["curses", "verbose", "no_uvloop"]))

    # Don't initialize regular logging no matter what.
    flags.add("--quiet")

    cli_args.extend(flags)

    cli_args.append("arbiter")
    cli_args.extend(list(forward_flags(args, ["init_only"])))

    # Always wait for the program to exit.
    cli_args.append("-w")

    cli_args.extend(args.configs)
    cli_args.append(f"package://{args.package}/{args.variant}.yaml")

    with tempfile(suffix=".json") as path:
        assert ARBITER.encode(path, server_config(args))[0]
        cli_args.append(str(path))

        print(f"runtimepy_main({cli_args})")
        result = runtimepy_main(cli_args)

    return result


def add_ui_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add ui-command arguments to its parser."""

    parser.add_argument(
        "-p",
        "--package",
        default=PKG_NAME,
        help="package to source application from",
    )
    parser.add_argument(
        "-v",
        "--variant",
        choices=[DEFAULT_VARIANT, "curses"],
        default=DEFAULT_VARIANT,
        help="application variant to use (default: %(default)s)",
    )
    server_args(parser)

    arbiter_args(parser, nargs="*")

    return ui_cmd
