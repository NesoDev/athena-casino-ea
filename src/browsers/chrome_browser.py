from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.browsers.abstract_browser import Browser
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from src.loggers.logger import Logger

class Chrome(Browser):
    def __init__(self, logger:Logger):
        self._logger = logger
        self._driver = self.initialize()

    def initialize(self):
        self._logger.log("Iniciando navegador...", "BROWSER")
        try:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument("--disable-webrtc")
            #service = Service(ChromeDriverManager().install())
            driver = uc.Chrome(options=options)
            self._logger.log("Navegador iniciado.", "BROWSER")
            return driver
        except (TimeoutError, TimeoutException) as e:
            self._logger.log(f"Error al iniciar Chrome: {e}", "ERROR")
            raise

    def quit(self):
        driver = self._driver
        driver.quit()