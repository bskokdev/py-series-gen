from cli.arguments import get_args
from publishers.publisher_factory import PublisherFactory
from generators import time_series_generator


if __name__ == "__main__":
    args = get_args()
    publisher = PublisherFactory().create_publisher(
        target=args.target,
        is_stream=args.stream,
        generator_func=time_series_generator
    )
    publisher.publish_to_target(args.batch_size)