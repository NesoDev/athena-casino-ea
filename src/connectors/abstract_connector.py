from abc import ABC, abstractmethod

class Connector(ABC):
    def __init__(self, data):
        self._data = data
    
    @abstractmethod
    def send_message(self, message):
        pass
    
    @abstractmethod
    def remove_message(self, social_name, message_id):
        pass