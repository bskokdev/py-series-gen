from argparse import ArgumentParser, Namespace
from cli.arguments import build_target_from_args, create_parser_with_all_args
from publishers.publisher_factory import PublisherFactory
from generators import time_series_generator


def run(arg_parser: ArgumentParser, arguments: Namespace):
    publish_target = build_target_from_args(parser=arg_parser, args=arguments)
    publisher = PublisherFactory().create_publisher(
        generator_func=time_series_generator, target=publish_target
    )
    publisher.publish_to_target()


if __name__ == "__main__":
    arg_parser, arguments = create_parser_with_all_args()
    if arguments.debug:
        # the debug run without try except block
        run(arg_parser=arg_parser, arguments=arguments)
    else:
        try:
            run(arg_parser=arg_parser, arguments=arguments)
        except Exception as e:
            print(str(e))
