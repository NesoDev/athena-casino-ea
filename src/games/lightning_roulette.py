from functions.lightning_roulette.strategy_functions import for_zones
from games.abstract_game import Game
from functions.lightning_roulette.scrap_functions import get_data, get_stats_button

class LightningRoulette(Game):
    def __init__(self, platform, connector, client):
        super().__init__(platform, connector, client)
        url_games = self.platform._get_url_games()
        self._url_game = url_games['lightining_roulette']
        self._driver = self.platform.getDriver()
        self._stats_button = None
        self._is_clicked_stats_button = False
    def setup(self):
        # iniciamos sesion en la plataforma
        self._platform.login()
        # nos dirigimos a la url del juego
        self._driver.get(self._url_game)
        # obtenemos el boton de estadísticas
        self._stats_button = get_stats_button(self._driver, 10)
    def start(self):
        if (not self._is_clicked_stats_button):
            self._stats_button.click()
        state = 0
        delay = 19
        while True:
            numbers = get_data(driver=self._driver, delay=delay)
            for_zones(numbers=numbers, state=state, connector=self._connector, client=self._client)
            print(f"Lectura de datos en {delay} segundos")
    def refresh(self):
        self._platform.refresh()
        self._is_clicked_stats_button = False
    def get_stats_button(self):
        return self._stats_button