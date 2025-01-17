from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Any
from values import TimeSeriesValue
from publishers.console_publisher import ConsolePublisher
from publishers.publisher import Publisher
from datetime import datetime, timedelta

from mockseries.utils import datetime_range
from mockseries.trend import LinearTrend
from mockseries.seasonality import SinusoidalSeasonality
from mockseries.noise import RedNoise
from mockseries.signal.signal import Signal

# TODO: add support for kafka publisher (this can be just a lib wrapper)
# TODO: add arguments for different publish targets

def define_time_series() -> Signal:
    """This only defines properties of the time series we're constructing

    Returns:
        Signal: Interface representing any type of signal.
    """
    trend = LinearTrend(coefficient=2, time_unit=timedelta(days=4), flat_base=100) # long term change
    seasonality = SinusoidalSeasonality(amplitude=20, period=timedelta(days=7)) \
        + SinusoidalSeasonality(amplitude=4, period=timedelta(days=1)) # repeating pattern
    noise = RedNoise(mean=0, std=3, correlation=0.5) # random changes
    timeseries = trend + seasonality + noise
    return timeseries

# TODO: add tests for this method
def time_series_generator(batch_size: int):
    """Generates time series values of size `batch_size` and yields them to the generator customer.
    If the `batch_size` is too big (> 1024), we split it up to several chunks which are then processed separately.
    However, the data integrity remains as we compute the offset for the `start_time` using timedelta.

    Args:
        batch_size (int): how many values should be generated in total
    """
    
    timeseries = define_time_series()
    chunk_size = min(batch_size, 1024)
    for start in range(0, batch_size, chunk_size):
        end = min(start + chunk_size, batch_size)
        curr_chunk_size = end - start

        timestamps = datetime_range(
            granularity=timedelta(seconds=1),
            start_time=datetime(2025, 1, 1) + timedelta(seconds=start),
            num_points=curr_chunk_size
        )
        data_points = timeseries.generate(time_points=timestamps)

        # yield from provides better performance because it handles the iteration at the C level rather than in Python code
        yield from (
            TimeSeriesValue(time, data) for time, data in zip(timestamps, data_points)
        )

def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    # This flag will cause the publisher to repeatedly send the batch to the target
    parser.add_argument('--stream', dest='stream', action='store_true', default=False)
    return parser.parse_args()

def handle_input(args: Any, publisher: Publisher):
    if args.stream:
        while True:
            publisher.publish_to_target(batch_size=args.batch_size)
    else:
        publisher.publish_to_target(batch_size=args.batch_size)

if __name__ == "__main__":
    args = get_args()
    console_publisher = ConsolePublisher(time_series_generator)
    handle_input(args, console_publisher)
