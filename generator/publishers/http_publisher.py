import logging
from time import sleep
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

    def __init__(self, generator_fun: Generator[Value, None, None], target: HttpTarget):
        super().__init__(generator_fun, target)
        self._max_retries = 5
        self._backoff_factor = 1
        self._status_forcelist = [429, 500, 502, 503, 504]

    def _compute_backoff_delay(self, response: Response, attempt: int) -> float:
        """Computes the delay the publisher should wait before attempting
        to send another request to the endpoint_url. It's possible the header
        returns Retry-After, so we prioritize this with backoff formula as fallback.

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
            ConnectionError: Raised if we reach the max number of retries with an error response

        Returns:
            Response | None: Response object returned by the server
        """
        if not value:
            return

        for attempt in range(self._max_retries):
            try:
                res = requests.post(self._target.endpoint_url, json=value.data)
                if res.status_code == 200:
                    return res
                elif res.status_code in self._status_forcelist:
                    sleep(self._compute_backoff_delay(response=res, attempt=attempt))
                else:
                    sleep(self._compute_backoff_delay(response=res, attempt=attempt))
                    res.raise_for_status()
            except HTTPError as e:
                if attempt == self._max_retries - 1:
                    logger.warning("Reached max number of retries with an error status")
                    raise ConnectionError(
                        f"Failed to publish data via HTTP to {self._target.endpoint_url}: {e}"
                    )

        return None

    def _publish_batch(self):
        """Publishes a single batch to the http target with metadata defined
        in self._target object.
        """
        if not isinstance(self._target, HttpTarget):
            return

        for generated_value in self._generator(self._target.batch_size):
            response = self._send_value_to_endpoint(value=generated_value)
            logger.info(
                f"Sent data to {self._target.endpoint_url} with response code: {response.status_code}"
            )
