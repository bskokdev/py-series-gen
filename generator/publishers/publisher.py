from abc import ABC, abstractmethod
from typing import Generator

from values import Value

from .targets import Target


class Publisher(ABC):
    """
    Each publisher publishes some data to the given target.
    This target can be whatever ... Kafka, Database, API, etc.
    The data to publish are generated via the passed generator function reference on the go.
    """

    def __init__(self, generator_fun: Generator[Value, None, None], target: Target):
        super().__init__()
        self._target = target
        self._generator = generator_fun

    @abstractmethod
    def _publish_batch(self):
        """Abstract method for publishing a single batch to the target.
        This has to be implemented by the concrete implementations of this class.
        """
        pass

    def _publish_stream(self):
        """Keeps publishing batches to the target unless the process is stopped"""
        while self._target.is_stream:
            self._publish_batch()

    def publish_to_target(self):
        """Publishes batch, or streams the batches to the target"""
        if not self._target.is_stream:
            self._publish_batch()
            return

        self._publish_stream()
