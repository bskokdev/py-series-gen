from . import PublishTarget
from values import TimeSeriesValue

class ConsoleTarget(PublishTarget):
    def establish_connection(self):
        # not needed for console target
        pass
    
    def disconnect(self):
        # not needed for console target
        pass
    
    def publish(self, value: TimeSeriesValue):
        print(f'{value.timestamp} | {value.data}')