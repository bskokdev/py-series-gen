from abc import ABC, abstractmethod

from .targets import PublishTarget

class Publisher(ABC):
    """
    Each publisher publishes some data to the given target.
    This target can be whatever ... Kafka, Database, API, etc.
    The data to publish are generated via the passed generator function reference on the go.
    """
    def __init__(self, generator_fun, target: PublishTarget):
        super().__init__()
        self.generator = generator_fun
        self.target = target
        
    @abstractmethod
    def publish_to_target(self, batch_size: int):
        pass
        # self.target.establish_connection()
        # for value in self.generator(batch_size):
        #     self.target.publish(value)
        # self.target.disconnect()
    