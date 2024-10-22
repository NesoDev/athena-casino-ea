from drivers.abstract_driver import Driver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from src.config.settings import load_env_variable

class Chrome(Driver):
    def __init__(self):
        super().__init__()
        self._driver = None
        self._initialize()

    def initialize(self):
        service = ChromeService(ChromeDriverManager().install())
        options_browser = self._options
        driver = webdriver.Chrome(service =  service, options = options_browser)
        self._driver = driver
        return self._driver