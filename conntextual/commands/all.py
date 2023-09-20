# =====================================
# generator=datazen
# version=3.1.3
# hash=f353fb494df76a27eff3f95cce1dd6b6
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from conntextual.commands.client import add_client_cmd
from conntextual.commands.ui import add_ui_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "client",
            "attempt to connect a client to a remote session",
            add_client_cmd,
        ),
        (
            "ui",
            "run a user interface for runtimepy applications",
            add_ui_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
