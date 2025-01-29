import pytest
from publishers.targets import HttpTarget


@pytest.mark.unit_test
def test_empty_endpoint_url():
    with pytest.raises(ValueError) as exc_info:
        HttpTarget(endpoint_url="", batch_size=22, is_stream=False)

    assert (
        "HTTP endpoint URL has to be specified (--endpoint HTTP_ENDPOINT_URL)"
        in str(exc_info.value)
    )


@pytest.mark.unit_test
def test_invalid_endpoint_url():
    with pytest.raises(ValueError) as exc_info:
        HttpTarget(endpoint_url="/data/random.xml", batch_size=420, is_stream=False)

    assert "HTTP endpoint URL has to be a valid URL (https://example.com)" in str(
        exc_info.value
    )


@pytest.mark.unit_test
def test_valid_endpoint_url():
    try:
        HttpTarget(endpoint_url="http://example.com", batch_size=10, is_stream=False)
    except ValueError:
        pytest.fail("Valid URL should not raise a ValueError")
