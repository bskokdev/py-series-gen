from argparse import ArgumentParser, Namespace

import cli.parser as cli_parser
import pytest
from publishers.targets import ConsoleTarget, FileTarget, KafkaTarget

from .fixtures import (
    all_args_parser_fixture,
    console_args_fixture,
    file_args_fixture,
    kafka_args_fixture,
)


@pytest.mark.unit_test
def test_create_parser_with_all_args(all_args_parser_fixture: ArgumentParser):
    defined_args = all_args_parser_fixture.parse_args()

    _, created_args = cli_parser.create_parser_with_all_args()
    assert defined_args.__eq__(created_args)
    assert not defined_args.__eq__(Namespace())
    for arg in vars(defined_args):
        assert created_args.__contains__(arg)


# TODO: handle invalid argument validation cases
@pytest.mark.unit_test
def test_build_kafka_target_from_args(kafka_args_fixture: Namespace):
    invalid_target = KafkaTarget(
        kafka_topic="python",
        bootstrap_server="nasa-computer",
        server_port=901,
        batch_size=100_000,
        is_stream=False,
    )
    expected_target = KafkaTarget(
        kafka_topic="test-topic",
        bootstrap_server="localtest",
        server_port=9092,
        batch_size=32,
        is_stream=False,
    )

    created_target = cli_parser.build_target_from_args(args=kafka_args_fixture)

    assert created_target
    assert created_target.__eq__(expected_target)
    assert not created_target.__eq__(invalid_target)


@pytest.mark.unit_test
def test_build_console_target_from_args(console_args_fixture: Namespace):
    invalid_target = ConsoleTarget(batch_size=123, is_stream=True)
    expected_target = ConsoleTarget(
        batch_size=53,
        is_stream=False,
    )

    created_target = cli_parser.build_target_from_args(args=console_args_fixture)

    assert created_target
    assert created_target.__eq__(expected_target)
    assert not created_target.__eq__(invalid_target)


@pytest.mark.unit_test
def test_build_file_target_from_args(file_args_fixture: Namespace):
    invalid_path_target = FileTarget(
        file_path="directory/wrong.csv", batch_size=123, is_stream=True
    )
    expected_target = FileTarget(
        file_path="directory/file.csv", batch_size=53, is_stream=False
    )

    created_target = cli_parser.build_target_from_args(args=file_args_fixture)

    assert created_target
    assert created_target.__eq__(expected_target)
    assert not created_target.__eq__(invalid_path_target)
