from argparse import ArgumentParser, Namespace

import pytest
from cli.arguments import build_target_from_args, create_parser_with_all_args
from publishers.targets import ConsoleTarget, KafkaTarget, Target


@pytest.fixture
def all_args_parser_fixture() -> ArgumentParser:
    test_parser = ArgumentParser()
    test_parser.add_argument(
        "--target", dest="target", type=str, help="Destination to publish the data to"
    )
    test_parser.add_argument(
        "--batch-size",
        dest="batch_size",
        type=int,
    )
    test_parser.add_argument(
        "--stream",
        dest="is_stream",
        action="store_true",
        default=False,
    )
    test_parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
    )
    kafka_group = test_parser.add_argument_group("kafka arguments")
    kafka_group.add_argument("--bootstrap-server", dest="bootstrap_server", type=str)
    kafka_group.add_argument("--port", dest="port", type=int)
    kafka_group.add_argument("--topic", dest="kafka_topic", type=str)
    return test_parser


@pytest.fixture
def kafka_args_fixture() -> Namespace:
    return Namespace(
        target="kafka",
        batch_size=32,
        is_stream=False,
        debug=False,
        bootstrap_server="localtest",
        port=9092,
        kafka_topic="test-topic",
    )


@pytest.mark.unit_test
def test_create_parser_with_all_args(all_args_parser_fixture: ArgumentParser):
    defined_args = all_args_parser_fixture.parse_args()
    empty_args = Namespace()

    _, created_args = create_parser_with_all_args()
    assert defined_args.__eq__(created_args)
    assert not defined_args.__eq__(empty_args)
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
    created_target = build_target_from_args(ArgumentParser(), kafka_args_fixture)

    assert created_target.__eq__(expected_target)
    assert not created_target.__eq__(console_target)
