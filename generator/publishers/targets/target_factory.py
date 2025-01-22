from argparse import Namespace

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
            args (Namespace): Argument namescape which can be used to fill target object

        Raises:
            ValueError: Raised from the target implementations if the arguments are invalid
            TypeError: Raised if the target_type does not match any existing type

        Returns:
            Target: Newly constructed target object of specific type
        """
        match target_type:
            case TargetType.console:
                return ConsoleTarget(
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                )
            case TargetType.kafka:
                return KafkaTarget(
                    bootstrap_server=args.bootstrap_server,
                    kafka_topic=args.kafka_topic,
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                    server_port=args.port,
                )
            case _:
                raise TypeError("Target was not provided or no such target exists.")
