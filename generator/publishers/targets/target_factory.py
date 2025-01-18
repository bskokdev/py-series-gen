from argparse import Namespace
from . import Target, TargetType, ConsoleTarget


class TargetFactory:
    """Factory class which constructs new targets based on their type."""

    @staticmethod
    def create_target(target_type: TargetType, args: Namespace) -> Target:
        """The main factory method which produces new targets of specific type,
        based on the give type and arguments.

        Args:
            target_type (TargetType): Required type of the new Target
            args (Namespace): Argument namescape which can be used to fill target object

        Raises:
            ValueError: ValueError is raised if an invalid type is passed to this function

        Returns:
            Target: Newly constructed target object of specific type
        """
        match target_type:
            case TargetType.console:
                return ConsoleTarget(
                    target_type=target_type,
                    batch_size=args.batch_size,
                    is_stream=args.is_stream,
                )
            case _:
                raise ValueError("Target type does not exist")
