# =====================================
# generator=datazen
# version=3.1.3
# hash=fffb56549200e052a1bc8f7fac716767
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
from conntextual.commands.ui import add_ui_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "ui",
            "run a user interface for runtimepy applications",
            add_ui_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
