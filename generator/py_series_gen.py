from argparse import ArgumentParser, Namespace

import cli.arguments as cli
from generators import time_series_generator
from publishers.publisher_factory import PublisherFactory


def run(arg_parser: ArgumentParser, args: Namespace):
    """Main function of the entire program which creates a target object from given arguments.
    Then a publisher is created based on that target via a factory.

    Args:
        arg_parser (ArgumentParser): An object resposible for handling CLI args
        args (Namespace): Arguments parsed by the parser (access via args.<variable>)

    Raises:
        ValueError: Raised if any of the core arguments is not provided
    """
    cli.verify_core_args(parser=arg_parser, args=args)

    publish_target = cli.build_target_from_args(parser=arg_parser, args=args)
    publisher = PublisherFactory().create_publisher(
        generator_func=time_series_generator, target=publish_target
    )
    publisher.publish_to_target()


if __name__ == "__main__":
    arg_parser, arguments = cli.create_parser_with_all_args()
    if arguments.debug:
        # the debug run without try except block
        run(arg_parser=arg_parser, args=arguments)
    else:
        try:
            run(arg_parser=arg_parser, args=arguments)
        except Exception as e:
            print(str(e))
