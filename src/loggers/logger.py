import logging
from datetime import datetime
import pytz

class Logger:
    def __init__(self, timezone="UTC"):
        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        try:
            self.timezone = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            self.timezone = pytz.UTC
            self.logger.error(f"Zona horaria desconocida. Usando UTC como predeterminado.")
        
    def log(self, message, log_type="INFO"):

        current_time = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
        
        formatted_message = f"{current_time} --> [{log_type}] {message}"
        self.logger.info(formatted_message)

