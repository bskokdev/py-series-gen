import json
from abc import ABC
from dataclasses import dataclass
from typing import Any, Tuple


@dataclass
class Value(ABC):
    """Generic data class which represents an object holding some data."""

    data: Tuple[str, ...]

    def serialize(self):
        return json.dumps(self.data)
