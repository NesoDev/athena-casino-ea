from abc import ABC, abstractmethod
from src.config.settings import load_env_variable

class Driver(ABC):
    def __init__(self):
        self._options = load_env_variable('DATA_DRIVERS')['options']
        
    @abstractmethod
    def initialize(self):
        pass
    
    def quit(self):
        driver = self.driver
        driver.quit()