from enum import Enum

class TargetType(Enum):
    console = 1
    kafka = 2

class Target:
    def __init__(self, target_type: TargetType, batch_size: int = 0, is_stream: bool = False):
        self.type = target_type
        self.batch_size = batch_size
        self.is_stream = is_stream
    
    def __repr__(self):
        return repr(f'<type={self.type} | batch-size={self.batch_size} | is_stream={self.is_stream}>')

class ConsoleTarget(Target):
    def __init__(self, target_type, batch_size = 0, is_stream = False):
        super().__init__(target_type, batch_size, is_stream)