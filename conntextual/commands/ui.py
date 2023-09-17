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
from vcorelib.logging import forward_flags

# internal
from conntextual import PKG_NAME

DEFAULT_VARIANT = "app"


def ui_cmd(args: _Namespace) -> int:
    """Execute the ui command."""

    cli_args = ["runtimepy"]

    flags = set(forward_flags(args, ["curses", "verbose", "no_uvloop"]))

    # Don't initialize regular logging no matter what.
    flags.add("--quiet")

    cli_args.extend(flags)

    cli_args.append("arbiter")
    cli_args.extend(list(forward_flags(args, ["init_only"])))

    cli_args.append(f"package://{args.package}/{args.variant}.yaml")
    cli_args.extend(args.configs)

    print(f"runtimepy_main({cli_args})")
    return runtimepy_main(cli_args)


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
        choices=[DEFAULT_VARIANT, "curses", "wait_for_stop"],
        default=DEFAULT_VARIANT,
        help="application variant to use (default: %(default)s)",
    )

    arbiter_args(parser, nargs="*")

    return ui_cmd
