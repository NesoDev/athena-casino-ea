from abc import ABC, abstractmethod

class Platform(ABC):
    def __init__(self, driver, data):
        self._driver = driver
        self._data = data
        
    @abstractmethod
    def _to():
        pass
    
    @abstractmethod
    def _refresh():
        pass
    
    @abstractmethod
    def _login():
        pass
    
    @abstractmethod
    def _logout():
        pass