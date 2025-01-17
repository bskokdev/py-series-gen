from enum import Enum
from argparse import ArgumentParser

class TargetType(Enum):
    console = 1
    kafka = 2

class Target:
    def __init__(self, target_type: TargetType):
        self.type = target_type
        