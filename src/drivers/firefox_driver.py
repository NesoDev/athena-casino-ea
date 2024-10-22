from drivers.abstract_driver import Driver
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from src.config.settings import load_env_variable

class Firefox(Driver):
    def __init__(self):
        super().__init__()
        self._driver = None
        self._initialize()

    def initialize(self):
        service = FirefoxService(GeckoDriverManager().install())
        options_browser = self._options
        driver = webdriver.Firefox(service=service, options=options_browser)
        self._driver = driver
        return self._driver