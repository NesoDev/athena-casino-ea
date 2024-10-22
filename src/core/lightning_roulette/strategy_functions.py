from auxiliary_functions import create_new_message, is_equal_colors, is_equal_group, is_equal_parity, is_equal_zones, obtain_color, obtain_datetime, obtain_group, obtain_zone, obtain_others_zones, zones_list_to_string
from connectors.telegram_connector import Telegram
from clients.mongodb_client import Mongo
from src.reports.crono_report import send_report

message_cancel_start_bets = (
    "⚠️Rechazo de análisis\n"
    "El patrón detectado no es válido. Iniciando nuevo análisis…"
)
message_win_bet_head = "🎉¡ACIERTO! 🥳💰💵🤑🔮\n"
message_win_bet_body = "💵 Resultado: Apuesta Ganada en "
message_win_bet_foot = "💸 ¡Vamos por más! ¡Multipliquemos nuestras ganancias! 💰💰💰"

message_lose_bet = (
    "❌Apuesta Perdida\n"
    "Resultado: Apuesta no acertada. Iniciando nuevo análisis…"
)

message_alert_bet_head = "🎲 **¡ATENCIÓN!** 🚨🚨\n"
message_alert_bet_body = "🎯Analizando mesa para posible apuesta en"
message_alert_bet_foot = "📊 Esperando resultados… ⏳"

message_confirmed_start_bet_head = "✅ **¡CONFIRMADO!**\n"
message_confirmed_start_bet_body = "Apostar en"
message_confirmed_start_bet_foot = "🔐 Proteger el 0."

message_cases_head = "🎲 ¡ATENCIÓN! 🚨\n"
message_cases_body = "se volvió a repetir. Dobla tu apuesta anterior.\n"
message_cases_foot = "📊 Esperando resultados… ⏳✨" 

# Estrategias del juego Lightning Roulette:

