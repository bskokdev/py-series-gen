from dataclasses import dataclass
import datetime
from . import Value

@dataclass
class TimeSeriesValue(Value):
    """Time series value, which means a tuple object of: (timestamp, data)

    Args:
        Value: base class which represents any data object holding some data.
    """
    timestamp: datetime