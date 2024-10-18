from auxiliary_functions import create_new_message, is_equal_colors, is_equal_group, is_equal_parity, is_equal_zones, obtain_color, obtain_datetime, obtain_group, obtain_others_zones, zones_list_to_string
from connectors.telegram_connector import Telegram
from database.mongodb_client import Mongo
from src.reports.crono_report import send_report

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
        enviamos el mensaje (ATENCIÓN!!🔔🔔 Doblar apuesta) // preguntar por: 3 errores como máximo son cubiertos por el bot
        SINO empezamos de nuevo
"""

def for_zones(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    GAME_ID = game_id
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "por_zonas"
    print("[FOR ZONES] Iniciando proceso", end=" ")
    match(state):
        case 0:
            state=1 if is_equal_zones(numbers[0:3]) else 0
        case 1:
            state=2 if is_equal_zones(numbers[0:4]) else -2
        case 2:
            state=3 if is_equal_zones(numbers[0:5]) else 0
    if state == 0:
        print("-> No se encontró un patrón")
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            print("\n[FOR ZONES] Enviando Alerta a telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            #print("[FOR ZONES] Guardando Mensaje")
            data['latest_message_id_zones'] = client.insert_document(collection_name="Messages", document=new_message)
            #print("[FOR ZONES] Guardando Alerta")
            data['latest_alert_id_zones'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id_zones']})
            if data['check_simple_bet_by_zones']:
                if not is_equal_zones(numbers[0:5]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_zones'], name_attribute="status", new_value="acierto")
                    data['check_simple_bet_by_zones'] = False
                    send_report(client=client, connector=connector)
            if data['check_double_bet_by_zones']:
                if not is_equal_zones(numbers[0:6]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_zones'], name_attribute="status", new_value="acierto")
                    data['check_double_bet_by_zones'] = False
                    send_report(client=client, connector=connector)

        case 2:
            other_zones=obtain_others_zones(numbers[0])
            str_zones=zones_list_to_string(other_zones)
            data['str_latest_zones'] = str_zones
            message = f"CONFIRMADO ✅ apostar en zona {str_zones}"
            print("[FOR ZONES] Enviando mensaje a telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            print("[FOR ZONES] Guardando Mensaje")
            client.insert_document(collection_name="Messages", document=new_message)
            print("[FOR ZONES] Guardando Predicción")
            data['latest_prediction_id_zones'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_zones'], "type":"apuesta_simple", "status": "fallo"})
            data['check_simple_bet_by_zones'] = True
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            latest_message_zones = client.get_document(collection_name="Messages", document_id=data['latest_message_id_zones'])
            socials_id = latest_message_zones['socialsId']
            for social, id in socials_id.items():
                print(f"[FOR ZONES] Eliminando último mensaje de alerta en {social}")
                connector.remove_message(social_name=social, message_id=id)
            state = 0
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en zona {data['str_latest_zones']}"
            print("[FOR ZONES] Enviando mensaje a telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            print("[FOR ZONES] Guardando Mensaje")
            client.insert_document(collection_name="Messages", document=new_message)
            print("[FOR ZONES] Guardando Predicción")
            data['latest_prediction_id_zones'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_zones'], "type":"apuesta_doble", "status": "fallo"})
            data['check_simple_bet_by_zones'] = False
            data['check_double_bet_by_zones'] = True
            state = 0
    return state, data

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

def red_and_black(game_id: str, numbers:list, state:int, connector: Telegram, client: Mongo, data: dict):
    GAME_ID = game_id
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "rojo_y_blanco"

    print("[RED AND BLACK] Iniciando proceso", end=" ")
    client.select_database(db_name="RoobetDB")  # Pasarlo a un nivel superior si se repite
    match state:
        case 0:
            state = 1 if is_equal_colors(numbers[0:8]) else 0
        case 1:
            state = 2 if is_equal_colors(numbers[0:9]) else -2
        case 2:
            state = 3 if is_equal_colors(numbers[0:10]) else 0
    if state == 0:
        print("-> No se encontró un patrón")
    match state:
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            print("\n[RED AND BLACK] Enviando mensaje a Telegram")
            connector.send_message(message=message)

            print("[RED AND BLACK] Guardando mensaje")
            new_message = create_new_message(client, "RoobetDB", GAME_ID, STRATEGY_ID, DATE_TIME, message)
            data['latest_message_id_color'] = client.insert_document("Messages", new_message)

            print("[RED AND BLACK] Guardando alerta")
            data['latest_alert_id_color'] = client.insert_document("Alerts", {"messageID": data['latest_message_id_color']})

            if data['check_simple_bet_by_color']:
                if not is_equal_colors(numbers[0:10]):
                    print("[RED AND BLACK] Actualizando estado de predicción a 'acierto'")
                    client.update_attribute_by_document("Predictions", data['latest_prediction_id_color'], "status", "acierto")
                    data['check_simple_bet_by_color'] = False
                    send_report(client=client, connector=connector)

            if data['check_double_bet_by_color']:
                if not is_equal_colors(numbers[0:11]):
                    print("[RED AND BLACK] Actualizando estado de predicción a 'acierto'")
                    client.update_attribute_by_document("Predictions", data['latest_prediction_id_color'], "status", "acierto")
                    data['check_double_bet_by_color'] = False
                    send_report(client=client, connector=connector)

        case 2:
            str_color = obtain_color(numbers[0])
            message = f"CONFIRMADO ✅ APOSTAR EN '{str_color}' 🔴!"
            print("[RED AND BLACK] Enviando mensaje a Telegram")
            connector.send_message(message=message)

            print("[RED AND BLACK] Guardando mensaje y predicción")
            new_message = create_new_message(client, "RoobetDB", GAME_ID, STRATEGY_ID, DATE_TIME, message)
            client.insert_document("Messages", new_message)
            data['latest_prediction_id_color'] = client.insert_document("Predictions", {
                "alertID": data['latest_alert_id_color'], "type": "apuesta_simple", "status": "fallo"
            })
            data['check_simple_bet_by_color'] = True

        case -2:
            print("[RED AND BLACK] Eliminando último mensaje de alerta")
            latest_message_color = client.get_document("Messages", data['latest_message_id_color'])
            socials_id = latest_message_color['socialsId']
            for social, id in socials_id.items():
                connector.remove_message(social, id)
            state = 0

        case 3:
            message = f"ATENCIÓN!! 🔔🔔 Doblar apuesta en '{data['str_latest_color']}'"
            print("[RED AND BLACK] Enviando mensaje a Telegram")
            connector.send_message(message=message)

            print("[RED AND BLACK] Guardando mensaje y predicción")
            new_message = create_new_message(client, "RoobetDB", GAME_ID, STRATEGY_ID, DATE_TIME, message)
            client.insert_document("Messages", new_message)
            data['latest_prediction_id_color'] = client.insert_document("Predictions", {
                "alertID": data['latest_alert_id_color'], "type": "apuesta_doble", "status": "fallo"
            })
            data['check_simple_bet_by_color'] = False
            data['check_double_bet_by_color'] = True
            state = 0

    return state, data


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
    GAME_ID = game_id
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "par_e_impar"
    print("[EVEN AND ODD] Iniciando proceso", end=" ")
    match(state):
        case 0:
            state=1 if is_equal_parity(numbers[0:8]) else 0
        case 1:
            state=2 if is_equal_parity(numbers[0:9]) else -2
        case 2:
            state=3 if is_equal_parity(numbers[0:10]) else 0
    if state == 0:
        print("-> No se encontró un patrón")
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            print("\n[EVEN AND ODD] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            data['latest_message_id_parity'] = client.insert_document(collection_name="Messages", document=new_message)
            data['latest_alert_id_parity'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id_parity']})
            if data['check_simple_bet_by_parity']:
                if not is_equal_parity(numbers[0:10]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_parity'], name_attribute="status", new_value="acierto")
                    data['check_simple_bet_by_parity'] = False
                    send_report(client=client, connector=connector)
            if data['check_double_bet_by_parity']:
                if not is_equal_parity(numbers[0:11]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_parity'], name_attribute="status", new_value="acierto")
                    data['check_double_bet_by_parity'] = False
                    send_report(client=client, connector=connector)
        case 2:
            str_parity = 'PAR' if int(numbers[0]) % 2 == 0 else "IMPAR"
            str_other_parity = 'IMPAR' if str_parity == 'PAR' else 'PAR'
            data['str_latest_parity'] = str_other_parity
            message = f"CONFIRMADO ✅ apostar en {str_other_parity}"
            print("[EVEN AND ODD] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="Messages", document=new_message)
            data['latest_prediction_id_parity'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_parity'], "type":"apuesta_simple", "status": "fallo"})
            data['check_simple_bet_by_parity'] = True
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            print("[EVEN AND ODD] Eliminando último mensaje de alerta")
            latest_message_parity = client.get_document(collection_name="Messages", document_id=data['latest_message_id_parity'])
            socials_id = latest_message_parity['socialsId']
            for social, id in socials_id.items():
                connector.remove_message(social_name=social, message_id=id)
            state = 0
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en {data['str_latest_parity']}"
            print("[EVEN AND ODD] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="Messages", document=new_message)
            data['latest_prediction_id_parity'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_parity'], "type":"apuesta_doble", "status": "fallo"})
            data['check_simple_bet_by_parity'] = False
            data['check_double_bet_by_parity'] = True
            state = 0
    return state, data

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
    GAME_ID = game_id
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "dos_grupos"
    print("[TWO GROUPS] Iniciando proceso", end=" ")
    match(state):
        case 0:
            state=1 if is_equal_group(numbers[0:8]) else 0
        case 1:
            state=2 if is_equal_group(numbers[0:9]) else -2
        case 2:
            state=3 if is_equal_group(numbers[0:10]) else 0
    if state == 0:
        print("-> No se encontró un patrón")
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            print("\n[TWO GROUPS] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            data['latest_message_id_group'] = client.insert_document(collection_name="Messages", document=new_message)
            data['latest_alert_id_group'] = client.insert_document(collection_name="Alerts", document={"messageID":data['latest_message_id_group']})
            if data['check_simple_bet_by_group']:
                if not is_equal_group(numbers[0:10]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_group'], name_attribute="status", new_value="acierto")
                    data['check_simple_bet_by_group'] = False
                    send_report(client=client, connector=connector)
            if data['check_double_bet_by_group']:
                if not is_equal_group(numbers[0:11]):
                    client.update_attribute_by_document(collection_name="Predictions", document_id=data['latest_prediction_id_group'], name_attribute="status", new_value="acierto")
                    data['check_double_bet_by_group'] = False
                    send_report(client=client, connector=connector)
        case 2:
            str_group = "[1, 18]" if obtain_group(int(numbers[0])) == 'first' else "[19, 36]"
            str_other_group = "[19, 36]" if str_group == "[1, 18]" else "[1, 18]"
            data['str_latest_group'] = str_other_group
            message = f"CONFIRMADO ✅ apostar en {str_other_group}"
            print("[TWO GROUPS] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="Messages", document=new_message)
            data['latest_prediction_id_group'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_group'], "type":"apuesta_simple", "status": "fallo"})
            data['check_simple_bet_by_group'] = True
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            print("[TWO GROUPS] Eliminando último mensaje de alerta")
            latest_message_group = client.get_document(collection_name="Messages", document_id=data['latest_message_id_group'])
            socials_id = latest_message_group['socialsId']
            for social, id in socials_id.items():
                connector.remove_message(social_name=social, message_id=id)
            state = 0
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en {data['str_latest_group']}"
            print("[TWO GROUPS] Enviando mensaje a Telegram")
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="Messages", document=new_message)
            data['latest_prediction_id_group'] = client.insert_document(collection_name="Predictions", document={"alertID":data['latest_alert_id_group'], "type":"apuesta_doble", "status": "fallo"})
            data['check_simple_bet_by_group'] = False
            data['check_double_bet_by_group'] = True
            state = 0
    return state, data