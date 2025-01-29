from .publisher import Publisher
from .targets import ConsoleTarget


class ConsolePublisher(Publisher):
    """Publisher which sends the data to the console output.

    Args:
        Publisher (Publisher):
            abstract publisher implementation. Mainly handles the instance values, and publish stream.
    """

    def _publish_batch(self):
        """Publishes a single batch of data to the console target.
        Target contains only default parameters (batch-size, stream, etc.)

        Raises:
            TypeError: Raised in case of a wrong target provided to the publisher
        """
        if not isinstance(self._target, ConsoleTarget):
            raise TypeError(
                "Wrong target provided to the console publisher, expecting ConsoleTarget"
            )
        for value in self._generator(self._target.batch_size):
            print(value.data)
