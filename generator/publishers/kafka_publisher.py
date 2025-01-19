from .targets import KafkaTarget
from . import Publisher
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from uuid import uuid4


class KafkaPublisher(Publisher):
    def __init__(self, generator_fun, target: KafkaTarget):
        super().__init__(generator_fun, target)
        self._producer_config = {"bootstrap.servers": target.full_server_address}
        self._producer = Producer(self._producer_config)
        self._string_serializer = StringSerializer("utf_8")

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

        for value in self._generator(self._target.batch_size):
            self._producer.produce(
                topic="py-topic",
                key=self._string_serializer(str(uuid4())),
                value=value.serialize(),
                callback=self.delivery_report,
            )
        self._producer.flush()
