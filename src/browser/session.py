from selenium.webdriver.support.ui import WebDriverWait  # type:ignore
from selenium.webdriver.support import expected_conditions as EC  # type:ignore
from selenium.webdriver.common.by import By  # type:ignore
import os
import json

class Session:
    def __init__(self, driver):
        """
        Inicializa la sesión del navegador.

        :param driver: Instancia del driver de Selenium para el navegador.
        """
        self.driver = driver
        self.data_casinos = json.loads(os.environ.get('DATA_CASINOS'))
        self.urls_casinos = {casino['url']: casino['name'] for casino in self.data_casinos.values()}
    
    def _login(self, url) -> bool:
        """
        Inicia sesión en el casino correspondiente basado en la URL.

        :param url: URL del casino en el que se quiere iniciar sesión.
        :return: True si el inicio de sesión fue exitoso, False de lo contrario.
        :raises ValueError: Si el casino no es compatible.
        """
        name_casino = self.urls_casinos[url]
        match(name_casino):
            case "roobet": 
                result = self._login_roobet(self.driver)
            case _: 
                raise ValueError(f"Unsupported casino: {name_casino}")
        return result

    def _login_roobet(self, driver) -> bool:
        """
        Realiza el proceso de inicio de sesión en Roobet.

        :param driver: Instancia del driver de Selenium para el navegador.
        :return: True si el inicio de sesión fue exitoso, False de lo contrario.
        """
        account_roobet = self.data_casinos['roobet']['account']
        username = account_roobet['username']
        password = account_roobet['password']
        result = True
        try: 
            username_input = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "auth-dialog-username"))
            )
            password_input = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "auth-dialog-current-password"))
            )
            username_input.send_keys(username)
            password_input.send_keys(password)
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[5]/div[3]/div/div/div/div[2]/div/form/div[3]/button",
                    )
                )
            )
            submit_button.click()
        except Exception as e:
            result = False
        finally:
            return result