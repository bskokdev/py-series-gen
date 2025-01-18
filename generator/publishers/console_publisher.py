from .publisher import Publisher


class ConsolePublisher(Publisher):
    """Publisher which sends the data to the console output.

    Args:
        Publisher (Publisher):
            abstract publisher implementation. Mainly handles the instance values, and publish stream.
    """

    def publish_to_target(self):
        """Publish method which overrides the based impl., and sends data to the console output.
        We call the base impl at the end to ensure correct behaviour with the `is_stream` flag.
        """
        while self._target.is_stream:
            for value in self._generator(self._target.batch_size):
                print(value.data)
