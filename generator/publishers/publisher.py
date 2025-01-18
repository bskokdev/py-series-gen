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
        """Abstract implementation of the publish method.
        If the is_stream argument == True in the target, we recurse on the method and continue the publish stream.
        Also in this method we can read all the arguments passed to the publisher (to establish connection, etc.)
        """
        if self._target.is_stream:
            self.publish_to_target()
