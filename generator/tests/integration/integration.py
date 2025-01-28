import cli.parser as cli_parser
from publishers import PublisherFactory
from values import Value


def run_integration():
    """This generilizes a single test run of the program"""
    arg_parser, test_args = cli_parser.create_parser_with_all_args()
    test_target = cli_parser.build_target_from_args(args=test_args, parser=arg_parser)
    publisher = PublisherFactory().create_publisher(
        generator_func=lambda batch_s: [Value(data=i) for i in range(batch_s)],
        target=test_target,
    )
    publisher.publish_to_target()
