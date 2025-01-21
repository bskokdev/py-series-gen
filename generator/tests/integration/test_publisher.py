import pytest

from cli.arguments import build_target_from_args, create_parser_with_all_args
from publishers.publisher_factory import PublisherFactory
from values import Value

from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="function")
def kafka_container():
    with KafkaContainer(image="docker.io/bitnami/kafka:2.8") as kafka:
        yield kafka


# TODO: figure out how to make integration tests work with the kafka client, and testcontainers
# @pytest.mark.integration_test
# def test_kafka_publisher(monkeypatch):
#     batch_size = 1024
#     args = [
#         "test.py",
#         "--target",
#         "kafka",
#         "--batch-size",
#         str(batch_size),
#         "--bootstrap-server",
#         "localhost",
#         "port",
#         "9092",
#         "--topic",
#         "test-topic",
#     ]
#     monkeypatch.setattr("sys.argv", args)

#     arg_parser, test_args = create_parser_with_all_args()
#     test_target = build_target_from_args(parser=arg_parser, args=test_args)
#     publisher = PublisherFactory().create_publisher(
#         generator_func=lambda batch_s: [Value(data=i) for i in range(batch_s)],
#         target=test_target,
#     )
#     publisher.publish_to_target()


@pytest.mark.integration_test
def test_console_publisher(capsys, monkeypatch):
    batch_size = 2048
    args = ["test.py", "--target", "console", "--batch-size", str(batch_size)]

    # this modifies the runtime arguments programatically
    monkeypatch.setattr("sys.argv", args)

    arg_parser, test_args = create_parser_with_all_args()
    test_target = build_target_from_args(parser=arg_parser, args=test_args)
    publisher = PublisherFactory().create_publisher(
        generator_func=lambda batch_s: [Value(data=i) for i in range(batch_s)],
        target=test_target,
    )
    publisher.publish_to_target()

    # capsys spies on the std, and reads the output (.out)
    output = capsys.readouterr().out

    assert output is not None

    assert "0" in output
    assert str(batch_size - 1) in output
    assert len(output.splitlines()) == batch_size
