from typing import Any

from .console_publisher import ConsolePublisher
from .kafka_publisher import KafkaPublisher
from .publisher import Publisher
from .targets import ConsoleTarget, KafkaTarget, Target


class PublisherFactory:
    """Factory class which constructs new publishers."""

    @staticmethod
    def create_publisher(generator_func: Any, target: Target) -> Publisher:
        """The main factory method which takes in publish cli args,
        and a generator function and creates a new publisher based on these arguments.

        Args:
            target (Target): publish target to send the data to. This contains all the metadata to do that.
            generator_func (any): generator function which creates the data

        Raises:
            ValueError: Raised if arguments don't match the pattern matched publisher
            TypeError: Raised if target type doesn't match any of existing types

        Returns:
            Publisher: concrete publisher implementation
        """

        match target:
            case ConsoleTarget():
                return ConsolePublisher(generator_fun=generator_func, target=target)
            case KafkaTarget():
                return KafkaPublisher(generator_fun=generator_func, target=target)
            case _:
                raise TypeError("Target was not provided or no such target exists.")
