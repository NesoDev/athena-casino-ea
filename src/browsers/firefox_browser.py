from src.browsers.abstract_browser import Browser
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException

class Firefox(Browser):
    def __init__(self):
        self._driver = self.initialize()

    def initialize(self):
        try:
            options_browser = Options()
            options_browser.add_argument('--headless')
            options_browser.add_argument("--disable-gpu")
            options_browser.add_argument("--no-sandbox")
            options_browser.add_argument("--disable-dev-shm-usage")
    
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options_browser)
            return driver
        except (TimeoutError, TimeoutException) as e:
            print(f"Error al iniciar Firefox: {e}")
            raise
