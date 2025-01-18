from . import Target


class KafkaTarget(Target):
    """Target specific to the kafka publish destination.
    This class contains state which is required to publish events to Kafka broker.

    Args:
        Target: Base class with the base arguments, and state
    """

    def __init__(
        self,
        kafka_topic: str,
        bootstrap_server: str,
        server_port: int,
        batch_size: int = 0,
        is_stream: bool = False,
    ):
        self.bootstrap_server = bootstrap_server
        self.server_port = server_port
        self.kafka_topic = kafka_topic
        super().__init__(batch_size=batch_size, is_stream=is_stream)

    def _validate_arguments(self):
        """Validates arguments specific to Kafka

        Raises:
            ValueError: Raised if either kafka server, or topic are not provided.
        """
        if not self.bootstrap_server:
            raise ValueError(
                "Kafka bootstrap server has to be specified (--bootstrap-server ADDRESS)"
            )
        elif not self.kafka_topic:
            raise ValueError("Kafka topic has to be specified (--topic TOPIC_NAME)")
        elif not self.server_port:
            raise ValueError("Kafka broker port has to be specified (--port PORT)")

    def __repr__(self):
        return repr(
            f"<Base: {super().__repr__()}, bootstrap_server={self.bootstrap_server}, server_port={self.server_port}, kafka_topic={self.kafka_topic}>"
        )
