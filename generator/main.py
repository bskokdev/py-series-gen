from cli.arguments import build_target_from_args
from publishers.publisher_factory import PublisherFactory
from generators import time_series_generator


if __name__ == "__main__":
    publish_target = build_target_from_args()
    publisher = PublisherFactory().create_publisher(
        generator_func=time_series_generator,
        target=publish_target
    )
    publisher.publish_to_target()