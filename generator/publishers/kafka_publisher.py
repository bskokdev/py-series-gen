from .targets import KafkaTarget
from . import Publisher


class KafkaPublisher(Publisher):
    def __init__(self, generator_fun, target: KafkaTarget):
        super().__init__(generator_fun, target)

    def publish_to_target(self):
        """Publishes the generator data to the given kafka topic.

        Raises:
            TypeError: Raised if target type doesn't KafkaTarget
        """
        if not isinstance(self._target, KafkaTarget):
            raise TypeError(
                "Wrong target type provided to the kafka publisher, expecting KafkaTarget"
            )
        print(f"kafka target: {self._target}")
