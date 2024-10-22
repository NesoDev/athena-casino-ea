from drivers.firefox_driver import Firefox
from platforms.roobet_platform import Roobet
from connectors.telegram_connector import Telegram
from clients.mongodb_client import Mongo
from games.lightning_roulette import LightningRoulette

class BotLigthningRoulette:
    def __init__(self):
        driver = Firefox()
        platform = Roobet(driver)
        connector = Telegram()
        client = Mongo()
        self._game = LightningRoulette(platform, connector, client)
    
    def start(self):
        game = self._game
        game.start()