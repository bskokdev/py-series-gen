from datetime import datetime, timedelta

from mockseries.utils import datetime_range
from mockseries.trend import LinearTrend
from mockseries.seasonality import SinusoidalSeasonality
from mockseries.noise import RedNoise
from mockseries.signal.signal import Signal

from values import TimeSeriesValue

def _define_time_series() -> Signal:
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

# TODO: add tests for this function
def time_series_generator(batch_size: int):
    """Generates time series values of size `batch_size` and yields them to the generator customer.
    we split the batch-size into chunks, this allows computer to store less data in the memory buffer
    Let's say we have 120 000 000 000 data points to generate, we don't want to store this into memory at once,
    so we store only these chunks and yield from the chunks ... it may take a bit longer, but we don't crash the program/pc

    Args:
        batch_size (int): how many values should be generated in total
    """
    
    timeseries = _define_time_series()
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
            TimeSeriesValue(timestamp=time, data=data) for time, data in zip(timestamps, data_points)
        )