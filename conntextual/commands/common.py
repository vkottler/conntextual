"""
A module implementing shared argument parsing interfaces.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from typing import List

# third-party
from vcorelib.logging import forward_flags

DEFAULT_VARIANT = "app"


def runtimepy_cli_args(args: _Namespace) -> List[str]:
    """Get base command-line arguments for a runtimepy invocation."""

    cli_args = ["runtimepy"]

    flags = set(forward_flags(args, ["curses", "verbose", "no_uvloop"]))

    is_headless = getattr(args, "variant", None) == "headless"

    if not args.verbose and not is_headless:
        flags.add("--quiet")

    cli_args.extend(flags)

    cli_args.append(args.cmd)
    cli_args.extend(list(forward_flags(args, ["init_only"])))

    # Ensure that the application continues to run when running the user
    # interface.
    if not is_headless or args.wait_for_stop:
        cli_args.append("--wait-for-stop")

    cli_args.extend(args.configs)

    return cli_args


def common_cli_args(parser: _ArgumentParser) -> None:
    """Add common command-line options."""

    parser.add_argument(
        "-c",
        "--cmd",
        default="arbiter",
        help="runtimepy command to run (default: %(default)s)",
    )
