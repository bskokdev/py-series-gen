import pytest
from publishers import HttpPublisher
from publishers.targets import HttpTarget
from requests import Response
from values import Value


@pytest.fixture
def valid_response() -> Response:
    response = Response()
    response.headers = {}
    response.status_code = 200
    return response


@pytest.fixture
def response_with_retry_after() -> Response:
    response = Response()
    response.status_code = 429
    response.headers = {"Retry-After": "5"}
    return response


@pytest.fixture
def http_target_fixture() -> HttpTarget:
    return HttpTarget(endpoint_url="https://example.com/")


@pytest.fixture
def http_publisher_fixture(http_target_fixture: HttpTarget) -> HttpPublisher:
    return HttpPublisher(
        generator_fun=lambda batch_s: [Value(data=[i]) for i in range(batch_s)],
        target=http_target_fixture,
        max_retries=16,
        backoff_factor=2,
    )


@pytest.mark.unit_test
def test_compute_backoff_delay_with_retry_after(
    response_with_retry_after: Response, http_publisher_fixture: HttpPublisher
):
    # retry-after header has a priority over the backoff strategy
    negative_attempt_delay = http_publisher_fixture._compute_backoff_delay(
        response=response_with_retry_after, attempt=-1
    )

    first_delay = http_publisher_fixture._compute_backoff_delay(
        response=response_with_retry_after, attempt=1
    )

    second_delay = http_publisher_fixture._compute_backoff_delay(
        response=response_with_retry_after, attempt=2
    )

    twelfth_delay = http_publisher_fixture._compute_backoff_delay(
        response=response_with_retry_after, attempt=12
    )

    assert negative_attempt_delay == 0.0
    assert first_delay == 5.0
    assert second_delay == 5.0
    assert twelfth_delay == 5.0


@pytest.mark.unit_test
def test_compute_backoff_delay_without_retry_after(
    valid_response: Response,
    http_publisher_fixture: HttpPublisher,
):
    negative_attempt_delay = http_publisher_fixture._compute_backoff_delay(
        response=valid_response, attempt=-1
    )
    # backoff_factor * (2 ** (attempt - 1))
    # 2 * (2 ** (1 - 1)) = 2.0
    first_delay = http_publisher_fixture._compute_backoff_delay(
        response=valid_response, attempt=1
    )

    # 2 * (2 ** (2 - 1)) = 4.0
    second_delay = http_publisher_fixture._compute_backoff_delay(
        response=valid_response, attempt=2
    )
    # 2 * (2 ** (12 - 1)) = 4096.0
    twelfth_delay = http_publisher_fixture._compute_backoff_delay(
        response=valid_response, attempt=12
    )

    assert negative_attempt_delay == 0.0
    assert first_delay == 2.0
    assert second_delay == 4.0
    assert twelfth_delay == 4096.0
