from connectors.abstract_connector import Connector
import requests

class Telegram(Connector):
    def __init__(self, data):
        super().__init__(data)
        self._connector = self.data['telegram']
        self._chat_id = self.connector['chat_id']
        self._endpoint = self.connector['endpoint']

    def send_message(self, message):
        endpoint = self._endpoint
        url = f"{endpoint}/sendMessage"
        params = {
            'chat_id': self._chat_id,
            'text': message
        }
        success = False
        while not success:
            try:
                res = requests.post(url, params)
                if res.status_code == 200: success = True
            except Exception as e:
                pass

    def remove_message(self, social_name, message_id):
        if (social_name == "telegram"):
            endpoint = self._endpoint
            url = f"{endpoint}/deleteMessage"
            params = {
                'chat_id': self._chat_id,
                'message_id': message_id
            }
            success = False
            while not success:
                try:
                    res = requests.post(url, params)
                    if res.status_code == 200: success = True
                except Exception as e:
                    pass

    def get_last_idmessage(self):
        pass