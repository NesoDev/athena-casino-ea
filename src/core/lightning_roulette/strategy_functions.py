from datetime import datetime
from src.core.lightning_roulette.auxiliary_functions import is_equal_colors, is_equal_group, is_equal_parity, is_equal_zones, obtain_color, obtain_group, obtain_zone, obtain_others_zones, zones_list_to_string
from src.connectors.telegram_connector import Telegram
from src.clients.mongodb_client import Mongo
from src.core.lightning_roulette.utils import resources
from src.core.lightning_roulette.report_functions import create_report_win_lose_daily
from src.loggers.logger import Logger

# Estrategias del juego Lightning Roulette:

def for_zones(game_id: str, numbers: list, connector: Telegram, client: Mongo, data: dict, logger: Logger):
    strategy_id = "for_zones"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:4]):
            data['state'] = 0
            logger.log("Se rompió el patrón...", "FOR ZONES")
            # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
            for lang, package in resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                if lang == 'es': 
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        # logger.log("------- Verificando predicción de la apuesta simple anterior -------", "FOR ZONES")
        if not is_equal_zones(numbers[0:5]):
            data['state'] = 0
            logger.log("Se cumplió la predicción simple anterior. Enviando mensaje...", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if current_zone == 0 else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_zone}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_double_bet']:
        data['state'] = 0
        data['check_double_bet'] = False
        # logger.log("------- Verificando predicción de la apuesta triple anterior -------", "FOR ZONES")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:6]):
            logger.log("Se cumplió la predicción doble anterior. Enviando mensaje...", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if current_zone == 0 else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_zone}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    # logger.log(f"Reporte: {client.obtain_win_lose_daily(db_name='RoobetDB')}", "FOR ZONES")
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            logger.log("No se cumplió la predicción doble anterior. Enviando mensaje...", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="fallo")
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_zones(numbers[0:3]) else 0
        case 1:
            data['state'] = 2 if is_equal_zones(numbers[0:4]) else 0
        case 2:
            data['state'] = 3 if is_equal_zones(numbers[0:5]) else 0

    if data['state'] == 0:
        logger.log("No se encontró un patrón.", "FOR ZONES")

    match data['state']:
        case 1:
            logger.log("Caso 1 se cumplió, Enviando alerta.", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            list_other_zones = obtain_others_zones([current_zone])
            str_other_zones = zones_list_to_string(list_other_zones)
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {str_other_zones} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 2:
            logger.log("Caso 2 se cumplió, Enviando predicción.", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            list_other_zones = obtain_others_zones([current_zone])
            str_other_zones = zones_list_to_string(list_other_zones)
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_confirmed_start_bet_head'], f"{messages['message_confirmed_start_bet_body']} {entity} {str_other_zones}", messages['message_confirmed_start_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
        case 3:
            logger.log("Caso 3 se cumplió, Enviando predicción.", "FOR ZONES")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_doble", "status": ""})
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_zone} {messages['message_cases_body']}", messages['message_cases_foot_double'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "FOR ZONES")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    return data


def red_and_black(game_id: str, numbers: list, connector: Telegram, client: Mongo, data: dict, logger: Logger):
    strategy_id = "red_and_black"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_colors(numbers[0:10]):
            data['state'] = 0
            logger.log("Se rompió el patrón...", "RED AND BLACK")
            # logger.log("Enviando mensaje en {lang}: {message}", "RED AND BLACK")
            for lang, package in resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                if lang == 'es': 
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document) 

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        # logger.log("-------- Verificando predicción de la apuesta simple anterior --------", "RED AND BLACK")
        if not is_equal_colors(numbers[0:11]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            logger.log("Se cumplió la predicción simple anterior. Enviando mensaje...", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚫'
            current_color = "0️⃣" if obtain_color(int(numbers[0])) == "neutral" else current_color
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if obtain_color(int(numbers[0])) == "neutral" else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_color}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_double_bet']:
        data['state'] = 0
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        # logger.log("-------- Verificando predicción de la apuesta doble anterior --------", "RED AND BLACK")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_colors(numbers[0:12]):
            #------------------------------------------------------------------------------------------------------------------
            logger.log("Se cumplió la predicción doble anterior. Enviando mensaje...", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚫'
            current_color = "0️⃣" if obtain_color(int(numbers[0])) == "neutral" else current_color
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if obtain_color(int(numbers[0])) == "neutral" else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_color} {obtain_zone(int(numbers[0]))}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            #------------------------------------------------------------------------------------------------------------------
            logger.log("No se cumplió la predicción doble anterior. Enviando mensaje...", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="fallo")
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_colors(numbers[0:9]) else 0
        case 1:
            data['state'] = 2 if is_equal_colors(numbers[0:10]) else 0
        case 2:
            data['state'] = 3 if is_equal_colors(numbers[0:11]) else 0

    if data['state'] == 0:
        logger.log("No se encontró un patrón.", "RED AND BLACK")
    match data['state']:
        case 1:
            logger.log("Caso 1 se cumplió, Enviando alerta.", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_color = '⚫' if obtain_color(int(numbers[0])) == 'red' else '🔴'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_color} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 2:
            logger.log("Caso 2 se cumplió, Enviando predicción.", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_color = '⚫' if obtain_color(int(numbers[0])) == 'red' else '🔴'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_confirmed_start_bet_head'], f"{messages['message_confirmed_start_bet_body']} {entity} {other_color}", messages['message_confirmed_start_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 3:
            logger.log("Caso 3 se cumplió, Enviando predicción.", "RED AND BLACK")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_doble", "status": ""})
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚫'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_color} {messages['message_cases_body']}", messages['message_cases_foot_double'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "RED AND BLACK")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
    return data

     
def even_and_odd(game_id: str, numbers: list, connector: Telegram, client: Mongo, data: dict, logger: Logger):
    strategy_id = "even_and_odd"
    #------------------------------------------------------------------------------------------------------------------
    types_parity = {"es": ["PAR", "IMPAR"], "en": ["EVEN", "ODD"], "fr": ["PAIR", "IMPAIR"]}
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_parity(numbers[0:10]):
            data['state'] = 0
            logger.log("Se rompió el patrón...", "EVEN AND ODD")
            # logger.log("Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
            for lang, package in resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                if lang == 'es': 
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        # logger.log("-------- Verificando predicción de la apuesta simple anterior --------", "EVEN AND ODD")
        if not is_equal_parity(numbers[0:11]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            logger.log("Se cumplió la predicción simple anterior. Enviando mensaje...", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                current_parity = 0 if int(numbers[0]) % 2 == 0 else 1
                current_parity = types_parity[lang][current_parity]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_parity}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_double_bet']:
        data['state'] = 0
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        # logger.log("-------- Verificando predicción de la apuesta doble anterior --------", "EVEN AND ODD")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_parity(numbers[0:12]):
            logger.log("Se cumplió la predicción doble anterior. Enviando mensaje...", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                current_parity = 0 if int(numbers[0]) % 2 == 0 else 1
                current_parity = types_parity[lang][current_parity]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_parity}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            logger.log("No se cumplió la predicción doble anterior. Enviando mensaje...", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="fallo")
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['state'] == 0:
        logger.log("No se encontró un patrón.", "EVEN AND ODD")
    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_parity(numbers[0:9]) else 0
        case 1:
            data['state'] = 2 if is_equal_parity(numbers[0:10]) else 0
        case 2:
            data['state'] = 3 if is_equal_parity(numbers[0:11]) else 0

    match data['state']:
        case 1:
            logger.log("Caso 1 se cumplió, Enviando predicción.", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                other_parity = 1 if int(numbers[0]) % 2 == 0 else 0
                other_parity = types_parity[lang][other_parity]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_parity} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 2:
            logger.log("Caso 2 se cumplió, Enviando predicción.", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                other_parity = 1 if int(numbers[0]) % 2 == 0 else 0
                other_parity = types_parity[lang][other_parity]
                message = (messages['message_confirmed_start_bet_head'], f"{messages['message_confirmed_start_bet_body']} {entity} {other_parity}", messages['message_confirmed_start_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 3:
            logger.log("Caso 3 se cumplió, Enviando predicción.", "EVEN AND ODD")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_double", "status": ""})
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                current_parity = 0 if int(numbers[0]) % 2 == 0 else 1
                current_parity = types_parity[lang][current_parity]
                message = (messages['message_cases_head'], f"{entity} {current_parity} {messages['message_cases_body']}", messages['message_cases_foot_double'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "EVEN AND ODD")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
    return data


def two_groups(game_id: str, numbers: list, connector: Telegram, client: Mongo, data: dict, logger: Logger):
    strategy_id = "two_groups"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_group(numbers[0:10]):
            data['state'] = 0
            logger.log("Se rompió el patrón...", "TWO GROUPS")
            # logger.log("Enviando mensaje en {lang}: {message}", "TWO GROUPS")
            for lang, package in resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                if lang == 'es': 
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        # logger.log("-------- Verificando predicción de la apuesta simple anterior --------", "TWO GROUPS")
        if not is_equal_group(numbers[0:11]):
            data['state'] = 0
            logger.log("Se cumplió la predicción simple anterior. Enviando mensaje...", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            current_group = "0️⃣" if obtain_color(int(numbers[0])) == "zero" else current_group
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if obtain_group(int(numbers[0])) == "zero" else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_group}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_double_bet']:
        data['state'] = 0
        data['check_double_bet'] = False
        # logger.log("-------- Verificando predicción de la apuesta doble anterior --------", "TWO GROUPS")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_group(numbers[0:12]):
            logger.log("Se cumplió la predicción doble anterior. Enviando mensaje...", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            current_group = "0️⃣" if obtain_color(int(numbers[0])) == "zero" else current_group
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                entity = "" if obtain_group(int(numbers[0])) == "zero" else entity
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_group}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            logger.log("No se cumplió la predicción doble anterior. Enviando mensaje...", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="fallo")
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['state'] == 0:
        logger.log("No se encontró un patrón.", "TWO GROUPS")
    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_group(numbers[0:9]) else 0
        case 1:
            data['state'] = 2 if is_equal_group(numbers[0:10]) else 0
        case 2:
            data['state'] = 3 if is_equal_group(numbers[0:11]) else 0

    match data['state']:
        case 1:
            logger.log("Caso 1 se cumplió, Enviando alerta.", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_group = '1️⃣9️⃣\\-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣\\-1️⃣8️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_group} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 2:
            logger.log("Caso 2 se cumplió, Enviando predicción.", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_group = '1️⃣9️⃣\\-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣\\-1️⃣8️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_confirmed_start_bet_head'], f"{messages['message_confirmed_start_bet_body']} {entity} {other_group}", messages['message_confirmed_start_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID": data['latest_message_id']})
        case 3:
            logger.log("Caso 3 se cumplió, Enviando predicción.", "TWO GROUPS")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID": data['latest_alert_id'], "date": datetime.now(), "type": "apuesta_double", "status": ""})
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_group} {messages['message_cases_body']}", messages['message_cases_foot_double'])
                connector.send_message(message="\n".join(message), lang=lang)
                # logger.log(f"Enviando mensaje en {lang}: {message}", "TWO GROUPS")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
    return data