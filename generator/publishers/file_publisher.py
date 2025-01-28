import csv
from typing import Generator

from values import Value

from .publisher import Publisher
from .targets import FileTarget, FileType


class FilePublisher(Publisher):
    """Publisher which handles writes to all different file types

    Args:
        Publisher: Abstract publisher implementation
    """

    def __init__(self, generator_fun: Generator[Value, None, None], target: FileTarget):
        super().__init__(generator_fun, target)

    def _write_to_csv(self):
        """Writes data generated by the generator function to file
        specified at self.file_path
        """
        with open(self._target.file_path, "a", encoding="UTF8") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            # TODO: Figure out how to handle headers
            # idea: each generator would specify the respective csv header
            for value in self._generator(self._target.batch_size):
                print(f"{value.data} written to the CSV file")
                writer.writerow(value.data)

    def publish_batch(self):
        """Overrides the abstract method which specifies the publish of a single batch.
        Each file type has different write method defined in this publisher.

        Raises:
            TypeError: raised if the file type is not matched
        """
        match self._target.file_type:
            case FileType.CSV:
                self._write_to_csv()
            case _:
                raise TypeError("FileType not supported by the publisher")
