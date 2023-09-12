"""
A module implementing UI command processing.
"""

# built-in
from argparse import Namespace
from typing import Any, Optional, cast

# third-party
from runtimepy.channel import AnyChannel
from runtimepy.channel.environment import ChannelEnvironment
from runtimepy.mixins.environment import ChannelEnvironmentMixin
from runtimepy.primitives.bool import Bool
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

    def do_set(self, args: Namespace) -> CommandResult:
        """Attempt to set a channel value."""

        result = SUCCESS

        if not args.extra:
            return CommandResult(False, "No value specified.")

        try:
            self.env.set(args.channel, args.extra[0])
        except (KeyError, ValueError) as exc:
            result = CommandResult(False, str(exc))

        return result

    def do_toggle(self, args: Namespace, channel: AnyChannel) -> CommandResult:
        """Attempt to toggle a channel."""

        if args.command == ChannelCommand.TOGGLE:
            if not channel.type.is_boolean:
                return CommandResult(
                    False,
                    (
                        f"Channel '{args.channel}' is "
                        f"{channel.type}, not boolean."
                    ),
                )

            cast(Bool, channel.raw).toggle()

        return SUCCESS

    def handle_command(self, args: Namespace) -> CommandResult:
        """Handle a command from parsed arguments."""

        result = SUCCESS

        chan = self.env.get(args.channel)
        if chan is None:
            return CommandResult(False, f"No channel '{args.channel}'.")

        channel, enum = chan
        del enum

        # Check if channel is commandable (or if a -f/--force flag is set?).
        if not channel.commandable and not args.force:
            return CommandResult(
                False,
                (
                    f"Channel '{args.channel}' not "
                    "commandable! (use -f/--force to bypass if necessary)"
                ),
            )

        if args.command == ChannelCommand.TOGGLE:
            result = self.do_toggle(args, channel)
        elif args.command == ChannelCommand.SET:
            result = self.do_set(args)

        return result

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
