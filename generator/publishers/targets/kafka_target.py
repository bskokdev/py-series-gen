import logging

from .target import Target

logger = logging.getLogger(__name__)


class KafkaTarget(Target):
    """Target specific to the kafka publish destination.
    This class contains state which is required to publish events to Kafka broker.

    Args:
        Target: Base class with the base arguments, and state
    """

    def __init__(
        self,
        kafka_topic: str = "",
        bootstrap_server: str = "",
        server_port: int = 9092,
        batch_size: int = 0,
        is_stream: bool = False,
    ):
        self._server_address = bootstrap_server
        self._server_port = server_port
        self.full_server_address = f"{bootstrap_server}:{str(server_port)}"
        self.kafka_topic = kafka_topic
        super().__init__(batch_size=batch_size, is_stream=is_stream)

    def _validate_arguments(self):
        """Validates arguments specific to Kafka

        Raises:
            ValueError: Raised if either kafka server, or topic are not provided.
        """
        super()._validate_arguments()
        if not self._server_address:
            logger.error("Bootstrap server was empty")
            raise ValueError(
                "Bootstrap server has to be specified (--bootstrap-server ADDRESS)"
            )
        elif not self._server_port:
            logger.error("Bootstrap server port was empty")
            raise ValueError(
                "Bootstrap server's port has to be specified (--port PORT)"
            )
        elif not self.kafka_topic:
            logger.error("Kafka topic was empty")
            raise ValueError("Kafka topic has to be specified (--topic TOPIC_NAME)")

    def __repr__(self):
        return repr(
            f"<<Base: {super().__repr__()},"
            f" bootstrap_server={self.full_server_address},"
            f" kafka_topic={self.kafka_topic}>"
        )
