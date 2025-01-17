from abc import ABC
from dataclasses import dataclass

@dataclass
class Value(ABC):
    """Generic data class which represents an object holding some data."""
    data: str | int | float | bool