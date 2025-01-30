from unittest.mock import patch

import pytest
from publishers import HttpPublisher
from publishers.targets import HttpTarget
from requests import HTTPError, Response
from values import Value


@pytest.fixture
def http_publisher() -> HttpPublisher:
    return HttpPublisher(
        generator_fun=lambda batch_s: [Value(data=[i]) for i in range(batch_s)],
        target=HttpTarget(endpoint_url="https://example.com/"),
        max_retries=4,
        backoff_factor=1,
    )


@pytest.mark.unit_test
def test_compute_backoff_delay_with_retry_after(http_publisher: HttpPublisher):
    response_with_retry_after = Response()
    response_with_retry_after.status_code = 429
    response_with_retry_after.headers = {"Retry-After": "5"}
    # retry-after header has a priority over the backoff strategy
    negative_attempt_delay = http_publisher._compute_backoff_delay(
        response=response_with_retry_after, attempt=-1
    )

    first_delay = http_publisher._compute_backoff_delay(
        response=response_with_retry_after, attempt=1
    )

    second_delay = http_publisher._compute_backoff_delay(
        response=response_with_retry_after, attempt=2
    )

    twelfth_delay = http_publisher._compute_backoff_delay(
        response=response_with_retry_after, attempt=12
    )

    assert negative_attempt_delay == 0.0
    assert first_delay == 5.0
    assert second_delay == 5.0
    assert twelfth_delay == 5.0


@pytest.mark.unit_test
def test_compute_backoff_delay_without_retry_after(http_publisher: HttpPublisher):
    valid_response = Response()
    valid_response.headers = {}
    valid_response.status_code = 200
    negative_attempt_delay = http_publisher._compute_backoff_delay(
        response=valid_response, attempt=-1
    )
    # backoff_factor * (2 ** (attempt - 1))
    # 1 * (2 ** (1 - 1)) = 1.0
    first_delay = http_publisher._compute_backoff_delay(
        response=valid_response, attempt=1
    )

    # 1 * (2 ** (2 - 1)) = 2.0
    second_delay = http_publisher._compute_backoff_delay(
        response=valid_response, attempt=2
    )
    # 1 * (2 ** (12 - 1)) = 2048.0
    twelfth_delay = http_publisher._compute_backoff_delay(
        response=valid_response, attempt=12
    )

    assert negative_attempt_delay == 0.0
    assert first_delay == 1.0
    assert second_delay == 2.0
    assert twelfth_delay == 2048.0


@pytest.mark.unit_test
def test_send_value_to_endpoint_success(http_publisher: HttpPublisher):
    mock_response = Response()
    mock_response.status_code = 200
    with patch("requests.post", return_value=mock_response):
        result = http_publisher._send_value_to_endpoint(value=Value([1, 2, 3]))
        assert result == mock_response


@pytest.mark.unit_test
def test_send_value_to_endpoint_retry(http_publisher: HttpPublisher):
    mock_response = Response()
    mock_response.status_code = 429
    # intercept the post, and sleep functions
    # set the return value of the post function
    # verity the sleep was called `_max_retries` times
    with patch("requests.post", return_value=mock_response), patch(
        "time.sleep"
    ) as mock_sleep:
        with pytest.raises(HTTPError) as exc_info:
            result = http_publisher._send_value_to_endpoint(value=Value([1, 2, 3]))
            assert result is None
            assert mock_sleep.call_count == http_publisher._max_retries

        assert (
            f"Failed to publish data via HTTP POST to {http_publisher._target.endpoint_url}"
            in str(exc_info.value)
        )
