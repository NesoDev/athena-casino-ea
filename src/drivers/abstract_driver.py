from abc import ABC, abstractmethod

class Driver(ABC):
    def __init__(self, data):
        self.data = data
        
    @abstractmethod
    def initialize(self):
        pass
    
    def quit(self):
        driver = self.driver
        driver.quit()