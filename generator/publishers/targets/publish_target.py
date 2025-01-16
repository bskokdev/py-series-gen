from abc import ABC, abstractmethod
from values import Value

class PublishTarget(ABC):
    @abstractmethod
    def establish_connection(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def publish(self, value: Value):
        pass
    