import logging
from urllib.parse import urlparse

from .target import Target

logger = logging.getLogger(__name__)


class HttpTarget(Target):
    """Metadata object which contains endpoint URL
    where the data will be published

    Args:
        Target: Abstract target implementation.
        Contains batch size parameter, and stream flag
    """

    def __init__(self, endpoint_url: str = "", batch_size=0, is_stream=False):
        self.endpoint_url = endpoint_url
        super().__init__(batch_size, is_stream)

    def _is_url_valid(self) -> bool:
        """Checks if the `self.endpoint_url` is a valid URL
        via urlparse function.

        Returns:
            bool: Whether the url is a valid URL
        """
        try:
            result = urlparse(self.endpoint_url)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False

    def _validate_arguments(self):
        """Validates all http related arguments.
        This implementation will be called in abstract Target class.

        Raises:
            ValueError: Raised if any of the http related args isn't valid
        """
        super()._validate_arguments()
        if not self.endpoint_url:
            logger.error("Endpoint URL was empty")
            raise ValueError(
                "HTTP endpoint URL has to be specified (--endpoint HTTP_ENDPOINT_URL)"
            )

        if not self._is_url_valid():
            logger.error(f"Endpoint path: f{self.endpoint_url} is not a valid URL")
            raise ValueError(
                "HTTP endpoint URL has to be a valid URL (https://example.com)"
            )

    def __repr__(self):
        return repr(f"<<Base: {super().__repr__()}>, endpoint_url={self.endpoint_url}>")
