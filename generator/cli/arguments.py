from argparse import ArgumentParser
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from .argument_formatter import TargetHelpFormatter
from publishers.targets import TargetFactory, TargetType, Target

# Maps a target type argument string to an actual enum class, for better typing
target_arg_to_type: Dict[str, TargetType] = defaultdict(
    None, {"console": TargetType.console, "kafka": TargetType.kafka}
)

# Maps a target type to a list of arguments specific to such type
# This is where you add specific arguments for each target type (console, kafka, etc.)
specific_target_args: Dict[TargetType, List[Tuple[str, str, Any]]] = defaultdict(
    list,
    {
        TargetType.kafka: [
            ("--bootstrap-server", "bootstrap_server", str, "Address of the broker"),
            ("--port", "port", str, "Port at which the broker process is running"),
            ("--topic", "kafka_topic", str, "Kafka topic to send the data to"),
        ]
    },
)


def _attach_default_args(parser: ArgumentParser):
    parser.add_argument(
        "--target", dest="target", type=str, help="Destination to publish the data to"
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


def create_parser_with_all_args() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=TargetHelpFormatter)
    _attach_default_args(parser)

    # Add all target-specific arguments with their target type as a prefix
    for target_type, args in specific_target_args.items():
        group = parser.add_argument_group(f"{target_type.name} specific arguments")
        for argument, variable, dtype, help_str in args:
            group.add_argument(argument, dest=variable, type=dtype, help=help_str)

    return parser


def build_target_from_args() -> Target:
    parser = create_parser_with_all_args()
    args = parser.parse_args()

    if not args.target:
        parser.error("Target type must be specified (--target TARGET)")

    target_type = target_arg_to_type[args.target]

    try:
        return TargetFactory().create_target(target_type=target_type, args=args)
    except Exception as e:
        parser.error(str(e))
