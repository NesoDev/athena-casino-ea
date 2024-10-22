from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, platform, connector, client, game_id):
        self._game_id = game_id
        self._platform = platform
        self._connector = connector
        self._client = client
        
    @abstractmethod
    def setup():
        pass