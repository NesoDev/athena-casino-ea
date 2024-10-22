from core.lightning_roulette.scrap_functions import get_submit_button
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from platforms.abstract_platform import Platform
import time
from src.config.settings import load_env_variable

class Roobet(Platform):
    def __init__(self, driver):
        data_roobet = load_env_variable('DATA_PLATFORMS')['roobet']
        super().__init__(driver, data_roobet)
        self._platform_data = self._data['roobet']
        self._url = self._platform_data['url']
        self._account = self._platform_data['account']
        self._username = self._account['username']
        self._password = self._account['password']
        self._url_games = self._platform_data['url_games']
        
    def login(self):
        # Recuperamos el driver
        driver = self._driver
        # Nos dirigimos al url login
        driver.get(self._url)
        # Recuperamos las credenciales
        username = self.get_username()
        password = self.get_password()
        delay_refresh = 180 # 3 minutos
        while True:
            # Ingresamos las credenciales
            self.enter_credentials(username, password)
            # Enviamos las credenciales
            self.submit_form(driver)
            # Verificamos la presencia de un captcha luego de 10 segundos
            present_captcha = self.check_captcha(driver=self._driver, delay_work=10)
            # Si hay un captcha esperamos 3 minutos, luego refrescamos la página
            if present_captcha:
                time.sleep(delay_refresh)
                self._driver.refresh()
                continue
            # Si no hay captcha, rompemos el bucle
            break
    
    def enter_credentials(self, username, password, delay=0.1):
        while True:
            try:
                print("[SCRAPPER] Ingresando credenciales.")
                username_input = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.ID, "auth-dialog-username")))
                password_input = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.ID, "auth-dialog-current-password")))
                username_input.send_keys(username)
                password_input.send_keys(password)
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"[ERROR] El ingreso de credenciales falló. Reintentando en {delay} segundos...")
                time.sleep(delay)
    
    def submit_form(self, driver):
        submit_button = get_submit_button(driver, self.driver.find_element(By.ID, "auth-dialog-username"), 10)
        submit_button.click()

    def check_captcha(driver, delay: 0.1, delay_work):
        time.sleep(delay_work)
        while True:
            try:
                print("[SCRAPPER] Verificando la presencia de un captcha.")
                captcha_container = driver.find_elements(By.XPATH, "./*")[-1]
                style_captcha_container = captcha_container.get_attribute("style")
                visibility_captcha_container = style_captcha_container.split("visibility:")[-1].split(";")[0].strip()
                print("[SCRAPPER] Retornando resultado de la verificación de la presencia de un captcha.")
                if visibility_captcha_container == "visible":
                    return True
                return False
            except (NoSuchElementException, StaleElementReferenceException, IndexError) as e:
                print(f"[ERROR] La verificación de la presencia de un captcha falló. Reintentando en {delay} segundos...")
                time.sleep(delay)
            
    def refresh(self):
        driver = self.driver
        driver.refresh()        