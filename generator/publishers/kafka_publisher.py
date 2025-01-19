from .targets import KafkaTarget
from . import Publisher
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from uuid import uuid4


class KafkaPublisher(Publisher):
    """Publisher which generates data to the target via a generator function.
    So far this has required bootstrap-server, and port parameters, and will be
    expanded soon in the future (if I'm not too lazy).

    Args:
        Publisher: Base publisher implementation with validation, and stream handling
    """

    def __init__(self, generator_fun, target: KafkaTarget):
        super().__init__(generator_fun, target)
        self._producer_config = {"bootstrap.servers": target.full_server_address}
        self._producer = Producer(self._producer_config)
        self._string_serializer = StringSerializer("utf_8")

    @staticmethod
    def delivery_report(err: str, msg: str):
        """Reporting function which is called after every publish of a message to a Kafka topic

        Args:
            err (str): Error message, in case the producer fails to send the message
            msg (str): Confirmation of successful message delivery to a topic
        """
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish_batch(self):
        """Publishes a single batch of data to a kafka topic defined in the self._target

        Raises:
            TypeError: Raised if target type doesn't match KafkaTarget
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
