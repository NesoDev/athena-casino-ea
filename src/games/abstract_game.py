from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, platform, connector, client):
        self._platform = platform
        self._connector = connector
        self._client = client
        
    @abstractmethod
    def setup():
        pass