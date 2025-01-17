from .publisher import Publisher

class ConsolePublisher(Publisher):
    """Publisher which sends the data to the console output.

    Args:
        Publisher (Publisher):
            abstract publisher implementation. Mainly handles the instance values, and publish stream.
    """
    def publish_to_target(self, batch_size: int):
        """Publish method which overrides the based impl., and sends data to the console output.
        We call the base impl at the end to ensure correct behaviour with the `is_stream` flag.

        Args:
            batch_size (int): Amount of data to be sent to the the console.
        """
        for value in self._generator(batch_size):
            print(f'{value.timestamp} | {value.data}')
        
        super().publish_to_target(batch_size)