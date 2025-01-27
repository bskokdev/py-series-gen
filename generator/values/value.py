import json
from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class Value(ABC):
    """Generic data class which represents an object holding some data."""

    data: List[str]

    def serialize(self):
        return json.dumps(self.data)
