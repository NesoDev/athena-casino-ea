from connectors.abstract_connector import Connector
from database.mongodb_client import MongoClient
from functions.lightning_roulette.auxiliary_functions import create_new_message, is_equal_colors, is_equal_group, is_equal_parity, is_equal_zones, obtain_color, obtain_datetime, obtain_group, obtain_latest_message, obtain_latest_message_by_strategyId, obtain_others_zones, zones_list_to_string, obtain_latest_document_by_strategyId

GAME_ID = "lightning_roulette"
str_latest_zones = None
str_latest_color = None
str_latest_parity = None
str_latest_group = None
latest_message_id_zones = None
latest_alert_id_zones = None
check_simple_bet_by_zones = False
check_double_bet_by_zones = False

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

def for_zones(numbers:list, state:int, connector: Connector, client: MongoClient):
    global str_latest_zones, latest_message_id_zones ,latest_alert_id_zones, check_simple_bet_by_zones, check_double_bet_by_zones
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "por_zonas"
    client.select_database(db_name="RoobetDB") # pasarlo a un nivel superior ya que todas las estrategias usan esto
    match(state):
        case 0:
            state=1 if is_equal_zones(numbers[0:3]) else 0
        case 1:
            state=2 if is_equal_zones(numbers[0:4]) else -2
        case 2:
            state=3 if is_equal_zones(numbers[0:5]) else 0
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            latest_message_id_zones = client.insert_document(collection_name="messages", document=new_message)
            latest_alert_id_zones = client.insert_document(collection_name="alerts", document={"messageID":latest_message_id_zones})
            if check_simple_bet_by_zones:
                if not is_equal_zones(numbers[0:5]):
                    client.update_attribute_by_document(collection_name="predictions", document_id=latest_prediction_id_zones, name_attribute="status", new_value="acierto")
                    check_simple_bet_by_zones = False
            if check_double_bet_by_zones:
                if not is_equal_zones(numbers[0:6]):
                    client.update_attribute_by_document(collection_name="predictions", document_id=latest_prediction_id_zones, name_attribute="status", new_value="acierto")
                    check_double_bet_by_zones = False
        case 2:
            other_zones=obtain_others_zones(numbers[0])
            str_zones=zones_list_to_string(other_zones)
            str_latest_zones = str_zones
            message = f"CONFIRMADO ✅ apostar en zona {str_zones}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
            latest_prediction_id_zones = client.insert_document(collection_name="predictions", document={"alertID":latest_alert_id_zones, "type":"apuesta_simple", "status": "fallo"})
            check_simple_bet_by_zones = True
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            latest_message_zones = client.get_document(collection_name="messages", document_id=latest_message_id_zones)
            socials_id = latest_message_zones['socialsId']
            for social, id in socials_id.items():
                connector.remove_message(social_name=social, message_id=id)
            state = 0
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en zona {str_latest_zones}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
            latest_prediction_id_zones = client.insert_document(collection_name="predictions", document={"alertID":latest_alert_id_zones, "type":"apuesta_doble", "status": "fallo"})
            check_simple_bet_by_zones = False
            check_double_bet_by_zones = True
            state = 0

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

def red_and_black(numbers:list, state:int, connector: Connector, client: MongoClient):
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "rojo_y_blanco"
    client.select_database(db_name="RoobetDB") # pasarlo a un nivel superior ya que todas las estrategias usan esto
    match(state):
        case 0:
            state=1 if is_equal_colors(numbers[0:8]) else 0
        case 1:
            state=2 if is_equal_colors(numbers[0:9]) else -2
        case 2:
            state=3 if is_equal_colors(numbers[0:10]) else 0
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case 2:
            str_color = obtain_color(numbers[0])
            str_color = "ROJO 🔴" if str_color == "red" else "NEGRO ⚫"
            str_latest_color = str_color
            message = f"CONFIRMADO ✅ apostar en {str_color}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            last_message_by_forZones = obtain_latest_message_by_strategyId(client=client, db_name="RobbetDB", strategyId=STRATEGY_ID)
            if last_message_by_forZones != None:
                last_socialsId_by_forZones=last_message_by_forZones["socialsId"]
                for social, id in last_socialsId_by_forZones.items():
                    connector.remove_message(social, id)
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en {str_latest_color}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)

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
      
def even_and_odd(numbers:list, state:int, connector: Connector, client: MongoClient):
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "par_e_impar"
    client.select_database(db_name="RoobetDB") # pasarlo a un nivel superior ya que todas las estrategias usan esto
    match(state):
        case 0:
            state=1 if is_equal_parity(numbers[0:8]) else 0
        case 1:
            state=2 if is_equal_parity(numbers[0:9]) else -2
        case 2:
            state=3 if is_equal_parity(numbers[0:10]) else 0
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case 2:
            str_parity = 'PAR' if int(numbers[0]) % 2 == 0 else "IMPAR"
            str_other_parity = 'IMPAR' if str_parity == 'PAR' else 'PAR'
            str_latest_parity = str_other_parity
            message = f"CONFIRMADO ✅ apostar en {str_other_parity}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            last_message_by_forZones = obtain_latest_message_by_strategyId(client=client, db_name="RobbetDB", strategyId=STRATEGY_ID)
            if last_message_by_forZones != None:
                last_socialsId_by_forZones=last_message_by_forZones["socialsId"]
                for social, id in last_socialsId_by_forZones.items():
                    connector.remove_message(social, id)
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en {str_latest_parity}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)

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

def two_groups(numbers:list, state:int, connector: Connector, client: MongoClient):
    DATE_TIME = obtain_datetime()
    STRATEGY_ID = "dos_grupos"
    client.select_database(db_name="RoobetDB") # pasarlo a un nivel superior ya que todas las estrategias usan esto
    match(state):
        case 0:
            state=1 if is_equal_group(numbers[0:8]) else 0
        case 1:
            state=2 if is_equal_group(numbers[0:9]) else -2
        case 2:
            state=3 if is_equal_group(numbers[0:10]) else 0
    match(state):
        case 1:
            message = "ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case 2:
            str_group = "[1, 18]" if obtain_group(int(numbers[0])) == 'first' else "[19, 36]"
            str_other_group = "[19, 36]" if str_group == "[1, 18]" else "[1, 18]"
            str_latest_group = str_other_group
            message = f"CONFIRMADO ✅ apostar en {str_other_group}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)
        case -2:
            # eliminamos el ultimo mensaje (ATENCIÓN!! 🚨🚨 Analizando mesa para una posible apuesta ‼️)
            last_message_by_forZones = obtain_latest_message_by_strategyId(client=client, db_name="RobbetDB", strategyId=STRATEGY_ID)
            if last_message_by_forZones != None:
                last_socialsId_by_forZones=last_message_by_forZones["socialsId"]
                for social, id in last_socialsId_by_forZones.items():
                    connector.remove_message(social, id)
        case 3:
            message = f"CONFIRMADO 🔔 Doblar apuesta en {str_latest_group}"
            connector.send_message(message=message)
            new_message = create_new_message(client=client, db_name="RoobetDB", game_id=GAME_ID, strategy_id=STRATEGY_ID, date_Time=DATE_TIME, message=message)
            client.insert_document(collection_name="messages", document=new_message)