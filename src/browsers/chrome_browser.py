from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.browsers.abstract_browser import Browser
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException

class Chrome(Browser):
    def __init__(self):
        self._driver = self.initialize()

    def initialize(self):
        try:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except (TimeoutError, TimeoutException) as e:
            print(f"Error al iniciar Chrome: {e}")
            raise