import random
from datetime import datetime, timedelta

from mockseries.noise import RedNoise
from mockseries.seasonality import SinusoidalSeasonality
from mockseries.signal.signal import Signal
from mockseries.trend import LinearTrend
from mockseries.utils import datetime_range

from values import Value


def _define_time_series() -> Signal:
    """This only defines properties of the time series we're constructing

    Returns:
        Signal: Interface representing any type of signal.
    """
    # trend parameters
    trend_coefficient = random.uniform(1, 5)  # slope
    trend_time_unit = timedelta(days=random.randint(2, 7))
    flat_base = random.uniform(50, 150)  # f(x) base value

    # seasonality parameters
    amplitude1 = random.uniform(10, 30)
    period1 = timedelta(days=random.randint(5, 10))
    amplitude2 = random.uniform(2, 90)
    period2 = timedelta(days=1)

    # noise parameters
    noise_mean = 0
    noise_std = random.uniform(1, 5)  # standard deviation
    noise_correlation = random.uniform(0.1, 0.9)

    trend = LinearTrend(
        coefficient=trend_coefficient, time_unit=trend_time_unit, flat_base=flat_base
    )  # long term change

    seasonality = SinusoidalSeasonality(
        amplitude=amplitude1, period=period1
    ) + SinusoidalSeasonality(
        amplitude=amplitude2, period=period2
    )  # repeating pattern

    noise = RedNoise(
        mean=noise_mean, std=noise_std, correlation=noise_correlation
    )  # noise
    timeseries = trend + seasonality + noise
    return timeseries


def time_series_generator(batch_size: int):
    """Generates time series values of size `batch_size` and yields them to the generator customer.
    we split the batch-size into chunks, this allows computer to store less data in the memory buffer
    Let's say we have 120 000 000 000 data points to generate, we don't want to store this into memory at once,
    so we store only these chunks and yield from the chunks ... it may take a bit longer, but we don't crash the program/pc

    Args:
        batch_size (int): how many values should be generated in total
    """
    if batch_size < 0:
        return

    timeseries = _define_time_series()
    chunk_size = min(batch_size, 1024)
    for start in range(0, batch_size, chunk_size):
        end = min(start + chunk_size, batch_size)
        curr_chunk_size = end - start

        timestamps = datetime_range(
            granularity=timedelta(seconds=1),
            start_time=datetime(2025, 1, 1) + timedelta(seconds=start),
            num_points=curr_chunk_size,
        )
        data_points = timeseries.generate(time_points=timestamps)

        # yield from provides better performance because it handles the iteration at the C level rather than in Python code
        yield from (
            Value(data=(str(time_point), str(data_point)))
            for time_point, data_point in zip(timestamps, data_points)
        )
