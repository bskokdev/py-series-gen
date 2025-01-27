from argparse import ArgumentParser, Namespace

import pytest

import cli.parser as cli_parser
from publishers.targets import ConsoleTarget, KafkaTarget


@pytest.fixture
def all_args_parser_fixture() -> ArgumentParser:
    test_parser = ArgumentParser()
    test_parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="Destination to publish the data to",
    )
    test_parser.add_argument(
        "--batch-size",
        dest="batch_size",
        type=int,
        help="Size of a single batch of data",
    )
    test_parser.add_argument(
        "--generator",
        dest="generator",
        type=str,
        help="Name of the generator functon to be used",
    )
    test_parser.add_argument(
        "--stream",
        dest="is_stream",
        action="store_true",
        default=False,
        help="Should data be streamed",
    )
    test_parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Should the program be run in the debug mode",
    )
    kafka_group = test_parser.add_argument_group("kafka arguments")
    kafka_group.add_argument(
        "--bootstrap-server",
        dest="bootstrap_server",
        type=str,
        help="kafka bootstrap server address",
    )
    kafka_group.add_argument(
        "--port", dest="port", type=int, help="Kafka bootstrap server port"
    )
    kafka_group.add_argument(
        "--topic",
        dest="kafka_topic",
        type=str,
        help="Kafka topic to publish the data to",
    )
    return test_parser


@pytest.fixture
def kafka_args_fixture() -> Namespace:
    return Namespace(
        target="kafka",
        batch_size=32,
        generator="time-series",
        is_stream=False,
        debug=False,
        bootstrap_server="localtest",
        port=9092,
        kafka_topic="test-topic",
    )


@pytest.mark.unit_test
def test_create_parser_with_all_args(all_args_parser_fixture: ArgumentParser):
    defined_args = all_args_parser_fixture.parse_args()

    _, created_args = cli_parser.create_parser_with_all_args()
    assert defined_args.__eq__(created_args)
    assert not defined_args.__eq__(Namespace())
    for arg in vars(defined_args):
        assert created_args.__contains__(arg)


@pytest.mark.unit_test
def test_build_target_from_args(kafka_args_fixture: Namespace):
    console_target = ConsoleTarget(batch_size=420, is_stream=True)
    expected_target = KafkaTarget(
        kafka_topic="test-topic",
        bootstrap_server="localtest",
        server_port=9092,
        batch_size=32,
        is_stream=False,
    )
    created_target = cli_parser.build_target_from_args(
        ArgumentParser(), kafka_args_fixture
    )

    assert created_target.__eq__(expected_target)
    assert not created_target.__eq__(console_target)
