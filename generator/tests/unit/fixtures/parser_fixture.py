from argparse import ArgumentParser

import pytest


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
    file_group = test_parser.add_argument_group("file arguments")
    file_group.add_argument(
        "--path",
        dest="file_path",
        type=str,
        help="Path of the file where the data should be published",
    )
    http_group = test_parser.add_argument_group("http arguments")
    http_group.add_argument(
        "--endpoint",
        dest="endpoint_url",
        type=str,
        help="HTTP POST endpoint url which accepts the generated data",
    )
    return test_parser
