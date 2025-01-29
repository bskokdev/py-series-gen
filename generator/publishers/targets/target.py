from abc import ABC, abstractmethod
from enum import Enum


class TargetType(Enum):
    CONSOLE = 1
    KAFKA = 2
    FILE = 3
    HTTP = 4


class Target(ABC):
    """This class wraps arguments, and other state required to publish the data a destination.
    Also the argument validation is done in the concrete implementations of this class.
    """

    def __init__(self, batch_size: int = 0, is_stream: bool = False):
        self.batch_size = batch_size
        self.is_stream = is_stream
        self._validate_arguments()  # The concrete class' impl will be called

    @abstractmethod
    def _validate_arguments(self):
        """Abstract function overriden by concrete implementations to validate their args"""
        if not self.batch_size or self.batch_size < 0:
            raise ValueError(
                "Batch size must be specified (--batch-size SIZE | SIZE > 0)"
            )

    def __repr__(self):
        return repr(f"<batch-size={self.batch_size}, is_stream={self.is_stream}>")

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ if type(self) == type(other) else False
