"""
An entry-point for the 'ui' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from typing import Iterable, Iterator

# third-party
from runtimepy.commands.common import arbiter_args
from runtimepy.entry import main as runtimepy_main
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from conntextual import PKG_NAME

DEFAULT_VARIANT = "app"


def forward_flags(args: _Namespace, names: Iterable[str]) -> Iterator[str]:
    """Forward flag arguments."""

    for name in names:
        if getattr(args, name, False):
            yield f"--{name}"


def ui_cmd(args: _Namespace) -> int:
    """Execute the ui command."""

    cli_args = ["runtimepy"]
    cli_args.extend(list(forward_flags(args, ["curses", "verbose"])))

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
        choices=[DEFAULT_VARIANT, "curses"],
        default=DEFAULT_VARIANT,
        help="application variant to use (default: %(default)s)",
    )

    arbiter_args(parser, nargs="*")

    return ui_cmd
