from src.core.lightning_roulette.strategy_functions import (
    even_and_odd,
    for_zones,
    red_and_white,
    two_groups,
)
from src.games.abstract_game import Game
from src.core.lightning_roulette.scrap_functions import (
    check_session_expired,
    get_data,
    get_funplay_button,
    get_stats_button,
)
from src.connectors.abstract_connector import Connector
from src.clients.mongodb_client import Mongo
from src.platforms.abstract_platform import Platform
from datetime import datetime
import time
from selenium.common.exceptions import ElementClickInterceptedException


class LightningRoulette(Game):
    def __init__(self, platform: Platform, connector: Connector, client: Mongo):
        super().__init__(platform, connector, client, game_id="lightning_roulette")
        url_games = self._platform._url_games
        self._url_game = url_games[self._game_id]
        self._browser = self._platform._browser
        self._driver = self._browser._driver
        self._stats_button = None
        self._is_clicked_stats_button = False

    def setup(self):
        # Iniciamos la conexión al cluster
        self._client.connect()
        # Seleccionamos una base de datos
        self._client.select_database("RoobetDB")
        # Iniciamos sesión en la plataforma
        self._platform.login(self._url_game)

    def loop_get_process_data(self, delay_loop: int, latest_numbers: list, data: dict):
        # Si estadísticas aún no fue presionado
        if not self._is_clicked_stats_button:
            # Presionamos estadísticas
            self.press_stats(delay=0.1)
        while True:
            # Verificamos si la sesión expiró
            if check_session_expired(driver=self._driver, delay=0.1):
                print(f"\n\n[SESSION] La sesión expiró por inactividad a las {datetime.now()}. Recargando página....\n\n")
                break
            # Extraemos los resultados
            numbers = get_data(driver=self._driver, delay=0.1)
            # Verificamos si el contenedor de estadísticas está vacío
            if numbers is None:
                # Cerramos estadísticas
                self.press_stats(delay=0.1)
                # Reabrimos estadísticas
                self.press_stats(delay=0.1)
                continue
            # Procesamos los resultados solo si son nuevos y correctos
            if latest_numbers != numbers and len(numbers) == 12:
                # Si en cierto caso expiró la sesión, y hubo más de un resultado nuevo
                if len(latest_numbers) == 12 and numbers[1:] != latest_numbers[:11]:
                    # Reiniciamos data
                    data = self.restart_data_shared()
                print(f"Datos extraídos a las {datetime.now()}: {numbers} ----")
                # Procesamos los datos en base a las estrategias y actualizamos latest_numbers
                self.update_data(data, numbers)
                latest_numbers = numbers
            # Esperamos
            time.sleep(delay_loop)

    def update_data(self, data, numbers):
        data["zones"] = for_zones(self._game_id, numbers, self._connector, self._client, data["zones"])
        data["color"] = red_and_white(self._game_id, numbers, self._connector, self._client, data["color"])
        data["parity"] = even_and_odd(self._game_id, numbers, self._connector, self._client, data["parity"])
        data["group"] = two_groups(self._game_id, numbers, self._connector, self._client, data["group"])

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
        while True:
            try:
                # Obtenemos y clickeamos en el botón estadísticas
                stats_button = get_stats_button(self._driver, delay=0.1)
                print("[SCRAPER] StatsButton ha sido presionado")
                stats_button.click()
                self._is_clicked_stats_button = not self._is_clicked_stats_button
                break
            except ElementClickInterceptedException:
                print(f"[SCRAPPER] Error al hacer click en 'button stats'. Reintentando en {delay} segundos...")
                time.sleep(delay)

    def select_funplay(self, delay):
        while True:
            try:
                # Obtenemos el botón funplay
                funplay_button = get_funplay_button(self._driver, delay=0.1)
                if funplay_button:
                    print(f"[SCRAPER] Funplay ha sido presionado")
                    funplay_button.click()
                break
            except ElementClickInterceptedException:
                print(f"[SCRAPPER] Error al hacer click en 'button funplay'. Reintentando en {delay} segundos...")
                time.sleep(delay)

    def play(self):
        # Preparamos el cliente, el conector, iniciamos sesión e ingresamos al juego
        self.setup()
        # Empieza el ciclo principal
        latest_numbers = []
        # Data compartida
        data_shared = self.restart_data_shared()
        while True:
            # Esperamos 10 segundos
            time.sleep(10)
            # Seleccionamos funplay
            self.select_funplay(delay=0.1)
            # Abrimos las estadísticas
            self.press_stats(delay=0.1)
            # Obtenemos y procesamos los datos de forma ininterrumpida
            self.loop_get_process_data(delay_loop=0.1, latest_numbers=latest_numbers, data=data_shared)
            # Si el proceso anterior se rompe, refrescamos la página
            self.refresh()

    def refresh(self):
        self._platform.refresh()
        self._is_clicked_stats_button = False