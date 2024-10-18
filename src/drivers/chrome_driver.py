from drivers.abstract_driver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from src.config.settings import load_env_variable

class Chrome(Driver):
    def __init__(self):
        data_chrome = load_env_variable('DATA_DRIVERS')['chrome']
        super().__init__(data_chrome)
        self._driver = None
        self._initialize()

    def initialize(self):
        path_browser = self.data["path"]
        options_browser = self.data["options"]
        service = ChromeService(path_browser)
        driver = webdriver.Chrome(service=service, options=options_browser)
        self._driver = driver
        return self._driver
    
    def to(self, url):
        driver = self.driver
        driver.get(url)