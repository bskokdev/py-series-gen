from argparse import ArgumentParser, Namespace
from typing import Any, Tuple

from publishers.targets.target import Target
from publishers.targets.target_factory import TargetFactory

from .argument_formatter import TargetHelpFormatter
from .arguments import (
    core_arguments,
    flags,
    generator_name_to_function,
    specific_target_args,
    target_arg_to_type,
)


def _attach_core_arguments_and_flags(parser: ArgumentParser):
    """Attaches defaulty supported arguments to the parser.

    Args:
        parser (ArgumentParser): An object which handles all the arguments
    """
    for arg, dest, arg_type, help in core_arguments:
        parser.add_argument(arg, dest=dest, type=arg_type, help=help)

    for arg_flag, dest, action, default, help in flags:
        parser.add_argument(
            arg_flag, dest=dest, action=action, default=default, help=help
        )


def create_parser_with_all_args() -> Tuple[ArgumentParser, Namespace]:
    """Constructs a parser with all supported arguments in the application.
    Utilizes mapping of :
        * target type -> list of arguments specific to that type

    Returns:
        Tuple[ArgumentParser, Namespace]: parser, and arguments
    """
    parser = ArgumentParser(formatter_class=TargetHelpFormatter)
    _attach_core_arguments_and_flags(parser)

    # Add all target-specific arguments with their target type as a prefix
    for target_type, args in specific_target_args.items():
        group = parser.add_argument_group(f"{target_type.name} arguments")
        for argument, variable, dtype, help_str in args:
            group.add_argument(argument, dest=variable, type=dtype, help=help_str)

    return parser, parser.parse_args()


def build_target_from_args(parser: ArgumentParser, args: Namespace) -> Target:
    """Build a target object (state supplied to a publisher) from the CLI arguments.
    We cast the --target argument to an argument type via mapping:
        * target str -> target type

    Args:
        parser (ArgumentParser): An object which handles all the arguments state
        args (Namespace): All arguments wrapped in a namespace object

    Returns:
        Target: A target object which is a state supplied to a publisher
    """
    if not args.target:
        parser.error("Target type must be specified (--target TARGET)")

    target_type = target_arg_to_type[args.target]
    try:
        return TargetFactory().create_target(target_type=target_type, args=args)
    except Exception as e:
        parser.error(str(e))


def get_generator_func_from_args(args: Namespace) -> Any:
    return generator_name_to_function[args.generator]


def verify_core_args(parser: ArgumentParser, args: Namespace):
    """Verifies core runtime arguments (target, and batch_size).
    If one of them doesn't match the expected value a ValueError is raised.

    Args:
        args (Namespace): An entire namespace of arguments from parser

    Raises:
        ValueError: Raised if target, or batch_size don't contain a valid value
    """
    if not args.generator or args.generator not in generator_name_to_function:
        parser.error(
            "Generator function must be specified (--generator NAME). It's possible such generator is not yet supported."
        )

    if not args.target or args.target not in target_arg_to_type:
        parser.error(
            "Target type must be specified (--target TARGET). It's possible such target is not yet supported."
        )

    if not args.batch_size or args.batch_size < 0:
        parser.error("Batch size must be specified (--batch-size SIZE | SIZE > 0)")
