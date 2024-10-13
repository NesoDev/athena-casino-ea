from datetime import datetime
from database.mongodb_client import MongoClient

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
    zone = obtain_zone(numbers[0])
    for number in numbers[1:]:
        if obtain_zone(number) != zone:
            return False    
    return True

def obtain_others_zones(number:int) -> int:
    zone = obtain_zone(number)
    match(zone):
        case 0:
            return [1, 2, 3]
        case 1:
            return [2, 3]
        case 2:
            return [1, 3]
        case 3:
            return [1, 2]
        
def zones_list_to_string(zones: list) -> str:
    if not zones:
        return ""
    quoted_zones = [f'"{zone}"' for zone in zones]
    if len(quoted_zones) == 1:
        return quoted_zones[0]
    return ', '.join(quoted_zones[:-1]) + ' y ' + quoted_zones[-1]
    
def obtain_latest_message_by_strategyId(client: MongoClient, db_name: str, strategyId: str):
    client.select_database(db_name)
    messages = client.get_collection("messages")
    latest_document = messages.find_one(
        {"strategyId": strategyId},
        sort=[("date", -1)]
    )
    return latest_document if latest_document else None

def obtain_latest_message(client:MongoClient, db_name:str):
    client.select_database(db_name)
    messages = client.get_collection("messages")
    last_message = messages.find_one(sort=[("date", -1)])
    return last_message if last_message else None

def create_new_message(client: MongoClient, db_name: str, game_id: str, strategy_id: str, date_Time: datetime, message: str):
    new_message = {
        "game_id": game_id,
        "strategy_id": strategy_id,
        "content": message,
        "date": date_Time,
        "socialsId": { "telegram": "0"} 
    }
    last_message=obtain_latest_message(client=client, db_name=db_name)
    if (last_message != None):
        last_socialsId=last_message["socialsId"]
        sociaslId = {}
        for social, id in last_socialsId.items():
            sociaslId[social] = str(int(id) + 1)
        new_message["socialsId"] = sociaslId
    return new_message
        
def obtain_datetime():
    return datetime.now()

def obtain_color(number: int):
    reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31,33, 35]
    if number in reds:
        color = "red"
    elif number in blacks:
        color = "black"
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