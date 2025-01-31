from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from generators import time_series_generator
from publishers.targets import TargetType

# Maps a target type argument string to an actual enum class, for better typing
target_arg_to_type: Dict[str, TargetType] = {
    "console": TargetType.CONSOLE,
    "kafka": TargetType.KAFKA,
    "file": TargetType.FILE,
    "http": TargetType.HTTP,
}

# Maps the name of the generator to the actual function to be called to generate the data
generator_name_to_function: Dict[str, Any] = {"time-series": time_series_generator}

T = TypeVar("T")


@dataclass
class Argument(Generic[T]):
    arg: str
    dest: str
    type: type[T]
    help: str

    def __iter__(self):
        return iter((self.arg, self.dest, self.type, self.help))


@dataclass
class Flag:
    flag: str
    dest: str
    action: str
    default: bool
    help: str

    def __iter__(self):
        return iter((self.flag, self.dest, self.action, self.default, self.help))


core_arguments: List[Argument] = [
    Argument(
        arg="--target",
        dest="target",
        type=str,
        help="Destination to publish the data to",
    ),
    Argument(
        arg="--batch-size",
        dest="batch_size",
        type=int,
        help="Single batch (iteration) size",
    ),
    Argument(
        arg="--generator",
        dest="generator",
        type=str,
        help="Name of the generator functon to be used",
    ),
]

flags: List[Flag] = [
    Flag(
        flag="--stream",
        dest="is_stream",
        action="store_true",
        default=False,
        help="Should the batch be sent repeatedly",
    ),
    Flag(
        flag="--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Should the process run in debug mode",
    ),
]

# Maps a target type to a list of arguments specific to such type
# This is where you add specific arguments for each target type
specific_target_args: Dict[TargetType, List[Argument]] = defaultdict(
    list,
    {
        TargetType.KAFKA: [
            Argument(
                arg="--bootstrap-server",
                dest="bootstrap_server",
                type=str,
                help="Address of the bootstrap server",
            ),
            Argument(
                arg="--port",
                dest="port",
                type=int,
                help="Port at which the broker process is running",
            ),
            Argument(
                arg="--topic",
                dest="kafka_topic",
                type=str,
                help="Kafka topic to send the data to",
            ),
        ],
        TargetType.FILE: [
            Argument(
                arg="--path",
                dest="file_path",
                type=str,
                help="Path of the file where the data should be published",
            ),
        ],
        TargetType.HTTP: [
            Argument(
                arg="--endpoint",
                dest="endpoint_url",
                type=str,
                help="HTTP POST endpoint url which accepts the generated data",
            ),
        ],
    },
)
