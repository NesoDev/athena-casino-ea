from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class BrowserDriver:
    def __init__(self, config):
        self.config = config
        self._initialize()

    def _initialize(self):
        name_browser = self.config["name"].lower()
        path_browser = self.config["path"]
        options_browser = self.config["options"]
        match (name_browser):
            case "chrome":
                service = ChromeService(path_browser)
                driver = webdriver.Chrome(service=service, options=options_browser)
            case "firefox":
                service = FirefoxService(path_browser)
                driver = webdriver.Firefox(service=service, options=options_browser)
            case _:
                raise ValueError(f"Unsupported browser: {name_browser}")
        return driver

    def getConfig(self):
        return self.config

    def __str__(self):
        return f"{self.config['name']}\n{self.config['path']}\n{self.config['options']}"