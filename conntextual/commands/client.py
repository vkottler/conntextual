"""
An entry-point for the 'client' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from runtimepy.entry import main as runtimepy_main
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.io import ARBITER
from vcorelib.paths.context import tempfile

# internal
from conntextual import PKG_NAME
from conntextual.client import client_args, client_config
from conntextual.commands.common import (
    DEFAULT_VARIANT,
    common_cli_args,
    runtimepy_cli_args,
)


def client_cmd(args: _Namespace) -> int:
    """Execute the client command."""

    cli_args = runtimepy_cli_args(args)
    cli_args.append(f"package://{PKG_NAME}/{DEFAULT_VARIANT}.yaml")

    with tempfile(suffix=".json") as path:
        assert ARBITER.encode(path, client_config(args))[0]
        cli_args.append(str(path))

        print(f"runtimepy_main({cli_args})")
        result = runtimepy_main(cli_args)

    return result  # pragma: nocover


def add_client_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add client-command arguments to its parser."""

    common_cli_args(parser)
    client_args(parser)

    return client_cmd
