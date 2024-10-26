from abc import ABC, abstractmethod

class Platform(ABC):
    def __init__(self, browser, data):
        self._browser = browser
        self._driver = self._browser._driver
        self._data = data
        
    @abstractmethod
    def login():
        pass
    
    @abstractmethod
    def enter_credentials():
        pass

    @abstractmethod
    def submit_form():
        pass

    @abstractmethod
    def check_captcha():
        pass

    @abstractmethod
    def refresh():
        pass