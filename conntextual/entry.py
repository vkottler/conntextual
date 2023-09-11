# =====================================
# generator=datazen
# version=3.1.3
# hash=9bf8e775e93cc789e583c753b9b13bb6
# =====================================

"""
This package's command-line entry-point (boilerplate).
"""

# built-in
import argparse
import os
from pathlib import Path
import sys
from typing import List

# third-party
from vcorelib.logging import logging_args

# internal
from conntextual import DESCRIPTION, VERSION
from conntextual.app import add_app_args, entry


def main(argv: List[str] = None) -> int:
    """Program entry-point."""

    result = 0

    # fall back on command-line arguments
    command_args = sys.argv
    if argv is not None:
        command_args = argv

    # initialize argument parsing
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    logging_args(parser)
    parser.add_argument(
        "-C",
        "--dir",
        default=Path.cwd(),
        dest="dir",
        type=Path,
        help="execute from a specific directory",
    )
    starting_dir = Path.cwd()

    add_app_args(parser)

    # parse arguments and execute the requested command
    try:
        args = parser.parse_args(command_args[1:])
        args.version = VERSION
        args.dir = args.dir.resolve()

        # change to the specified directory
        os.chdir(args.dir)

        # run the application
        result = entry(args)
    except SystemExit as exc:
        result = 1
        if exc.code is not None and isinstance(exc.code, int):
            result = exc.code

    # return to starting dir
    os.chdir(starting_dir)

    return result
