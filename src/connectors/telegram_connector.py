from src.connectors.abstract_connector import Connector
from src.config.settings import load_env_variable
import requests


class Telegram(Connector):
    def __init__(self):
        data_telegram = load_env_variable('DATA_CONNECTORS')['telegram']
        super().__init__(data_telegram)
        self._endpoint = self._data["endpoint"]
        self._bots = self._data["bots"]

    def send_message(self, message, lang):
        endpoint = self._endpoint
        data_bot = self._data["bots"][lang]
        token = data_bot["token"]
        chat_id = data_bot["chat_id"]
        url = f"{endpoint}{token}/sendMessage"
        params = {"chat_id": chat_id, "text": message, "parse_mode": "MarkdownV2"}
        while True:
            try:
                res = requests.post(
                    url, json=params, timeout=15
                )  # Timeout de 15 segundos
                print(f"Contenido: {res.text}")
                res.raise_for_status()
                #print("[TELEGRAM] Mensaje enviado correctamente.")
                break
            except requests.exceptions.Timeout:
                print(
                    "[ERROR] La solicitud a Telegram excedió el tiempo de espera. Reintentando envío..."
                )
            except requests.exceptions.RequestException as e:
                print(
                    f"[ERROR] No se pudo enviar el mensaje: {e}. Reintentando envío..."
                )

    def get_updates(self):
        endpoint = self._endpoint
        token = self._token
        url = f"{endpoint}{token}/getUpdates"
        requests.post(url=url)

    def remove_message(self, social_name, message_id):
        if social_name == "telegram":
            self.get_updates()
            endpoint = self._endpoint
            token = self._token
            url = f"{endpoint}{token}/deleteMessage"
            params = {"chat_id": self._chat_id, "message_id": message_id}
            try:
                res = requests.post(url, json=params)
                res.raise_for_status()
                print("[INFO] Mensaje eliminado correctamente.")
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] No se pudo eliminar el mensaje: {e}")

    
