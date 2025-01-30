import cli.parser as cli
from publishers import PublisherFactory
from values import Value


def run_integration():
    """This generilizes a single test run of the program
    We don't specify the generator function in the test arguments
    as we're using custom generator for testing.
    """
    arg_parser, test_args = cli.create_parser_with_all_args()
    test_target = cli.build_target_from_args(args=test_args, parser=arg_parser)
    publisher = PublisherFactory().create_publisher(
        generator_func=lambda batch_s: [
            Value(data=[i, i + 1, i + 2]) for i in range(batch_s)
        ],
        target=test_target,
    )
    publisher.publish_to_target()
