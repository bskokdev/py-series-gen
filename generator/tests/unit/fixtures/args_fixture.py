from argparse import Namespace

import pytest


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


@pytest.fixture
def console_args_fixture() -> Namespace:
    return Namespace(
        target="console",
        batch_size=53,
        generator="time-series",
        is_stream=False,
        debug=False,
    )


@pytest.fixture
def file_args_fixture() -> Namespace:
    return Namespace(
        target="file",
        file_path="directory/file.csv",
        batch_size=53,
        generator="time-series",
        is_stream=False,
        debug=False,
    )
