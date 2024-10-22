import time
from core.lightning_roulette.strategy_functions import (
    even_and_odd,
    for_zones,
    red_and_black,
    two_groups,
)
from games.abstract_game import Game
from core.lightning_roulette.scrap_functions import (
    check_session_expired,
    get_data,
    get_stats_button,
)
from src.connectors.abstract_connector import Connector
from src.clients.mongodb_client import Mongo
from src.platforms.abstract_platform import Platform


class LightningRoulette(Game):
    def __init__(self, platform: Platform, connector: Connector, client: Mongo):
        super().__init__(platform, connector, client, game_id="lightining_roulette")
        url_games = self._platform.get_url_games()
        self._url_game = url_games[self._game_id]
        self._driver = self._platform.getDriver()
        self._stats_button = None
        self._is_clicked_stats_button = False

    def setup(self):
        # iniciamos la conexion al cluster
        self._client.connect()
        # seleccionamos una base base de datos
        self._client.select_database("RoobetDB")
        # iniciamos sesion en la plataforma
        self._platform.login()
        # nos dirigimos a la url del juego
        self._driver.get(self._url_game)

    def loop_get_process_data(self, delay_loop: int):
        if not self._is_clicked_stats_button:
            self._stats_button.click()
        zone_data = {
            "state": 0,
            "latest_message_id": None,
            "latest_alert_id": None,
            "latest_prediction_id": None,
            "check_start_bets": False,
            "check_simple_bet": False,
            "check_double_bet": False,
            "check_triple_bet": False,
        }
        color_data = {
            "state": 0,
            "latest_message_id": None,
            "latest_alert_id": None,
            "latest_prediction_id": None,
            "check_start_bets": False,
            "check_simple_bet": False,
            "check_double_bet": False,
            "check_triple_bet": False,
        }
        parity_data = {
            "state": 0,
            "latest_message_id": None,
            "latest_alert_id": None,
            "latest_prediction_id": None,
            "check_start_bets": False,
            "check_simple_bet": False,
            "check_double_bet": False,
            "check_triple_bet": False,
        }
        group_data = {
            "state": 0,
            "latest_message_id": None,
            "latest_alert_id": None,
            "latest_prediction_id": None,
            "check_start_bets": False,
            "check_simple_bet": False,
            "check_double_bet": False,
            "check_triple_bet": False,
        }
        latest_numbers = []
        while True:
            # verificamos si la sesion expiró
            if check_session_expired(driver=self._driver):
                break
            # extraemos los resultados
            numbers = get_data(driver=self._driver)
            # procesamos los resultados solo si son nuevos y correctos
            if latest_numbers != numbers and len(numbers) == 12:
                zone_data = for_zones(
                    game_id=self._game_id,
                    numbers=numbers,
                    connector=self._connector,
                    client=self._client,
                    data=zone_data,
                )
                color_data = red_and_black(
                    game_id=self._game_id,
                    numbers=numbers,
                    connector=self._connector,
                    client=self._client,
                    data=color_data,
                )
                parity_data = even_and_odd(
                    game_id=self._game_id,
                    numbers=numbers,
                    connector=self._connector,
                    client=self._client,
                    data=parity_data,
                )
                group_data = two_groups(
                    game_id=self._game_id,
                    numbers=numbers,
                    connector=self._connector,
                    client=self._client,
                    data=group_data,
                )
                latest_numbers = numbers
            time.sleep(delay_loop)

    def play(self):
        # preparamos el cliente, el conector, iniciamos sesion e ingresamos al juego
        self.setup()
        # empieza el ciclo principal
        while True:
            # obtenemos y clickeamos en el boton estadisticas
            self._stats_button = get_stats_button(self._driver, 10)
            self._stats_button.click()
            self._is_clicked_stats_button = True
            # obtenemos y procesamos los datos de forma ininterrumpida
            self.loop_get_process_data(delay_loop=0.1)
            # si el proceso anterior se rompe, refrescamos la página
            self.refresh()

    def refresh(self):
        self._platform.refresh()
        self._is_clicked_stats_button = False