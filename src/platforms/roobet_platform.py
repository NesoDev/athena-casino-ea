from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.platforms.abstract_platform import Platform
from src.core.lightning_roulette.scrap_functions import get_submit_button
from src.config.settings import load_env_variable
import time


class Roobet(Platform):
    def __init__(self, browser):
        data_roobet = load_env_variable('DATA_PLATFORMS')['roobet']
        super().__init__(browser, data_roobet)
        self._url = self._data["url"]
        self._account = self._data["account"]
        self._username = self._account["username"]
        self._password = self._account["password"]
        self._url_games = self._data["url_games"]

    def login(self, game_url):
        # Recuperamos el driver
        driver = self._driver
        # Nos dirigimos al url login
        driver.get(game_url)
        # Recuperamos las credenciales
        username = self._username
        password = self._password
        delay_refresh = 180  # 3 minutos
        while True:
            # Ingresamos las credenciales
            password_input = self.enter_credentials(username, password)
            # Enviamos las credenciales
            self.submit_form(input=password_input)
            # Verificamos la presencia de un captcha luego de 15 segundoa
            if not self.check_captcha(delay_work=5, delay=0.1):
                print(f"[CAPTCHA DETECTOR] Captcha encontrado inactivo...")
            else:
                print(f"[CAPTCHA DETECTOR] Captcha encontrado activo...")
                print(f"[CAPTCHA DETECTOR] Esperamos {delay_refresh/60} minutos para refrescar la página...")
                time.sleep(delay_refresh)
                driver.refresh()
                # Aumentamos el tiempo de espera
                delay_refresh += 60
                continue
            # Si no hay captcha, rompemos el bucle
            break

    def enter_credentials(self, username, password, delay=0.1):
        driver = self._driver
        while True:
            try:
                print("[SCRAPPER] Ingresando credenciales.")
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "auth-dialog-username"))
                )
                password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "auth-dialog-current-password"))
                )
    
                if username_input.get_attribute("value") != "":
                    username_input.clear()
                username_input.send_keys(username)
    
                if password_input.get_attribute("value") != "":
                    password_input.clear()
                password_input.send_keys(password)
    
                if (username_input.get_attribute("value") == username and
                    password_input.get_attribute("value") == password):
                    print("[SCRAPPER] Credenciales ingresadas correctamente.")
                    return password_input
                
                print("[SCRAPPER] Las credenciales no se ingresaron correctamente. Reintentando...")
            except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException) as e:
                print(f"[ERROR] El ingreso de credenciales falló. Reintentando en {delay} segundos...")
                time.sleep(delay)

    def submit_form(self, input):
        driver = self._driver
        submit_button = get_submit_button(driver, input_element=input, delay=0.1)
        print("[SCRAPPER] Enviando credencianles...")
        submit_button.click()

    def check_captcha(self, delay_work, delay):
        driver = self._driver
        #print(f"[SCRAPPER] Esperamos {delay_work} segundos para verificar la presencia de un captcha.")
        time.sleep(delay_work)
        while True:
            try:
                body = driver.find_element(By.TAG_NAME, "body")
                elements_body = body.find_elements(By.XPATH, "./*")
                divs_body = [e for e in elements_body if e.tag_name == "div"]
                latests_fourth_divs_body = divs_body[::-1][0:4:]
                divs = [div for div in latests_fourth_divs_body if div.get_attribute("role") != "presentation"]
                divs = [div for div in divs if div.get_attribute("id") not in ("intercom-container", "intercom-css-container", "intercom-modal-container", "onesignal-slidedown-container", "seon-container-dis")]
                if len(divs) == 0:
                    continue
                captcha_container = divs[0]
                style_captcha_container = captcha_container.get_attribute("style")
                opacity_captcha_container = (
                    style_captcha_container.split("opacity:")[-1]
                    .split(";")[0]
                    .strip()
                )
                if opacity_captcha_container == None or opacity_captcha_container == "":
                    continue
                #print("[SCRAPPER] Retornando resultado de la verificación de la presencia de un captcha.")
                if opacity_captcha_container == "1":
                    return True
                if opacity_captcha_container == "0":
                    return False
            except (NoSuchElementException, StaleElementReferenceException, TimeoutError ,TimeoutException, IndexError,) as e:
                print(f"[ERROR] La verificación de la presencia de un captcha falló. Reintentando en {delay} segundos...")
                time.sleep(delay)

    def refresh(self):
        # Recuperamos el driver
        driver = self._driver
        driver.refresh()
