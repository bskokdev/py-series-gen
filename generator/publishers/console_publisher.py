from .publisher import Publisher

class ConsolePublisher(Publisher):
    def publish_to_target(self, batch_size):
        for value in self.generator(batch_size):
            print(f'{value.timestamp} | {value.data}')