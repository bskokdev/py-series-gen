from abc import ABC, abstractmethod

class Publisher(ABC):
    """
    Each publisher publishes some data to the given target.
    This target can be whatever ... Kafka, Database, API, etc.
    The data to publish are generated via the passed generator function reference on the go.
    """
    def __init__(self, generator_fun, is_stream: bool = False):
        super().__init__()
        self._is_stream = is_stream
        self._generator = generator_fun
        
    @abstractmethod
    def publish_to_target(self, batch_size: int):
        """Abstract implementation of the publish method.
        In this base impl we check for the is_stream state.
        If the is_stream argument == True, we recurse on the method and continue the publish stream

        Args:
            batch_size (int): Amount of data to be sent to the target in a single publish batch.
                In case of is_stream == True, total data sent is: (n * batch_size),
                where n is the number of repetitions.
        """
        if self._is_stream:
            self.publish_to_target(batch_size)
    