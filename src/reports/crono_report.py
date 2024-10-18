from core.lightning_roulette.auxiliary_functions import create_new_message, obtain_datetime
from connectors.telegram_connector import Telegram
from database.mongodb_client import Mongo

def obtain_win_lose(client: Mongo, db_name: str):
    client.select_database(db_name)
    predictions = client.get_collection('predictions')
    wins = 0
    loses = 0
    if predictions is not None:
        for prediction in predictions.find({}):
            if prediction.status == 'acierto':
                wins += 1
            if prediction.status == 'fallo':
                loses += 1
    return f"{wins} ACIERTOS \n{loses} FALLOS"

def send_report(client: Mongo, connector: Telegram):
    datetime = obtain_datetime()
    db_name = 'RoobetDB'
    report = obtain_win_lose(client, db_name)
    connector.send_message(message=report)
    message = create_new_message(client, db_name, game_id="lightning_roulette", strategy_id="all", date_Time=datetime, message=report)
    client.insert_document(collection_name="Messages", document=message)