""""
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
def for_zones(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "por_zonas"
    entity = "Zona"
    if data['check_start_bets']:
        if not is_equal_zones(numbers[0:4]):
            message = message_cancel_start_bets
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            connector.send_message(message=message)
        data['check_start_bets'] = False
    if data['check_simple_bet']:
        print("///////// Verificando predicción de la apuesta simple anterior //////////")
        if not is_equal_zones(numbers[0:5]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "type":"apuesta_simple", "status": "acierto"})
            data['check_simple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {obtain_zone(int(numbers[0]))}\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_double_bet']:
        print("///////// Verificando predicción de la apuesta doble anterior //////////")
        if not is_equal_zones(numbers[0:6]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_doble", "status": "acierto"})
            data['check_double_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {obtain_zone(int(numbers[0]))}\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_triple_bet']:
        print("///////// Verificando predicción de la apuesta triple anterior //////////")
        if not is_equal_zones(numbers[0:7]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            data['check_triple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {obtain_zone(int(numbers[0]))}\n", message_win_bet_foot)
        else:
            message = message_lose_bet
        connector.send_message(message=message)
        data['state'] = 0
        report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
        connector.send_message(message=report_daily_win_lose)
        message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
        client.insert_document(collection_name="Messages", document=message)
    print("[FOR ZONES] Iniciando proceso", end=" ")
    match(data['state']):
        case 0:
            data['state'] = 1 if is_equal_zones(numbers[0:3]) else 0
        case 1:
            data['state'] = 2 if is_equal_zones(numbers[0:4]) else 0
        case 2:
            data['state'] = 3 if is_equal_zones(numbers[0:5]) else 0
        case 3:
            data['state'] = 4 if is_equal_zones(numbers[0:6]) else 0
    match(data['state']):
        case 1:
            print("[FOR ZONES - CASE 1] Enviando Alerta a telegram")
            zone = obtain_zone(int(numbers[0]))
            other_zones = obtain_others_zones([zone])
            str_other_zones = zones_list_to_string(other_zones)
            message = (message_alert_bet_head, f"{message_alert_bet_body} zonas {str_other_zones} 🌀✨\n", message_alert_bet_foot)
            print(f"Enviando mensaje : {message}")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
            data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
            data['check_start_bets'] = True
        case 2:
            other_zones=obtain_others_zones([numbers[0]])
            str_zones=zones_list_to_string(other_zones)
            data['latest_zones'] = other_zones
            message = (message_confirmed_start_bet_head, f"{message_confirmed_start_bet_body} zonas {str_zones}.\n", message_confirmed_start_bet_foot)
            print("[FOR ZONES - CASE 2] Enviando predicción a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = True
        case 3:
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[FOR ZONES - CASE 3] Enviando prediccion a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = False
            data['check_double_bet'] = True
        case 4:
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[FOR ZONES - CASE 4] Enviando mensaje a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_triple", "status": "fallo"})
            data['check_simple_bet'] = False
            data['check_double_bet'] = False
            data['check_triple_bet'] = True
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
def red_and_white(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "rojo_y_blanco"
    entity = "color"
    if data['check_start_bets']:
        if not is_equal_colors(numbers[0:9]):
            message = message_cancel_start_bets
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            connector.send_message(message=message)
        data['check_start_bets'] = False
    if data['check_simple_bet']:
        print("///////// Verificando predicción de la apuesta simple anterior //////////")
        if not is_equal_colors(numbers[0:10]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "type":"apuesta_simple", "status": "acierto"})
            data['check_simple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'🔴 Rojo' if obtain_color(int(numbers[0])) == 'red' else '⚪ Blanco'}'\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_double_bet']:
        print("///////// Verificando predicción de la apuesta doble anterior //////////")
        if not is_equal_colors(numbers[0:11]):
            data['state'] = 0
            data['check_double_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'🔴 Rojo' if obtain_color(int(numbers[0])) == 'red' else '⚪ Blanco'}'\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_triple_bet']:
        print("///////// Verificando predicción de la apuesta triple anterior //////////")
        if not is_equal_colors(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            data['check_triple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'🔴 Rojo' if obtain_color(int(numbers[0])) == 'red' else '⚪ Blanco'}'\n", message_win_bet_foot)
        else:
            message = message_lose_bet
        connector.send_message(message=message)
        data['state'] = 0
        report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
        connector.send_message(message=report_daily_win_lose)
        message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
        client.insert_document(collection_name="Messages", document=message)
    match state:
        case 0:
            data['state'] = 1 if is_equal_colors(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_colors(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_colors(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_colors(numbers[0:11]) else 0
    match state:
        case 1:
            message = (message_alert_bet_head, f"{message_alert_bet_body} {entity} {'⚪ BLANCO' if obtain_color(int(numbers[0])) == 'red' else '🔴 ROJO'} 🌀✨\n", message_alert_bet_foot)
            print("[EVEN AND ODD - CASE 1] Enviando Alerta a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
            data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
            data['check_start_bets'] = True
        case 2:
            str_color = f'⚪ BLANCO' if obtain_color(int(numbers[0])) == 'red' else '🔴 ROJO'
            message = (message_confirmed_start_bet_head,  f"{message_confirmed_start_bet_body} {entity} {str_color}.\n", message_confirmed_start_bet_foot)
            print("[RED AND WHITE- CASE 2] Enviando predicción a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = True
        case 3:
            str_color = f'⚪ BLANCO' if obtain_color(int(numbers[0])) == 'red' else '🔴 ROJO'
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[EVEN AND ODD - CASE 3] Enviando prediccion a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = False
            data['check_double_bet'] = True
        case 4:
            str_color = f'⚪ BLANCO' if obtain_color(int(numbers[0])) == 'red' else '🔴 ROJO'
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[EVEN AND ODD - CASE 4] Enviando mensaje a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_triple", "status": "fallo"})
            data['check_simple_bet'] = False
            data['check_double_bet'] = False
            data['check_triple_bet'] = True
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
      
def even_and_odd(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "par_e_impar"
    entity = "Paridad"
    if data['check_start_bets']:
        if not is_equal_parity(numbers[0:9]):
            message = message_cancel_start_bets
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            connector.send_message(message=message)
        data['check_start_bets'] = False
    if data['check_simple_bet']:
        print("///////// Verificando predicción de la apuesta simple anterior //////////")
        if not is_equal_parity(numbers[0:10]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "type":"apuesta_simple", "status": "acierto"})
            data['check_simple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'PAR' if (int(numbers[0])) % 2 == 0 else 'IMPAR'} {numbers[0]}.\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_double_bet']:
        print("///////// Verificando predicción de la apuesta doble anterior //////////")
        if not is_equal_parity(numbers[0:11]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_doble", "status": "acierto"})
            data['check_double_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'PAR' if (int(numbers[0])) % 2 == 0 else 'IMPAR'} {numbers[0]}.\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_triple_bet']:
        print("///////// Verificando predicción de la apuesta triple anterior //////////")
        if not is_equal_parity(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            data['check_triple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'PAR' if (int(numbers[0])) % 2 == 0 else 'IMPAR'} {numbers[0]}.\n", message_win_bet_foot)
        else:
            message = message_lose_bet
        connector.send_message(message=message)
        data['state'] = 0
        report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
        connector.send_message(message=report_daily_win_lose)
        message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
        client.insert_document(collection_name="Messages", document=message)
    print("[RED AND WHITE] Iniciando proceso", end=" ")
    client.select_database(db_name="RoobetDB")  # Pasarlo a un nivel superior si se repite
    match state:
        case 0:
            data['state'] = 1 if is_equal_parity(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_parity(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_parity(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_parity(numbers[0:11]) else 0
    match state:
        case 1:
            message = (message_alert_bet_head, f"{message_alert_bet_body} {'IMPARES ' if int(numbers[0]) % 2 == 0 else 'PARES'} 🌀✨\n", message_alert_bet_foot)
            print("[EVEN AND ODD - CASE 1] Enviando Alerta a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            data['latest_message_id'] = client.insert_document(collection_name="Messages", document=message_document)
            data['latest_alert_id'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id']})
            data['check_start_bets'] = True
        case 2:
            str_parity = "IMPARES" if int(numbers[0]) % 2 == 0 else "PARES"
            message = (message_confirmed_start_bet_head,  f"{message_confirmed_start_bet_body} {str_parity}.\n", message_confirmed_start_bet_foot)
            print("[EVEN AND ODD - CASE 2] Enviando predicción a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = True
        case 3:
            str_parity = "IMPARES" if int(numbers[0]) % 2 == 0 else "PARES"
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[EVEN AND ODD - CASE 3] Enviando prediccion a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = False
            data['check_double_bet'] = True
        case 4:
            str_parity = "IMPARES" if int(numbers[0]) % 2 == 0 else "PARES"
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[EVEN AND ODD - CASE 4] Enviando mensaje a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_triple", "status": "fallo"})
            data['check_simple_bet'] = False
            data['check_double_bet'] = False
            data['check_triple_bet'] = True
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

def two_groups(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    strategy_id = "dos_grupos"
    entity = "Grupo"
    if data['check_start_bets']:
        if not is_equal_group(numbers[0:9]):
            message = message_cancel_start_bets
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            connector.send_message(message=message)
        data['check_start_bets'] = False
    if data['check_simple_bet']:
        print("///////// Verificando predicción de la apuesta simple anterior //////////")
        if not is_equal_group(numbers[0:10]):
            data['state'] = 0
            client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "type":"apuesta_simple", "status": "acierto"})
            data['check_simple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'1️⃣-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣-3️⃣6️⃣'} {numbers[0]}.\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_double_bet']:
        print("///////// Verificando predicción de la apuesta doble anterior //////////")
        if not is_equal_group(numbers[0:11]):
            data['state'] = 0
            prediction_id = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_doble", "status": "acierto"})
            data['check_double_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'1️⃣-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣-3️⃣6️⃣'} {numbers[0]}.\n", message_win_bet_foot)
            connector.send_message(message=message)
            report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
            connector.send_message(message=report_daily_win_lose)
            message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
            client.insert_document(collection_name="Messages", document=message)
    if data['check_triple_bet']:
        print("///////// Verificando predicción de la apuesta triple anterior //////////")
        if not is_equal_group(numbers[0:12]):
            client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id'], name_attribute="status", new_value="acierto")
            data['check_triple_bet'] = False
            message = (message_win_bet_head, f"{message_win_bet_body} {entity} {'1️⃣-1️⃣8️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣9️⃣-3️⃣6️⃣'}.\n", message_win_bet_foot)
        else:
            message = message_lose_bet
        connector.send_message(message=message)    
        data['state'] = 0
        report_daily_win_lose = client.create_report_win_lose_daily(db_name="RoobetDB")
        connector.send_message(message=report_daily_win_lose)
        message = client.create_new_message(db_name='RoobetDB', game_id=game_id, strategy_id="null", message=report_daily_win_lose)
        client.insert_document(collection_name="Messages", document=message)

    print("[TWO GROUPS] Iniciando proceso", end=" ")
    match(data['state']):
        case 0:
            data['state'] = 1 if is_equal_group(numbers[0:8]) else 0
        case 1:
            data['state'] = 2 if is_equal_group(numbers[0:9]) else 0
        case 2:
            data['state'] = 3 if is_equal_group(numbers[0:10]) else 0
        case 3:
            data['state'] = 4 if is_equal_group(numbers[0:11]) else 0
    match(data['state']):
        case 1:
            message = (message_alert_bet_head, f"{message_alert_bet_body} {entity} {'1️⃣9️⃣-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣-1️⃣8️⃣'} 🌀✨\n", message_alert_bet_foot)
            print("\n[TWO GROUPS - CASE 1] Enviando alert a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            data['latest_message_id_group'] = client.insert_document(collection_name="Messages", document=new_message)
            data['latest_alert_id_group'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id_group']})
        case 2:
            message = (message_confirmed_start_bet_head,  f"{message_confirmed_start_bet_body} {entity} {'1️⃣9️⃣-3️⃣6️⃣' if obtain_group(int(numbers[0])) == 'first' else '1️⃣-1️⃣8️⃣'}.\n", message_confirmed_start_bet_foot)
            print("[TWO GROUPS - CASE 2] Enviando predicción a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = True
        case 3:
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[TWO GROUPS - CASE 3] Enviando prediccion a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['check_simple_bet'] = False
            data['check_double_bet'] = True
        case 4:
            message = (message_cases_head, f"{entity} {message_cases_body}", message_cases_foot)
            print("[TWO GROUPS - CASE 4] Enviando mensaje a telegram")
            connector.send_message(message=message)
            message_document = create_new_message(client=client, db_name="RoobetDB", game_id=game_id, strategy_id=strategy_id, message=message)
            client.insert_document(collection_name="Messages", document=message_document)
            data['latest_prediction_id'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id'], "date": obtain_datetime(), "type":"apuesta_triple", "status": "fallo"})
            data['check_simple_bet'] = False
            data['check_double_bet'] = False
            data['check_triple_bet'] = True
    return data