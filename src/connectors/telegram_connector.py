from connectors.abstract_connector import Connector
import requests
from src.config.settings import load_env_variable

class Telegram(Connector):
    def __init__(self, ):
        data_telegram = load_env_variable('DATA_CONNECTORS')['telegram']
        super().__init__(data_telegram)
        self._token = self._data['token']
        self._chat_id = self._data['chat_id']
        self._endpoint = self._data['endpoint']

    def send_message(self, message):
        endpoint = self._endpoint
        token = self._token
        url = f"{endpoint}{token}/sendMessage"
        params = {
            'chat_id': self._chat_id,
            'text': message
        }
        try:
            res = requests.post(url, json=params)
            res.raise_for_status()
            print("[CONNECTOR] Mensaje enviado correctamente.")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] No se pudo enviar el mensaje.")

    def get_updates(self):
        endpoint = self._endpoint
        token = self._token
        url = f"{endpoint}{token}/getUpdates"
        requests.post(url=url)

    def remove_message(self, social_name, message_id):
        if (social_name == "telegram"):
            self.get_updates()
            endpoint = self._endpoint
            token = self._token
            url = f"{endpoint}{token}/deleteMessage"
            params = {
                'chat_id': self._chat_id,
                'message_id': message_id
            }
            try:
                res = requests.post(url, json=params)
                res.raise_for_status()
                print("[CONNECTOR] Mensaje eliminado correctamente.")
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] No se pudo eliminar el mensaje: {e}")