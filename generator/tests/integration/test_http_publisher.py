from collections import defaultdict

import pytest
from pytest_httpserver import HTTPServer
from werkzeug import Request, Response

from .integration import run_integration


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("localhost", 8182)


@pytest.mark.integration_test
def test_http_publisher(monkeypatch, httpserver: HTTPServer):
    batch_size = 1024
    for _ in range(batch_size):
        httpserver.expect_request("/test_data", method="POST").respond_with_response(
            Response(status=200)
        )

    http_endpoint = f"http://{httpserver.host}:{httpserver.port}/test_data"
    args = [
        "test.py",
        "--target",
        "http",
        "--endpoint",
        http_endpoint,
        "--batch-size",
        str(batch_size),
    ]
    monkeypatch.setattr("sys.argv", args)
    run_integration()

    assert (
        len(httpserver.log) == 1024
    ), f"Expected 1024 requests, but got {len(httpserver.log)}"

    for i, request in enumerate(httpserver.log):
        assert request[0].method == "POST"
        assert request[0].path == "/test_data"
        assert request[0].json == [i, i + 1, i + 2]


@pytest.mark.integration_test
def test_http_publisher_with_retries(monkeypatch, httpserver: HTTPServer):
    batch_size = 16
    retryable_status_codes = [429, 500]

    # tracks the number of attempts for each request
    # maps request id to number of attempts
    attempt_counts = defaultdict(int)

    def handler(request: Request) -> Response:
        """Custom http handler which for the first 2 responses returns error codes
        that will trigger a retry from the HttpPublisher

        Args:
            request (Request): Http request sent to the server

        Returns:
            Response: Response with custom status code
        """
        request_id = request.get_data(as_text=True)
        attempt_counts[request_id] += 1

        # in the first 2 attempts we want to return retryable error codes
        if attempt_counts[request_id] <= 2:
            return Response(
                status=retryable_status_codes[
                    attempt_counts[request_id] % len(retryable_status_codes)
                ]
            )
        # on the third attempt the server returns 200
        else:
            return Response(status=200)

    httpserver.expect_request("/test_data", method="POST").respond_with_handler(handler)

    http_endpoint = f"http://{httpserver.host}:{httpserver.port}/test_data"
    args = [
        "test.py",
        "--target",
        "http",
        "--endpoint",
        http_endpoint,
        "--batch-size",
        str(batch_size),
    ]
    monkeypatch.setattr("sys.argv", args)
    run_integration()

    assert (
        len(httpserver.log) == 3 * batch_size
    ), f"Expected {3 * batch_size} requests (including retries), but got {len(httpserver.log)}"

    # we need to verify that no data was lost during the retries
    successful_requests = [
        request for request in httpserver.log if request[1].status_code == 200
    ]
    assert (
        len(successful_requests) == batch_size
    ), f"Expected {batch_size} successful requests, but got {len(successful_requests)}"

    for i, request in enumerate(successful_requests):
        assert request[0].method == "POST"
        assert request[0].path == "/test_data"
        assert request[0].json == [i, i + 1, i + 2]
