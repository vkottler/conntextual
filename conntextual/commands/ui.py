"""
An entry-point for the 'ui' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from runtimepy.commands.common import arbiter_args
from runtimepy.entry import main as runtimepy_main
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.io import ARBITER
from vcorelib.paths.context import tempfile

# internal
from conntextual import PKG_NAME
from conntextual.commands.common import (
    DEFAULT_VARIANT,
    common_cli_args,
    runtimepy_cli_args,
)
from conntextual.server import server_args, server_config


def ui_cmd(args: _Namespace) -> int:
    """Execute the ui command."""

    cli_args = runtimepy_cli_args(args)

    cli_args.append(f"package://{args.package}/{args.variant}.yaml")

    with tempfile(suffix=".json") as path:
        assert ARBITER.encode(path, server_config(args))[0]
        if not args.no_server:
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
        choices=[DEFAULT_VARIANT, "curses", "headless"],
        default=DEFAULT_VARIANT,
        help="application variant to use (default: %(default)s)",
    )
    common_cli_args(parser)
    server_args(parser)

    with arbiter_args(parser, nargs="*"):
        pass

    return ui_cmd
