from .targets import KafkaTarget
from . import Publisher
from confluent_kafka import Producer


class KafkaPublisher(Publisher):
    def __init__(self, generator_fun, target: KafkaTarget):
        super().__init__(generator_fun, target)
        self._producer_config = {"bootstrap.servers": self._target.full_server_address}
        self._producer = Producer(self._producer_config)

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish_to_target(self):
        """Publishes the generator data the kafka topic defined in the self._target

        Raises:
            TypeError: Raised if target type doesn't KafkaTarget
        """
        if not isinstance(self._target, KafkaTarget):
            raise TypeError(
                "Wrong target type provided to the kafka publisher, expecting KafkaTarget"
            )

        for _ in self._generator(self._target.batch_size):
            self._producer.produce(
                "py-topic",
                "test message",
                callback=self.delivery_report,
            )
        self._producer.flush()
