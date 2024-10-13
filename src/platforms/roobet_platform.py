from functions.lightning_roulette.scrap_functions import get_submit_button
from selenium.webdriver.support.ui import WebDriverWait  # type:ignore
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException # type:ignore
from selenium.webdriver.common.by import By  # type:ignore
from platforms.abstract_platform import Platform
import time

class Roobet(Platform):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self._platform_data = self.data['roobet']
        self._url = self._platform_data['url']
        self._account = self._platform_data['account']
        self._username = self._account['username']
        self._password = self._account['password']
        self._url_games = self._platform_data['url_games']
        
    def get_driver(self):
        return self.driver
        
    def get_platform_data(self):
        return self._platform_data

    def get_url(self):
        return self._url

    def get_account(self):
        return self._account

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_url_games(self):
        return self._url_games

    def login(self):
        driver = self.driver
        url = self.get_url()
        driver.get(url)
        username = self.get_username()
        password = self.get_password()
        attempts = 3
        delay = 10
        for attempt in range(attempts):
            try:
                time.sleep(delay)
                self.enter_credentials(username, password)
                self.submit_form(driver)
                return
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"[INFO] Error en el intento {attempt + 1}. Reintentando en {delay} segundos...")
                if attempt == attempts - 1:
                    print("[ERROR] Se han agotado los intentos. Intentando de nuevo después de 2 minutos...")
                    time.sleep(120)
                    attempts = 3
    
    def enter_credentials(self, username, password):
        driver = self.driver
        username_input = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "auth-dialog-username")))
        password_input = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "auth-dialog-current-password")))
        username_input.send_keys(username)
        password_input.send_keys(password)
    
    def submit_form(self, driver):
        submit_button = self.get_submit_button(driver, self.driver.find_element(By.ID, "auth-dialog-username"), 10)
        submit_button.click()
            
    def refresh(self):
        driver = self.driver
        driver.refresh()        