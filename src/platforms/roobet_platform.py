from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.platforms.abstract_platform import Platform
from src.core.lightning_roulette.scrap_functions import get_submit_button
from src.config.settings import load_env_variable
import time

class Roobet(Platform):
    def __init__(self, browser, logger):
        data_roobet = load_env_variable('DATA_PLATFORMS')['roobet']
        super().__init__(browser, data_roobet)
        self._url = self._data["url"]
        self._account = self._data["account"]
        self._username = self._account["username"]
        self._password = self._account["password"]
        self._url_games = self._data["url_games"]
        self._logger = logger
        self.max_captcha_resolution_time = 60 #60 segundos

    def login(self, game_url):
        # Nos dirigimos al url login
        self._driver.get(game_url)
        self._logger.log(f"Estamos en {game_url}...", "DRIVER")
        max_retries = 2
        retry_count = 0
        while self._driver.current_url == "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login" and retry_count < max_retries:
            retry_login = False
            # Esperamos que carge la página
            is_ready = self.check_loader_ready(delay=0.1)
            if is_ready == False:
                self._logger.log("Página demoró más de lo normal.", "CHECK LOADER")
                return False
            self._logger.log("Página lista para iniciar sesión.", "CHECK LOADER")
            # Obtenemos los inputs
            username_input, password_input = self.obtain_inputs()
            self._logger.log("Inputs 'username' y 'password' encontrados.", "SCRAPPER")
            # Ingresamos las credenciales
            is_input_credentials = self.enter_credentials(username_input, password_input)
            if is_input_credentials == False:
                self._logger.log("Se agotaron los intentos para ingresar las credenciales.", "SCRAPPER")
                return False
            self._logger.log("Credenciales ingresadas correctamente.", "SCRAPPER")
            # Enviamos las credenciales
            is_select_submit_button = self.press_submit_button(password_input, delay=0.1)
            if is_select_submit_button == False:
                self._logger.log("Se agotaron los intentos para seleccionar 'submit_button'", "ERROR")
                return False
            self._logger.log("Se presionó 'submit_button' correctamente.", "DRIVER")
            self._logger.log("Enviando credenciales...", "DRIVER")
            # Verificamos la presencia de un captcha
            self._logger.log("Verificando la presencia de un captcha...", "CAPTCHA DETECTOR")
            is_resolve_captcha = None
            captcha_start_time = time.time()
            while self._driver.current_url != "https://roobet.com/game/evolution:lightning_roulette":
                elapsed_time = time.time() - captcha_start_time
                if elapsed_time > self.max_captcha_resolution_time:
                    self._logger.log("El tiempo para resolver el captcha ha excedido el límite", "CAPTCHA DETECTOR")
                    return False
                is_active_captcha = self.check_captcha(delay_work=1, delay=0.1)
                if is_active_captcha:
                    if is_resolve_captcha is None:
                        is_resolve_captcha = False
                        self._logger.log("Captcha activo", "CAPTCHA DETECTOR")
                    self._logger.log("Resolviendo...", "CAPTCHA DETECTOR")
                elif self._driver.current_url == "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login":
                    password_input = self.obtain_input_password()
                    if password_input.get_attribute('value') == "":
                        self._logger.log("Resolución de captcha desaprobada", "CAPTCHA DETECTOR")
                        retry_login = True
                        break
            if retry_login:
                retry_count += 1
                continue
            if is_resolve_captcha is None:
                self._logger.log("Captcha inactivo", "CAPTCHA DETECTOR")
            else:
                self._logger.log("Resolución de captcha aprobada", "CAPTCHA DETECTOR")
            self._logger.log("Continuamos con el juego...", "CAPTCHA DETECTOR")
            break
        if retry_count >= max_retries:
            return False
        return True

    def check_loader_ready(self, delay):
        self._logger.log("Esperando que el loader esté listo...", "SCRAPPER")
        dt_max = 30 # 30 segundos
        dt = 0
        t0 = time.time()
        while dt < dt_max:
            try:
                loader = self._driver.find_element(By.ID, "loader")
                if loader.get_attribute("class") == "ready":
                    return True
            except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException) as e:
                dt = time.time() - t0
                self._logger.log(f"No se encontró el loader. Reintentando en {delay} segundos...", "ERROR")
                time.sleep(delay)
        return False
    
    def obtain_input_username(self, delay=0.1):
        while True:
            try:
                username_input = WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.ID, "auth-dialog-username"))
                )
                if username_input:
                    return username_input
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                self._logger.log(f"No se encontró el input de usuario. Reintentando en {delay} segundos...", "ERROR")
                time.sleep(delay)

    def obtain_input_password(self, delay=0.1):
        while True:
            try:
                password_input = WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.ID, "auth-dialog-current-password"))
                )
                if password_input:
                    return password_input
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                self._logger.log(f"No se encontró el input de contraseña. Reintentando en {delay} segundos...", "ERROR")
                time.sleep(delay)

    def obtain_inputs(self, delay=0.1):
        self._logger.log("Buscando inputs...", "SCRAPPER")
        username_input = self.obtain_input_username(delay)
        password_input = self.obtain_input_password(delay)
        return username_input, password_input
    
    def enter_credentials(self, username_input, password_input, delay=0.1):
        self._logger.log("Ingresando credenciales...", "SCRAPPER")
        max_retries = 5
        retries_count = 0
        while retries_count < max_retries:
            try:
                if username_input.get_attribute("value") != "":
                    username_input.clear()
                username_input.send_keys(self._username)
                if password_input.get_attribute("value") != "":
                    password_input.clear()
                password_input.send_keys(self._password)
                if (username_input.get_attribute("value") == self._username and
                    password_input.get_attribute("value") == self._password):
                    return True
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                retries_count += 1
                self._logger.log(f"El ingreso de credenciales falló. Reintentando en {delay} segundos...", "ERROR")
            time.sleep(delay)
        return False
    
    def press_submit_button(self, password_input, delay=0.1):
        submit_button = get_submit_button(self._driver, password_input, delay, self._logger)
        max_retries = 5
        retry_count = 0
        if submit_button is not None:
            while retry_count < max_retries:
                try:
                    # Seleccionamos submit_button
                    submit_button.click()
                    return True                      
                except ElementClickInterceptedException:
                    retry_count += 1
                    self._logger.log(f"No se pudo seleccionar 'submit_button'. Reintentando en {delay} segundos...", "ERROR")
                    time.sleep(delay)
        return False

    def check_captcha(self, delay_work=0, delay=0.1):
        time.sleep(delay_work)
        while True:
            try:
                body = self._driver.find_element(By.TAG_NAME, "body")
                elements_body = body.find_elements(By.XPATH, "./*")
                divs_body = [e for e in elements_body if e.tag_name == "div"]
                latests_fourth_divs_body = divs_body[::-1][0:4:]
                divs = [div for div in latests_fourth_divs_body if div.get_attribute("role") != "presentation"]
                divs = [div for div in divs if div.get_attribute("id") not in ("intercom-container", "intercom-css-container", "intercom-modal-container", "onesignal-slidedown-container", "seon-container-dis", "balanceMenu", "intercom-frame")]
                if len(divs) == 0:
                    continue
                captcha_container = divs[0]
                style_captcha_container = captcha_container.get_attribute("style")
                visibility_captcha_container = (
                    style_captcha_container.split("visibility:")[-1]
                    .split(";")[0]
                    .strip()
                )
                if visibility_captcha_container == None or visibility_captcha_container == "":
                    continue
                opacity_captcha_container = (
                    style_captcha_container.split("opacity:")[-1]
                    .split(";")[0]
                    .strip()
                )
                if opacity_captcha_container == None or opacity_captcha_container == "":
                    continue
                if visibility_captcha_container == "visible" and opacity_captcha_container == "1":
                    return True
                if visibility_captcha_container == "hidden" and opacity_captcha_container == "0":
                    return False
            except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
                self._logger.log(f"La verificación de la presencia de un captcha falló. Reintentando en {delay} segundos...", "ERROR")
                time.sleep(delay)
    
    def refresh(self):
        max_retries = 3
        retry_count = 0
        self._logger.log("Recargando página...", "DRIVER")
        while retry_count < max_retries:
            try:
                self._driver.refresh()
                self._is_opened_menu_data = False
                return True
            except TimeoutException:
                retry_count += 1
                time.sleep(5)
        return False
