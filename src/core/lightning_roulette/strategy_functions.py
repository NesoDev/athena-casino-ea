from datetime import datetime
from src.core.lightning_roulette.auxiliary_functions import create_new_message, is_equal_colors, is_equal_group, is_equal_parity, is_equal_zones, obtain_color, obtain_datetime, obtain_group, obtain_zone, obtain_others_zones, zones_list_to_string
from src.connectors.telegram_connector import Telegram
from src.clients.mongodb_client import Mongo
from src.core.lightning_roulette.utils import resources
from src.core.lightning_roulette.report_functions import create_report_win_lose_daily

# Estrategias del juego Lightning Roulette:

"""
1. Por zonas:
    -   SI 3 resultados consecutivos caen en la zona 'a', 
        enviamos el mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
        SINO empezamos de nuevo
    -   SI el 4to resultado se mantiene en la zona 'a',
        enviamos el mensaje (CONFIRMADO ✅ apostar en zona 'b' y 'c')
        SINO eliminamos el mansaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
        y empezamos de nuevo
    -   SI el 5to resultado se mantine en la zona 'a',
        enviamos el mensaje (ATENCIÓN!!🔔🔔 Doblar apuesta) // 3 errores cambian el status de la prediccion 
        SINO empezamos de nuevo
"""
def for_zones(game_id: str, numbers:list, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "for_zones"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:4]):
            for lang, package in  resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        print("------- Verificando predicción de la apuesta simple anterior -------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:5]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_zone}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_double_bet']:
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        print("------- Verificando predicción de la apuesta doble anterior -------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:6]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_doble", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_zone}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_triple_bet']:
        data['state'] = 0
        data['check_triple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta triple anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_zones(numbers[0:7]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_zone}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    match(data['state']):
        case 0:
            data['state'] = 1 if is_equal_zones(numbers[0:3]) else 0
        case 1:
            data['state'] = 2 if is_equal_zones(numbers[0:4]) else 0
        case 2:
            data['state'] = 3 if is_equal_zones(numbers[0:5]) else 0
        case 3:
            data['state'] = 4 if is_equal_zones(numbers[0:6]) else 0
    print("[FOR ZONES] Iniciando proceso")
    match(data['state']):
        case 1:
            print("[FOR ZONES - CASE 1] Enviando Alerta a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            list_other_zones = obtain_others_zones([current_zone])
            str_other_zones = zones_list_to_string(list_other_zones)
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {str_other_zones} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 2:
            print("[FOR ZONES - CASE 2] Enviando predicción a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            list_other_zones = obtain_others_zones([current_zone])
            str_other_zones = zones_list_to_string(list_other_zones)
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_confirmed_start_bet_head'], f"{messages['message_confirmed_start_bet_body']} {entity} {str_other_zones}", messages['message_confirmed_start_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
        case 3:
            print("[FOR ZONES - CASE 3] Enviando prediccion a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_zone} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
        case 4:
            print("[FOR ZONES - CASE 4] Enviando mensaje a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_triple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_triple", "status": "fallo"})
            #------------------------------------------------------------------------------------------------------------------
            current_zone = obtain_zone(int(numbers[0]))
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_zone} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)
    return data

"""
2. Rojo o Negro:
    -   SI 8 resultados consecutivos son de color 'a',
        enviamos el mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
    -   SI el 9no resultado también es de color 'a',
        enviamos el mensaje (CONFIRMADO ✅ APOSTAR EN 'b'🔴!)
        SINO empezamos de nuevo
    -   SI el 10mo resultado también es de color 'a',
        enviamos el mensaje (ATENCIÓN!!🔔🔔 Doblar apuesta) // preguntar por: 3 errores como máximo son cubiertos por el bot
""" 
def red_and_white(game_id: str, numbers:list, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "red_and_white"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_colors(numbers[0:9]):
            for lang, package in  resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document) 
    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #print("-------- Verificando predicción de la apuesta simple anterior --------")
        if not is_equal_colors(numbers[0:10]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚪'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_color}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_double_bet']:
        #------------------------------------------------------------------------------------------------------------------
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta doble anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_colors(numbers[0:11]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚪'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_color}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
    if data['check_triple_bet']:
        data['state'] = 0
        data['check_triple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta triple anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_colors(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚪'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_color} {obtain_zone(int(numbers[0]))}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    print("[RED_AND_WHITE] Iniciando proceso")
    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_colors(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_colors(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_colors(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_colors(numbers[0:11]) else 0
    match data['state']:
        case 1:
            print("[RED AND WHITE- CASE 1] Enviando alerta a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_color = '⚪' if obtain_color(int(numbers[0])) == 'red' else '🔴'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_color} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 2:
            print("[RED AND WHITE- CASE 2] Enviando predicción a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_color = '⚪' if obtain_color(int(numbers[0])) == 'red' else '🔴'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_color} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 3:
            print("[RED AND WHITE - CASE 3] Enviando prediccion a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚪'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_color} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 4:
            print("[RED AND WHITE - CASE 4] Enviando mensaje a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_triple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_triple", "status": "fallo"})
            #------------------------------------------------------------------------------------------------------------------
            current_color = '🔴' if obtain_color(int(numbers[0])) == 'red' else '⚪'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_color} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
    return data

"""
3. Par e impar 
    -   SI 8 resultados consecutivos son 'impares',
        enviamos el mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
    -   SI el 9no resultado también es 'impar',
        enviamos el mensaje (CONFIRMADO ✅ APOSTAR EN 'par'!)
        SINO empezamos de nuevo
    -   SI el 10mo resultado también es 'impar',
        enviamos el mensaje (ATENCIÓN!!🔔🔔 Doblar apuesta) // preguntar por: 3 errores como máximo son cubiertos por el bot
"""
     
def even_and_odd(game_id: str, numbers:list, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "even_and_odd"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_parity(numbers[0:9]):
            for lang, package in  resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #print("-------- Verificando predicción de la apuesta simple anterior --------")
        if not is_equal_parity(numbers[0:10]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_parity = '2️⃣' if int(numbers[0]) % 2 == 0 else '1️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_parity}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_double_bet']:
        #------------------------------------------------------------------------------------------------------------------
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta doble anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_parity(numbers[0:11]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_parity = '2️⃣' if int(numbers[0]) % 2 == 0 else '1️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_parity}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
    if data['check_triple_bet']:
        data['state'] = 0
        data['check_triple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta triple anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_parity(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_parity = '2️⃣' if int(numbers[0]) % 2 == 0 else '1️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_parity} {obtain_zone(int(numbers[0]))}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    print("[EVEN AND ODD] Iniciando proceso")
    match data['state']:
        case 0:
            data['state'] = 1 if is_equal_parity(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_parity(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_parity(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_parity(numbers[0:11]) else 0
    match data['state']:
        case 1:
            print("[EVEN AND ODD - CASE 1] Enviando alerta a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_paririty = '1️⃣' if int(numbers[0]) % 2 == 0 else '2️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_paririty} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 2:
            print("[EVEN AND ODD - CASE 2] Enviando predicción a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_paririty = '1️⃣' if int(numbers[0]) % 2 == 0 else '2️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_paririty} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 3:
            print("[EVEN AND ODD - CASE 3] Enviando prediccion a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_parity = '2️⃣' if int(numbers[0]) % 2 == 0 else '1️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_parity} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 4:
            print("[EVEN AND ODD - CASE 4] Enviando mensaje a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_triple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_triple", "status": "fallo"})
            #------------------------------------------------------------------------------------------------------------------
            current_parity = '2️⃣' if int(numbers[0]) % 2 == 0 else '1️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_parity} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
    return data

"""
4. 1-18 o 19-36 
    -   SI 8 resultados consecutivos están entre [1, 18],
        enviamos el mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
    -   SI el 9no resultado también está entre [1, 18],
        enviamos el mensaje (CONFIRMADO ✅ APOSTAR EN '[19, 36]'!)
        SINO empezamos de nuevo
    -   SI el 10mo resultado también está entre [1, 18],
        enviamos el mensaje (ATENCIÓN!!🔔🔔 Doblar apuesta) // preguntar por: 3 errores como máximo son cubiertos por el bot
"""

def two_groups(game_id: str, numbers:list, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "dos_grupos"
    #------------------------------------------------------------------------------------------------------------------
    if data['check_start_bets']:
        data['check_start_bets'] = False
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_group(numbers[0:9]):
            for lang, package in  resources.items():
                messages = package['default_messages']
                name_strategy = package['names_strategies'][strategy_id]
                message = (messages['message_cancel_start_bets_head'], f"{messages['message_cancel_start_bets_body_1']} {name_strategy} {messages['message_cancel_start_bets_body_2']}", messages['message_cancel_start_bets_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es': 
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    client.insert_document(collection_name="Messages", document=message_document)

    if data['check_simple_bet']:
        data['check_simple_bet'] = False
        #print("-------- Verificando predicción de la apuesta simple anterior --------")
        if not is_equal_group(numbers[0:10]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_group}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    if data['check_double_bet']:
        #------------------------------------------------------------------------------------------------------------------
        data['check_double_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta doble anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_group(numbers[0:11]):
            data['state'] = 0
            #------------------------------------------------------------------------------------------------------------------
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_simple", "status": "acierto"})
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_group}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
    if data['check_triple_bet']:
        data['state'] = 0
        data['check_triple_bet'] = False
        #------------------------------------------------------------------------------------------------------------------
        #print("-------- Verificando predicción de la apuesta triple anterior --------")
        #------------------------------------------------------------------------------------------------------------------
        if not is_equal_group(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_win_bet_head'], f"{messages['message_win_bet_body']} {entity} {current_group} {obtain_zone(int(numbers[0]))}", messages['message_win_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
        else:
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                message = messages['message_lose_bet']
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                report_daily_win_lose = create_report_win_lose_daily(client=client, lang=lang)
                connector.send_message(message=report_daily_win_lose, lang=lang)
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
                    client.insert_document(collection_name="Messages", document=message_document)
    print("[TWO GROUPS] Iniciando proceso")
    match(data['state']):
        case 0:
            data['state'] = 1 if is_equal_group(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_group(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_group(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_group(numbers[0:11]) else 0
    match data['state']:
        case 1:
            print("[TWO GROUPS - CASE 1] Enviando alerta a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_start_bets'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_group = '1️⃣9️⃣\\-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣\\-1️⃣8️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_group} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 2:
            print("[TWO GROUPS - CASE 2] Enviando predicción a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_simple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            other_group = '1️⃣9️⃣\\-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣\\-1️⃣8️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_alert_bet_head'], f"{messages['message_alert_bet_body']} {entity} {other_group} 🌀✨", messages['message_alert_bet_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 3:
            print("[TWO GROUPS - CASE 3] Enviando prediccion a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_double_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_group} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
        case 4:
            print("[TWO GROUPS - CASE 4] Enviando mensaje a telegram")
            #------------------------------------------------------------------------------------------------------------------
            data['check_triple_bet'] = True
            #------------------------------------------------------------------------------------------------------------------
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": datetime.now(), "type":"apuesta_triple", "status": "fallo"})
            #------------------------------------------------------------------------------------------------------------------
            current_group = '1️⃣\\-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣\\-3️⃣6️⃣'
            #------------------------------------------------------------------------------------------------------------------
            for lang, package in  resources.items():
                messages = package['default_messages']
                entity = package['entities_strategies'][strategy_id]
                message = (messages['message_cases_head'], f"{entity} {current_group} {messages['message_cases_body']}", messages['message_cases_foot'])
                connector.send_message(message="\n".join(message), lang=lang)
                #print(f"Enviando mensaje en {lang}: {message}")
                #------------------------------------------------------------------------------------------------------------------
                if lang == 'es':
                    message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
                    data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
                    data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
    return data