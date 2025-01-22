from argparse import ArgumentParser, Namespace
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from publishers.targets.target import Target, TargetType
from publishers.targets.target_factory import TargetFactory

from .argument_formatter import TargetHelpFormatter

# Maps a target type argument string to an actual enum class, for better typing
target_arg_to_type: Dict[str, TargetType] = defaultdict(
    None, {"console": TargetType.console, "kafka": TargetType.kafka}
)

# Maps a target type to a list of arguments specific to such type
# This is where you add specific arguments for each target type (console, kafka, etc.)
specific_target_args: Dict[TargetType, List[Tuple[str, str, Any, str]]] = defaultdict(
    list,
    {
        TargetType.kafka: [
            (
                "--bootstrap-server",
                "bootstrap_server",
                str,
                "Address of the bootstrap server",
            ),
            (
                "--port",
                "port",
                int,
                "Port at which the broker process is running",
            ),
            (
                "--topic",
                "kafka_topic",
                str,
                "Kafka topic to send the data to",
            ),
            # TODO: expand the arguments further, if possible
        ]
    },
)


def _attach_default_args(parser: ArgumentParser):
    """Attaches defaulty supported arguments to the parser.

    Args:
        parser (ArgumentParser): An object which handles all the arguments state
    """
    parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="Destination to publish the data to",
    )
    parser.add_argument(
        "--batch-size",
        dest="batch_size",
        type=int,
        help="Single batch (iteration) size",
    )
    parser.add_argument(
        "--stream",
        dest="is_stream",
        action="store_true",
        default=False,
        help="Should the batch be sent repeatedly",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Should the process run in debug mode",
    )


def create_parser_with_all_args() -> Tuple[ArgumentParser, Namespace]:
    """Constructs a parser with all supported arguments in the application.
    Utilizes mapping of :
        * target type -> list of arguments specific to that type

    Returns:
        Tuple[ArgumentParser, Namespace]: parser, and the complete argument namespace
    """
    parser = ArgumentParser(formatter_class=TargetHelpFormatter)
    _attach_default_args(parser)

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


def verify_core_args(parser: ArgumentParser, args: Namespace):
    """Verifies core runtime arguments (target, and batch_size).
    If one of them doesn't match the expected value a ValueError is raised.

    Args:
        args (Namespace): An entire namespace of arguments from parser

    Raises:
        ValueError: Raised if target, or batch_size don't contain a valid value
    """
    if not args.target or args.target not in target_arg_to_type:
        parser.error(
            "Target type must be specified (--target TARGET). It's possible"
            " that such target isn't supported yet :("
        )
    if not args.batch_size or args.batch_size < 0:
        parser.error(
            "Batch size value must be specified (--batch-size SIZE) where SIZE"
            " is a POSITIVE INTEGER!"
        )
