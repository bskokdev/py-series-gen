from dataclasses import dataclass
import datetime
from . import Value

@dataclass
class TimeSeriesValue(Value):
    timestamp: datetime