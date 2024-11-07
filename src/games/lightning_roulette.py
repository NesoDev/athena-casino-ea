from src.loggers.logger import Logger
from src.core.lightning_roulette.strategy_functions import (
    even_and_odd,
    for_zones,
    red_and_black,
    two_groups,
)
from src.games.abstract_game import Game
from src.core.lightning_roulette.scrap_functions import (
    get_data,
    get_funplay_button,
    get_stats_button,
    need_refresh_for_blocking,
)
from src.connectors.abstract_connector import Connector
from src.clients.mongodb_client import Mongo
from src.platforms.abstract_platform import Platform
from datetime import datetime, timedelta
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from src.core.lightning_roulette.utils import resources
import pytz
import schedule
import threading
from typing import Callable


class LightningRoulette(Game):
    def __init__(self, platform: Platform, connector: Connector, client: Mongo, logger: Logger):
        super().__init__(platform, connector, client, game_id="lightning_roulette")
        url_games = self._platform._url_games
        self._url_game = url_games[self._game_id]
        self._browser = self._platform._browser
        self._driver = self._browser._driver
        self._stats_button = None
        self._is_opened_menu_data = False
        self._logger = logger
        self._timeout_work = 7200 # 2 horas
        self._init_work = 0
        self._time_work = 0
        """self._time_restart_counter = '12:00'  # 12 pm / Lima
        self._timezone = 'America/Lima'"""

    def setup(self):
        # Iniciamos la ejecución de una tarea en segundo plano
        #self.start_schedule_task(self.send_message_restart_counter)
        # Iniciamos la conexión con el clúster
        is_connect = self._client.connect()
        if is_connect:
            self._logger.log("Conexión con el clúster exitosa.", "MONGODB")
            # Seleccionamos la BD
            self._client.select_database("RoobetDB")
            self._logger.log(f"BD seleccionada correctamente.", "MONGODB")
            # Iniciamos sesión en la plataforma
            is_loggin = self._platform.login(self._url_game)
            if not is_loggin:
                self._logger.log("Se agotaron los intentos de inicio de sesión.", "ROOBET")    
                return False
            self._logger.log("Se inició sesión correctamente.", "ROOBET")
            return True
        self._logger.log("Se agotaron los intentos de conexión con el clúster.", "MONGODB")
        return False

    def loop_get_process_data(self, delay_loop: int, latest_numbers: list, data: dict):
        max_retries = 100
        while True:
            # Actualizamos el tiempo de traabajo
            self.update_timework()
            """# Verificamos el cierre cronometrado
            if self._time_work >= self._timeout_work and not self.strategies_started(data=data):
                return False"""
            # Verificamos si la sesión expiró
            need_refresh_session = need_refresh_for_blocking(driver=self._driver, delay=0.1, max_retries=max_retries, logger=self._logger)
            if need_refresh_session is None:
                return False
            if need_refresh_session:
                return True
            # Verificamos si el juego está cerrado
            """ Lógica """
            max_retries = 30
            # Verificamos si el menu de datos está abierto
            if self._is_opened_menu_data == False:
                # Buscamos y presionamos el boton estadísticas
                is_select_stats = self.press_stats(delay=0.1)
                if is_select_stats == False:
                    self._logger.log("Se agotaron los intentos para presionar button stats.", "SCRAPPER")
                    return True
                self._logger.log("Button Stats ha sido presionado.", "SCRAPER")
                self._logger.log("Abriendo menú estadísticas...", "SCRAPPER")
                self._is_opened_menu_data = True
            # Extraemos los resultados
            numbers = get_data(driver=self._driver, delay=0.1, logger=self._logger)
            # Verificamos si el menu estadísticas se abrió correctamente
            if numbers == None and self._is_opened_menu_data == True:
                self._logger.log("Se agotaron los intentos para leer los datos.", "SCRAPPER")
                # Buscamos y presionamos el boton estadísticas
                is_select_stats = self.press_stats(delay=0.1)
                if is_select_stats == False:
                    self._logger.log("Se agotaron los intentos para presionar button stats.", "SCRAPPER")
                    return True
                self._logger.log("Button Stats ha sido presionado.", "SCRAPER")
                self._logger.log("Cerrando menú estadísticas...", "SCRAPPER")
                self._is_opened_menu_data = False
                continue
            # Procesamos los resultados solo si son nuevos y correctos
            if latest_numbers != numbers and len(numbers) == 12:
                # Si en cierto caso expiró la sesión, y hubo más de un resultado nuevo
                if len(latest_numbers) == 12 and numbers[1:] != latest_numbers[:11]:
                    # Reiniciamos data
                    data = self.restart_data_shared()
                self._logger.log(f"{numbers}","SCRAPPER")
                # Actualizando data compartida
                self.update_data(data, numbers)
                latest_numbers = numbers
            # Esperamos
            time.sleep(delay_loop)

    def update_data(self, data, numbers):
        data["zones"] = for_zones(self._game_id, numbers, self._connector, self._client, data["zones"], logger=self._logger)
        data["color"] = red_and_black(self._game_id, numbers, self._connector, self._client, data["color"], logger=self._logger)
        data["parity"] = even_and_odd(self._game_id, numbers, self._connector, self._client, data["parity"], logger=self._logger)
        data["group"] = two_groups(self._game_id, numbers, self._connector, self._client, data["group"], logger=self._logger)

    def restart_data_shared(self):
        # Reinicia los datos compartidos
        return {
            "zones": self.create_empty_data(),
            "color": self.create_empty_data(),
            "parity": self.create_empty_data(),
            "group": self.create_empty_data(),
        }

    def create_empty_data(self):
        return {
            "state": 0,
            "latest_message_id": None,
            "latest_alert_id": None,
            "latest_prediction_id": None,
            "check_start_bets": False,
            "check_simple_bet": False,
            "check_double_bet": False,
            "check_triple_bet": False,
        }

    def press_stats(self, delay):
        max_retries = 5
        retry_count = 0
        # Obtenemos el botón estadísticas
        stats_button = get_stats_button(self._driver, delay=0.1, logger=self._logger)
        if stats_button is None:
            return False
        self._logger.log("'button_stats' encontrado.", "SCRAPPER")
        while retry_count < max_retries:
            try:
                # Clickamos en el botón funplay
                stats_button.click()
                return True                      
            except ElementClickInterceptedException:
                retry_count += 1
                self._logger.log(f"No se pudo seleccionar 'button stats'. Reintentando en {delay} segundos...", "ERROR")
                time.sleep(delay)
        return False

    def select_funplay(self, delay):
        max_retries = 5
        retry_count = 0
        # Obtenemos el botón funplay
        funplay_button = get_funplay_button(self._driver, delay=0.1, logger=self._logger)
        if funplay_button is None:  
            return False
        self._logger.log("Botón 'fun play' encontrado.", "SCRAPPER")
        while retry_count < max_retries:
            try:
                funplay_button.click()
                return True
            except ElementClickInterceptedException:
                self._logger.log(f"No se pudo seleccionar 'button funplay'. Reintentando en {delay} segundos...", "SCRAPPER")
                retry_count += 1
                time.sleep(delay)
        return None

    def refresh(self):
        max_retries = 5
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
    
    def strategies_started(self, data: dict):
        states = []
        for _, value in data.items():
            state = value['state']
            states.append(state)
        states = set(states)
        states = list(states)
        if len(states) == 1 and states[0] == 0:
            return False
        return True
    
    def update_timework(self):
        self._time_work = time.time() - self._init_work

    def play(self):
        # Preparamos el cliente, el conector, iniciamos sesión e ingresamos al juego
        setup_success = self.setup()
        if setup_success:
            # Empieza el ciclo principal
            latest_numbers = []
            # Data compartida
            data_shared = self.restart_data_shared()
            self._logger.log("Data compartida se ha creado.", "PROCESS")
            # Seleccionamos funplay
            is_select_funplay = self.select_funplay(delay=0.1)
            if is_select_funplay is None:
                self._logger.log("Se agotaron los intentos para seleccionar Funplay.", "SCRAPER")
            else: 
                if is_select_funplay:
                    self._logger.log("Funplay ha sido presionado.", "SCRAPER")
                else:
                    self._logger.log("Funplay no existe.", "SCRAPER")
                self._init_work = time.time()
                while True:
                    # Iniciamos el procesamiento de datos
                    continue_process = self.loop_get_process_data(delay_loop=0.1, latest_numbers=latest_numbers, data=data_shared)
                    if continue_process == False:
                        self._logger.log(f"Apagando bot luego de {self._time_work} segundos trabajando.", "CHECK WORKER") 
                        break
                    # Refrescamos la página
                    refresh_success = self.refresh()
                    if refresh_success == False:
                        self._logger.log("Se agotaron los intentos al refrescar la página.", "ERROR")
                        break
                    self._logger.log("La página se ha recargado correctamente.", "DRIVER")
                    # Esperamos a que la página esté activa nuevamente
                    self._platform.check_loader_ready(delay=0.1)
                    self._logger.log("La página está lista para usarse.", "CHECK LOADER")
                    # Actualizamos el tiempo de trabajo
                    self.update_timework()
        # Cerramos la conexión a la BD
        self._client.close()
        self._logger.log(f"La conexión al clúster ha sido cerrado.", "MONGODB")
        # Cerramos el navegador
        self._driver.quit()
        self._logger.log(f"Navegador ha sido cerrado.", "DRIVER")

    """def start_schedule_task(self, task: Callable[[], None]):
        timezone = pytz.timezone(self._timezone)
        current_time = datetime.now(timezone)
        # Asignamos el tiempo de reinicio de acuerdo con `self._time_restart_counter`
        scheduled_time = timezone.localize(
            datetime.strptime(f"{current_time.strftime('%Y-%m-%d')} {self._time_restart_counter}:00", "%Y-%m-%d %H:%M:%S")
        )
        # Si el tiempo programado ha pasado, programamos para el día siguiente
        if current_time >= scheduled_time:
            scheduled_time += timedelta(days=1)
        schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(task)
        # Iniciamos  el scheduler en un hilo independiente
        thread = threading.Thread(target=self.run_schedule)
        thread.daemon = True
        thread.start()

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def send_message_restart_counter(self):
        self._logger.log("Enviando mensaje de reinicio de contadores...", "TASK ASYNCHRONE")
        for lang, package in resources.items():
            messages = package['default_messages']
            message = messages['restart_counter']
            self._connector.send_message(message=message, lang=lang)"""