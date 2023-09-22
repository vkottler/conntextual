"""
A module implementing shared argument parsing interfaces.
"""

# built-in
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

    cli_args.append("arbiter")
    cli_args.extend(list(forward_flags(args, ["init_only"])))

    # Only wait for the program to exit when in user-interface mode.
    if not is_headless:
        cli_args.append("-w")

    cli_args.extend(args.configs)

    return cli_args
