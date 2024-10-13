from database.mongodb_client import MongoClient
from drivers.chrome_driver import Chrome
from games.lightning_roulette import LightningRoulette
from platforms.roobet_platform import Roobet
from connectors.telegram_connector import Telegram
import os, json

def get_data(name_driver, name_platform, name_connector):
    # recuperamos las variables de entorno
    str_drivers = os.getenv('DATA_DRIVERS')
    str_platforms = os.getenv('DATA_PLATFORMS')
    str_connectors = os.getenv('DATA_CONNECTORS')
    # casteamos las variables de string a json
    drivers = json.loads(str_drivers)
    platforms = json.loads(str_platforms)
    connectors = json.loads(str_connectors)
    # recuperamos los datos de cada json
    data_driver = drivers[name_driver]
    data_platform = platforms[name_platform]
    data_connector  = connectors[name_connector]
    # retornaamos los datos
    return data_driver, data_platform, data_connector

if __name__ == "__main__":
    # obtenemos los datos del driver, plataforma y conector
    data_chrome, data_roobet, data_telegram = get_data('chrome', 'roobet', 'telegram')
    # iniciamos el driver de un navegador
    driver = Chrome(data_chrome)
    # instanciamos una plataforma
    platform = Roobet(driver, data_roobet)
    # instanciamos un juego
    game = LightningRoulette(platform)
    # iniciamos
    while True:
        game.setup()
        if game.get_stats_button != None:
            # iniciamos el juego
            game.start()
        else:
            # si sucede un error refrescamos la página
            game.refresh()