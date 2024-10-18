import time
from core.lightning_roulette.strategy_functions import even_and_odd, for_zones, red_and_black, two_groups
from games.abstract_game import Game
from core.lightning_roulette.scrap_functions import get_data, get_stats_button
from src.connectors.abstract_connector import Connector
from src.database.mongodb_client import Mongo
from src.platforms.abstract_platform import Platform

class LightningRoulette(Game):
    def __init__(self, platform: Platform, connector: Connector, client: Mongo):
        super().__init__(platform, connector, client)
        url_games = self._platform.get_url_games()
        self._url_game = url_games['lightining_roulette']
        self._driver = self._platform.getDriver()
        self._stats_button = None
        self._is_clicked_stats_button = False
    def setup(self):
        # iniciamos la conexion al cluester
        self._client.connect()
        # seleccionamos una base base de datos
        self._client.select_database('RoobetDB')
        # iniciamos sesion en la plataforma
        self._platform.login()
        # nos dirigimos a la url del juego
        self._driver.get(self._url_game)
        # obtenemos el boton de estadísticas y hacemos click
        self._stats_button = get_stats_button(self._driver, 10)
        self._stats_button.click()
        self._is_clicked_stats_button = True
    def start(self):
        self.setup()
        if (not self._is_clicked_stats_button):
            self._stats_button.click()
        game_id = "lightning_roulette"
        zones_state, color_state, parity_state, group_state = 0, 0, 0, 0
        zones_data = {
            "str_latest_zones": None,
            "latest_message_id_zones": None,
            "latest_alert_id_zones": None,
            "latest_prediction_id_zones": None,
            "check_simple_bet_by_zones": False,
            "check_double_bet_by_zones": False
        }
        color_data = {
            "str_latest_color": None,
            "latest_message_id_color": None,
            "latest_alert_id_color": None,
            "latest_prediction_id_color": None,
            "check_simple_bet_by_color": False,
            "check_double_bet_by_color": False
        }
        parity_data = {
            "str_latest_parity": None,
            "latest_message_id_parity": None,
            "latest_alert_id_parity": None,
            "latest_prediction_id_parity": None,
            "check_simple_bet_by_parity": False,
            "check_double_bet_by_parity": False
        }
        group_data = {
            "str_latest_group": None,
            "latest_message_id_group": None,
            "latest_alert_id_group": None,
            "latest_prediction_id_group": None,
            "check_simple_bet_by_group": False,
            "check_double_bet_by_group": False
        }
        delay_get_data = 5
        delay_loop_get_data = 5
        latest_numbers = []
        while True:
            numbers = get_data(driver=self._driver, delay=delay_get_data)
            if latest_numbers != numbers or not numbers:
                zones_state, zones_data = for_zones(game_id=game_id, numbers=numbers, state=zones_state, connector=self._connector, client=self._client, data=zones_data)
                color_state, color_data = red_and_black(game_id=game_id, numbers=numbers, state=color_state, connector=self._connector, client=self._client, data=color_data)
                parity_state, parity_data = even_and_odd(game_id=game_id, numbers=numbers, state=parity_state, connector=self._connector, client=self._client, data=parity_data)
                group_state, group_data = two_groups(game_id=game_id, numbers=numbers, state=group_state, connector=self._connector, client=self._client, data=group_data)
                latest_numbers = numbers
                time.sleep(delay_loop_get_data)
            else:
                delay_loop_get_data += 1
    def refresh(self):
        self._platform.refresh()
        self._is_clicked_stats_button = False
    def get_stats_button(self):
        return self._stats_button