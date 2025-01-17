from argparse import Namespace
from . import Target, TargetType, ConsoleTarget

class TargetFactory:
    """Factory class which constructs new targets based on their type."""
    @staticmethod
    def create_target(target_type: TargetType, args: Namespace) -> Target:
        match target_type:
            case TargetType.console:
                return ConsoleTarget(
                    target_type=target_type,
                    batch_size=args.batch_size,
                    is_stream=args.is_stream
                )
            case _:
                raise ValueError('Target type does not exist')