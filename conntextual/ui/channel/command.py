"""
A module implementing UI command processing.
"""

# built-in
from argparse import Namespace
from typing import Any, Optional

# third-party
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.mixins.environment import ChannelEnvironmentMixin
from vcorelib.logging import LoggerType

# internal
from conntextual.ui.channel.parser import ChannelCommand, CommandParser
from conntextual.ui.channel.result import SUCCESS, CommandResult


class CommandProcessor(ChannelEnvironmentMixin):
    """A command processing interface for channel environments."""

    def __init__(
        self, env: ChannelEnvironment, logger: LoggerType, **kwargs
    ) -> None:
        """Initialize this instance."""

        super().__init__(env=env, **kwargs)
        self.logger = logger

        self.parser_data: dict[str, Any] = {}
        self.parser = CommandParser()
        self.parser.data = self.parser_data

        self.parser.initialize()

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Get an input suggestion."""

        result = None

        args = self.parse(value)
        if args is not None:
            result = self.env.namespace_suggest(args.channel, delta=False)
            if result is not None:
                result = args.command + " " + result

        return result

    def handle_command(self, args: Namespace) -> CommandResult:
        """Handle a command from parsed arguments."""

        # validate channel

        if args.command == ChannelCommand.SET:
            pass

        elif args.command == ChannelCommand.TOGGLE:
            pass

        self.logger.info(args)

        return SUCCESS

    def parse(self, value: str) -> Optional[Namespace]:
        """Attempt to parse arguments."""

        self.parser_data["error_message"] = None
        args = self.parser.parse_args(value.split())
        return args if not self.parser_data["error_message"] else None

    def command(self, value: str) -> CommandResult:
        """Process a command."""

        args = self.parse(value)
        success = args is not None

        if not args or "help" in value:
            self.logger.info(self.parser.format_help())

        reason = None
        if not success:
            reason = self.parser_data["error_message"]
            if "help" not in value:
                self.logger.info("Try 'help'.")

        result = CommandResult(success, reason)

        if success:
            assert args is not None
            result = self.handle_command(args)

        return result
