from src.loggers.logger import Logger
from src.loggers.logger import Logger
from src.browsers.firefox_browser import Firefox
from src.browsers.chrome_browser import Chrome
from src.platforms.roobet_platform import Roobet
from src.connectors.telegram_connector import Telegram
from src.clients.mongodb_client import Mongo
from src.games.lightning_roulette import LightningRoulette

class BotLigthningRoulette:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._game = None
    
    def setup(self):
        browser = Firefox(self._logger)
        #browser = Chrome(self._logger)
        platform = Roobet(browser, self._logger)
        connector = Telegram(self._logger)
        client = Mongo(self._logger)
        self._game = LightningRoulette(platform, connector, client, self._logger)

    def run(self):
        while True:
            self.setup()
            self._game.play()
            self._logger.log("Apagando...", "BOT")
            self._logger.log(f"Reiniciando...","BOT")
            self._logger.log("Iniciando...", "BOT")