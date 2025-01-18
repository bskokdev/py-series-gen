import os
import pytest

from generators import time_series_generator


@pytest.mark.unit
def test_time_series_gen_positive_small():
    result_10 = [val for val in time_series_generator(10)]
    assert len(result_10) == 10

    result_512 = [val for val in time_series_generator(512)]
    assert len(result_512) == 512


@pytest.mark.skipif(
    os.environ.get("CI") != "true",
    reason="Skip on local runs because it takes too long, but run in CI",
)
@pytest.mark.unit
def test_time_series_gen_positive_large():
    result_large = [val for val in time_series_generator(100_000_000)]
    assert len(result_large) == 100_000_000


@pytest.mark.unit
def test_time_series_gen_negative():
    result_neg = [val for val in time_series_generator(-10)]
    assert len(result_neg) == 0

    result_neg = [val for val in time_series_generator(-100_000_000)]
    assert len(result_neg) == 0
