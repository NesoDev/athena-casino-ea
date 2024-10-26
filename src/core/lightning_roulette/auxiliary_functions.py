from datetime import datetime
from src.clients.mongodb_client import Mongo

def obtain_zone(number: int) -> int:
    if number == 0:
        return 0
    elif 1 <= number <= 12:
        return 1
    elif 13 <= number <= 24:
        return 2
    else:
        return 3

def is_equal_zones(numbers: list) -> bool:
    if not numbers:
        return False
    zone = obtain_zone(int(numbers[0]))
    for number in numbers[1:]:
        if obtain_zone(int(number)) != zone:
            return False    
    return True

def obtain_others_zones(zones: list) -> list:
    all_zones = {1, 2, 3}
    remaining_zones = all_zones - set(zones)
    return list(remaining_zones)
        
def zones_list_to_string(zones: list) -> str:
    if not zones:
        return ""
    quoted_zones = [f'{zone}' for zone in zones]
    if len(quoted_zones) == 1:
        return quoted_zones[0]
    return ', '.join(quoted_zones[:-1]) + ' & ' + quoted_zones[-1]
    
def obtain_latest_message_by_strategyId(client: Mongo, db_name: str, strategyId: str):
    client.select_database(db_name)
    messages = client.get_collection("Messages")
    latest_document = messages.find_one(
        {"strategyId": strategyId},
        sort=[("date", -1)]
    )
    return latest_document if latest_document else None

def obtain_latest_message(client:Mongo, db_name:str):
    client.select_database(db_name)
    messages = client.get_collection("Messages")
    
    #print(f"[DEBUG] Collection Messages: {messages}")
    last_message = messages.find_one(sort=[("date", -1)])
    
    #print(f"[DEBUG] LastMessage: {last_message}")
    return last_message if last_message is not None else None

def obtain_datetime():
    return datetime.now()

def create_new_message(client: Mongo, db_name: str, game_id: str, strategy_id: str, message: str):
    new_message = {
        "game_id": game_id,
        "strategy_id": strategy_id,
        "content": message,
        "date": obtain_datetime(),
        "socialsId": { "telegram": "62"} 
    }
    last_message = obtain_latest_message(client, db_name)
    
    if last_message is not None:
        last_socialsId = last_message["socialsId"]
        new_socialsId = {
            social: str(int(id) + 1) for social, id in last_socialsId.items()
        }
        new_message["socialsId"] = new_socialsId

    return new_message

def obtain_color(number: int):
    reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    whites = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31,33, 35]
    if number in reds:
        color = "red"
    elif number in whites:
        color = "white"
    elif number == 0:
        color = "neutral"  
    return color

def is_equal_colors(numbers: list):
    if not numbers:
        return False
    color = obtain_color(int(numbers[0]))
    if color == "neutral":
        return False
    for number in numbers[1:]:
        if obtain_color(int(number)) != color:
            return False
    return True

def is_equal_parity(numbers: list):
    if not numbers:
        return False
    parity = int(numbers[0]) % 2
    return all(int(number) % 2 == parity for number in numbers)

def obtain_group(number: int):
    if number == 0:
        return 'zero'
    elif 1 <= number <= 18:
        return 'first'
    elif 19 <= number <= 36:
        return 'second'

def is_equal_group(numbers: list):
    if not numbers:
        return False
    group = obtain_group(int(numbers[0]))
    if group == 'zero':
        return False
    for number in numbers[1:]:
        if obtain_group(int(number)) != group:
            return False
    return True