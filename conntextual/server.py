"""
A module implementing conntextual server interfaces.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
import socket
from typing import Any

# third-party
from runtimepy.net import IPv4Host, get_free_socket_name


def server_args(parser: _ArgumentParser) -> None:
    """Add command-line argument options for servers."""

    parser.add_argument(
        "--udp",
        default=0,
        type=int,
        help="JSON message server UDP port (default: %(default)d)",
    )
    parser.add_argument(
        "--udp-factory",
        default="udp_json",
        help="connection factory to use for UDP server (default: %(default)s)",
    )

    parser.add_argument(
        "--tcp",
        default=0,
        type=int,
        help="JSON message server TCP port (default: %(default)d)",
    )
    parser.add_argument(
        "--tcp-factory",
        default="tcp_json",
        help="connection factory to use for UDP server (default: %(default)s)",
    )

    parser.add_argument(
        "--websocket",
        default=0,
        type=int,
        help="JSON message server WebSocket port (default: %(default)d)",
    )
    parser.add_argument(
        "--websocket-factory",
        default="websocket_json",
        help=(
            "connection factory to use for WebSocket "
            "server (default: %(default)s)"
        ),
    )

    parser.add_argument(
        "-n",
        "--no-server",
        action="store_true",
        help="don't start any JSON command listeners",
    )


def server_config(args: _Namespace) -> dict[str, Any]:
    """Get a server configuration based on command-line arguments."""

    config: dict[str, Any] = {
        "includes": ["package://runtimepy/factories.yaml"],
        "servers": [
            {"factory": args.tcp_factory, "kwargs": {"port": "$tcp_json"}},
            {
                "factory": args.websocket_factory,
                "kwargs": {"port": "$websocket_json", "host": "0.0.0.0"},
            },
        ],
        "port_overrides": {
            "tcp_json": get_free_socket_name(IPv4Host(port=args.tcp)).port,
            "websocket_json": get_free_socket_name(
                IPv4Host(port=args.websocket)
            ).port,
        },
    }

    if not args.init_only:
        config["clients"] = [
            {
                "factory": args.udp_factory,
                "name": "udp_json_server",
                "kwargs": {"local_addr": ["localhost", "$udp_json"]},
            }
        ]
        config["port_overrides"]["udp_json"] = get_free_socket_name(
            IPv4Host(port=args.udp), kind=socket.SOCK_DGRAM
        ).port

    return config
