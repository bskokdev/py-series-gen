from abc import ABC, abstractmethod

from .targets.target import Target


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
        self._validate_publisher()

    def _validate_publisher(self):
        """Validates this every publisher, so it contains both generator function, and respective target

        Raises:
            ValueError: Raised if either the generator or target are not present in the publisher
        """
        if not self._target:
            raise ValueError("Target has to be specified for every publisher.")
        elif not self._generator:
            raise ValueError(
                "Generator has to be provided to publisher in order to generate"
                " the data"
            )

    @abstractmethod
    def publish_batch(self):
        """Abstract method for publishing a single batch to the target.
        This has to be implemented by the concrete implementations of this class.
        """
        pass

    def publish_stream(self):
        """Keeps publishing batches to the target unless the process is stopped"""
        while self._target.is_stream:
            self.publish_batch()

    def publish_to_target(self):
        """Publishes batch, or streams the batches to the target"""
        if not self._target.is_stream:
            self.publish_batch()
            return

        self.publish_stream()
