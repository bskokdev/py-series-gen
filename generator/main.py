from argparse import ArgumentParser, Namespace
from publishers.publisher_factory import PublisherFactory
from generators import time_series_generator

def get_args() -> Namespace:
    """Function which handles argument reading, and parsing.
    It produces the arguments namescape from which the parameters can be read.

    Returns:
        Namespace: An object from which we can access the parameters
    """
    parser = ArgumentParser()
    parser.add_argument('--target', dest='target', type=str)
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    # This flag will cause the publisher to repeatedly send the batch to the target
    parser.add_argument('--stream', dest='stream', action='store_true', default=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    publisher = PublisherFactory().create_publisher(
        target=args.target,
        is_stream=args.stream,
        generator_func=time_series_generator
    )
    publisher.publish_to_target(args.batch_size)