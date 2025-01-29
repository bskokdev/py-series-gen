from urllib.parse import urlparse

from .target import Target


class HttpTarget(Target):
    def __init__(self, endpoint_url: str, batch_size=0, is_stream=False):
        self.endpoint_url = endpoint_url
        super().__init__(batch_size, is_stream)

    def _is_url_valid(self) -> bool:
        try:
            result = urlparse(self.endpoint_url)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False

    def _validate_arguments(self):
        super()._validate_arguments()
        if not self.endpoint_url:
            raise ValueError(
                "HTTP endpoint URL has to be specified (--endpoint HTTP_ENDPOINT_URL)"
            )

        if not self._is_url_valid():
            raise ValueError("HTTP endpoint URL has to be a valid URL")
