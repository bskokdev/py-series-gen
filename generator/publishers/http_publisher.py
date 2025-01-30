import logging
import time
from typing import Generator

import requests
from requests import HTTPError, Response
from requests.exceptions import ConnectionError
from values import Value

from .publisher import Publisher
from .targets import HttpTarget

logger = logging.getLogger(__name__)


class HttpPublisher(Publisher):
    """Publisher which sends the data to an endpoint URL via POST requests.

    Args:
        Publisher: Abstract publisher implementation.
    """

    def __init__(
        self,
        generator_fun: Generator[Value, None, None],
        target: HttpTarget,
        max_retries: int = 5,
        backoff_factor: int = 1,
    ):
        super().__init__(generator_fun, target)
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor

    def _compute_backoff_delay(self, response: Response, attempt: int) -> float:
        """Computes the delay the publisher should wait before attempting
        to send another request to the endpoint_url. It's possible the header
        returns Retry-After, so we prioritize this with backoff formula as fallback.

        Backoff strategy = we increase the delay between requests with each attempt.

        Args:
            response (Response): HTTP response from the server
            attempt (int): On which attempt we're on

        Returns:
            float: Calculated publisher wait time
        """
        if attempt < 0:
            return 0.0

        return float(
            response.headers.get(
                "Retry-After", self._backoff_factor * (2 ** (attempt - 1))
            )
        )

    def _send_value_to_endpoint(self, value: Value) -> Response | None:
        """Sends value's data to the server at endpoint_url via POST request.
        If the request fails, publisher attempts to re-send the request.
        After each attempt the timeout is incrementaly increated, so we don't spam the server.

        Args:
            value (Value): Value DTO with data to be published

        Raises:
            HttpError: Raised if we reach the max number of retries with an error response

        Returns:
            Response | None: Response object returned by the server
        """
        if not value:
            return

        for attempt in range(self._max_retries):
            try:
                res = requests.post(self._target.endpoint_url, json=value.data)
                if res.ok:
                    return res
                else:
                    # For each error response code, we'll try to re-send the data,
                    # however, the timeout will be incrementally increased.
                    # In case of Retry-After header, we use it instead of the incremented timeout.
                    backoff_delay = self._compute_backoff_delay(
                        response=res, attempt=attempt
                    )
                    time.sleep(backoff_delay)

                    logger.warning(
                        f"Received an error response code, trying again after: {backoff_delay} seconds"
                    )
                    res.raise_for_status()
            except HTTPError as ex:
                if attempt == self._max_retries - 1:
                    raise HTTPError(
                        f"Failed to publish data via HTTP POST to {self._target.endpoint_url} with max number of retries"
                    ) from ex
            except ConnectionError as ex:
                raise ConnectionError(
                    f"Failed to connect to {self._target.endpoint_url}, check the URL"
                ) from ex

        return None

    def _publish_batch(self):
        """Publishes a single batch to the http target with metadata defined
        in self._target object.
        """
        if not isinstance(self._target, HttpTarget):
            return

        for generated_value in self._generator(self._target.batch_size):
            try:
                response = self._send_value_to_endpoint(value=generated_value)
                logger.info(
                    f"Sent data to {self._target.endpoint_url} with response code: {response.status_code}"
                )
            except HTTPError as ex:
                # We failed to send the data with max number of retries,
                # so we don't send any more data to not spam the server
                logger.error(f"{ex}... Not sending more data")
                break
            except ConnectionError as ex:
                # Publisher has failed to connect to the endpoint_url
                logger.error(f"{ex}... Not sending more data")
                break
