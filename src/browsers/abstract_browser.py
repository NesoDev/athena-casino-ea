from abc import ABC, abstractmethod

class Browser(ABC):
    def __init__(self):
        pass  
        
    @abstractmethod
    def initialize(self):
        pass
    
    def quit(self):
        driver = self.driver
        driver.quit()