from src.browsers.abstract_browser import Browser
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException
from src.loggers.logger import Logger
import os

class Firefox(Browser):
    def __init__(self, logger: Logger):
        self._logger = logger
        self._driver = self.initialize()

    def initialize(self):
        self._logger.log("Iniciando navegador...", "BROWSER")
        try:
            options_browser = Options()
            options_browser.add_argument('--headless')
            dir_profile = os.path.join(os.path.dirname(__file__), '..', '..', 'Firefox', 'Profiles', '2bdhj2ok.athena_profile')
            options_browser.add_argument('-profile')
            options_browser.add_argument(dir_profile) 
            #service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(options=options_browser)
            self._logger.log("Navegador iniciado.", "BROWSER")
            return driver
        except (TimeoutError, TimeoutException) as e:
            print(f"Error al iniciar Firefox: {e}")
            raise
    
    def quit(self):
        driver = self._driver
        driver.quit()