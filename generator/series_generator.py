from argparse import ArgumentParser, Namespace
from datetime import datetime
from values import TimeSeriesValue
from publishers.console_publisher import ConsolePublisher


def time_series_generator(batch_size: int):
    """
    Generator function which produces artificial time series data
    """
    for i in range(batch_size):
        val = 0.001 + i
        yield TimeSeriesValue(data=val, timestamp=datetime.now())


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    parser.add_argument('--stream', dest='stream', type=bool)  # (while True: publish)
    # TODO: add arguments for different publish targets
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    console_publisher = ConsolePublisher(time_series_generator)
    if args.stream:
        while True:
            console_publisher.publish_to_target(batch_size=args.batch_size)
    else:
        pass
