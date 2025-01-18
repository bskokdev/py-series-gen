from .targets import ConsoleTarget
from .publisher import Publisher


class ConsolePublisher(Publisher):
    """Publisher which sends the data to the console output.

    Args:
        Publisher (Publisher):
            abstract publisher implementation. Mainly handles the instance values, and publish stream.
    """

    def __init__(self, generator_fun, target: ConsoleTarget):
        super().__init__(generator_fun, target)

    def _publish_batch(self):
        """Publishes a single batch to the target"""
        for value in self._generator(self._target.batch_size):
            print(value.data)

    def _publish_stream(self):
        """Keeps publishing batches to the target unless the process is stopped"""
        while self._target.is_stream:
            self._publish_batch()

    def publish_to_target(self):
        """Publish method which overrides the based impl., and sends data to the console output.
        We call the base impl at the end to ensure correct behaviour with the `is_stream` flag.

        Raises:
            TypeError: Raised if target type doesn't ConsoleTarget
        """
        if not isinstance(self._target, ConsoleTarget):
            raise TypeError(
                "Wrong target type provided to the console publisher, expecting ConsoleTarget"
            )

        if self._target.is_stream:
            self._publish_stream()
        else:
            self._publish_batch()
