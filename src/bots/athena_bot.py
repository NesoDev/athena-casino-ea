from src.browsers.firefox_browser import Firefox
from src.browsers.chrome_browser import Chrome
from src.platforms.roobet_platform import Roobet
from src.connectors.telegram_connector import Telegram
from src.clients.mongodb_client import Mongo
from src.games.lightning_roulette import LightningRoulette

class BotLigthningRoulette:
    def __init__(self):
        print("Instanciando navegador...")
        #browser = Firefox()
        browser = Chrome()
        print("Instanciando plataforma...")
        platform = Roobet(browser)
        print("Instanciando conector...")
        connector = Telegram()
        print("Instanciando cliente...")
        client = Mongo()
        print("Instanciando juego...")
        self._game = LightningRoulette(platform, connector, client)
    
    def run(self):
        game = self._game
        game.play()