from datetime import timedelta
from typing import Any, Generator, List
import pytest

from cli.arguments import build_target_from_args, create_parser_with_all_args
from publishers.publisher_factory import PublisherFactory
from values import Value

from testcontainers.kafka import KafkaContainer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer


@pytest.fixture
def kafka_container() -> Generator[KafkaContainer, None, None]:
    with KafkaContainer(image="confluentinc/cp-kafka:7.8.0") as kafka:
        yield kafka


def _add_kafka_topic(admin: AdminClient, topic_name: str):
    """Uses an admin kafka client to create a new topic in the broker.

    Args:
        admin (AdminClient): An object which can interact and modify Kafka
        topic_name (str): Name of the topic to be added
    """
    test_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
    admin.create_topics([test_topic])


def _run_integration():
    """This generilizes a single test run of the program"""
    arg_parser, test_args = create_parser_with_all_args()
    test_target = build_target_from_args(parser=arg_parser, args=test_args)
    publisher = PublisherFactory().create_publisher(
        generator_func=lambda batch_s: [Value(data=i) for i in range(batch_s)],
        target=test_target,
    )
    publisher.publish_to_target()


def _listen_on_topics(consumer: Consumer, topic_names: List[str]) -> List[Any]:
    """Makes a consumer listen on the specified topics. For each message read,
    there's a 5s timeout. This means poll() waits up to 5s, before returning None.
    If None is received, we return from this function.

    Args:
        consumer (Consumer): Kafka consumer which will be listening
        topic_names (List[str]): List of topics on which the consumer should listen

    Returns:
        List[Any]: List of messages polled by the consumer
    """
    consumer.subscribe(topic_names)
    received = []
    while True:
        message = consumer.poll(timeout=5.0)
        if not message:
            consumer.unsubscribe()
            return received
        received.append(message)


@pytest.mark.integration_test
def test_kafka_publisher(monkeypatch, kafka_container):
    # get_bootstrap_server() returns "address:port" str
    bootstrap_server = kafka_container.get_bootstrap_server()
    server_address, server_port = bootstrap_server.split(":")
    test_topic_name = "test-topic"

    admin_client = AdminClient({"bootstrap.servers": bootstrap_server})
    _add_kafka_topic(admin=admin_client, topic_name=test_topic_name)

    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_server,
            "group.id": "test-group",
            "auto.offset.reset": "earliest",
        }
    )

    batch_size = 1024
    args = [
        "test.py",
        "--target",
        "kafka",
        "--batch-size",
        str(batch_size),
        "--bootstrap-server",
        server_address,
        "--port",
        str(server_port),
        "--topic",
        "test-topic",
    ]
    monkeypatch.setattr("sys.argv", args)
    _run_integration()

    received = _listen_on_topics(consumer=consumer, topic_names=[test_topic_name])
    consumer.close()

    assert len(received) == batch_size


@pytest.mark.integration_test
def test_console_publisher(capsys, monkeypatch):
    batch_size = 2048
    args = ["test.py", "--target", "console", "--batch-size", str(batch_size)]

    # this modifies the runtime arguments programatically
    monkeypatch.setattr("sys.argv", args)
    _run_integration()

    # capsys spies on the std, and reads the output (.out)
    output = capsys.readouterr().out

    assert output is not None

    assert "0" in output
    assert str(batch_size - 1) in output
    assert len(output.splitlines()) == batch_size
