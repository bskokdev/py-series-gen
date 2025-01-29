from argparse import Namespace

from publishers.targets.file_target import FileTarget

from .console_target import ConsoleTarget
from .kafka_target import KafkaTarget
from .target import Target, TargetType


class TargetFactory:
    """Factory class which constructs new targets based on their type."""

    @staticmethod
    def create_target(target_type: TargetType, args: Namespace) -> Target:
        """The main factory method which produces new targets of specific type,
        based on the give type and arguments. Argument validation is done
        in the concrete target implementations using validator functions.

        Args:
            target_type (TargetType): Required type of the new Target
            args (Namespace): Argument namespace used to fill target object

        Raises:
            ValueError: Raised from the target if the arguments are invalid
            TypeError: Raised if the type does not match any existing target

        Returns:
            Target: Newly constructed target object of specific type
        """
        match target_type:
            case TargetType.CONSOLE:
                return ConsoleTarget(
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                )
            case TargetType.KAFKA:
                return KafkaTarget(
                    bootstrap_server=args.bootstrap_server,
                    kafka_topic=args.kafka_topic,
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                    server_port=args.port,
                )
            case TargetType.FILE:
                return FileTarget(
                    file_path=args.file_path,
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                )
            case _:
                raise TypeError(
                    f"Target type '{target_type}' is not supported or no such target exists."
                )
