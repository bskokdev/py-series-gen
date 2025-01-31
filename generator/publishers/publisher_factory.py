import logging
from typing import Any, Callable, Generator, Type

from .console_publisher import ConsolePublisher
from .file_publisher import FilePublisher
from .http_publisher import HttpPublisher
from .kafka_publisher import KafkaPublisher
from .publisher import Publisher
from .targets import ConsoleTarget, FileTarget, HttpTarget, KafkaTarget, Target

logger = logging.getLogger(__name__)


class PublisherFactory:
    """Factory class which constructs new publishers."""

    @staticmethod
    def _match_target_type(target: Target) -> Type[Publisher]:
        """Returns a publisher based on the target type

        Args:
            target (Target): Concrete target implementation

        Raises:
            TypeError: Raised if target cannot be matched with a publisher

        Returns:
            Type[Publisher]: Concrete publisher for the specific target type
        """
        match target:
            case ConsoleTarget():
                return ConsolePublisher
            case KafkaTarget():
                return KafkaPublisher
            case FileTarget():
                return FilePublisher
            case HttpTarget():
                return HttpPublisher
            case _:
                logger.error(
                    "Failed to build a concrete publisher, ensure it's implemented"
                )
                raise TypeError(
                    f"Target type '{type(target).__name__}' is not supported"
                )

    @staticmethod
    def create_publisher(
        generator_func: Callable[[], Generator[Any, None, None]], target: Target
    ) -> Publisher:
        """Factory method which constructs publisher with the given generator function
        based on the target type of the provided target object. This method wraps the match,
        so we don't pass generator, and target over, and over again.

        Args:
            generator_func (Callable[[], Generator[Any, None, None]]): The generator function.
            target (Target): Object containing target metadata.

        Returns:
            Publisher: Concrete publisher for the specific target type
        """
        publisher_class = PublisherFactory._match_target_type(target)
        return publisher_class(generator_fun=generator_func, target=target)
