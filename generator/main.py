from cli.arguments import get_args, args_to_target
from publishers.publisher_factory import PublisherFactory
from generators import time_series_generator


if __name__ == "__main__":
    parser, args = get_args()
    publisher = PublisherFactory().create_publisher(
        target_arg=args.target,
        is_stream_arg=args.stream,
        generator_func=time_series_generator
    )
    publisher.publish_to_target(args.batch_size)