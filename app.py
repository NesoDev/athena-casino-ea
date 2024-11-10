from src.loggers.logger import Logger
from src.bots.athena_bot import BotLigthningRoulette

if __name__ == "__main__":
    logger = Logger("America/Lima")
    logger.log("Iniciando...", "BOT")
    bot = BotLigthningRoulette(logger=logger)
    bot.run()