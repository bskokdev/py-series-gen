from abc import ABC, abstractmethod

from .targets import Target


class Publisher(ABC):
    """
    Each publisher publishes some data to the given target.
    This target can be whatever ... Kafka, Database, API, etc.
    The data to publish are generated via the passed generator function reference on the go.
    """

    def __init__(self, generator_fun, target: Target):
        super().__init__()
        self._target = target
        self._generator = generator_fun

    @abstractmethod
    def publish_to_target(self):
        """Abstract publish method"""
        pass
