from pymongo import MongoClient as PyMongoClient
from pymongo.errors import DuplicateKeyError
from src.config.settings import load_env_variable
from datetime import datetime, timedelta
import time

class Mongo:
    def __init__(self):
        self.uri = load_env_variable('DATA_CLIENTS')['mongodb']['uri']
        self.client = None
        self.database = None

    def connect(self):
        while True:
            try:
                self.client = PyMongoClient(self.uri)
                print("[MONGODB] Conexion exitosa")
                break
            except Exception as e:
                print(f"[MONGODB] Fallo en la conexión")
                print(f"----- Esperando 5 segundos para el siguiente intento -----")
                time.sleep(5)

    def select_database(self, db_name):
        if self.client != None:
            self.database = self.client[db_name]
            print(f"[MONGODB] Base de datos {db_name} fue seleccionado.")
        else:
            print("[MONGODB] Error. Primero debes conectarte al servidor MongoDB.")

    def get_collection(self, collection_name):
        if self.database is not None:
            return self.database[collection_name]
        else:
            print("[MONGODB] Error. Primero debes seleccionar una base de datos.")
            return None  # Aseguramos que siempre devuelva None si hay un problema.

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        if collection is not None:  # Verificación corregida
            try:
                result = collection.insert_one(document)
                print(f"[MONGODB] Documento insertado con ID: {result.inserted_id}")
                return str(result.inserted_id)
            except DuplicateKeyError:
                print("[MONGODB] El documento ya existe.")
                return None
            except Exception as e:
                print(f"[MONGODB] Error al insertar documento: {e}")
                return None
        else:
            print("[MONGODB] La colección no existe o no fue seleccionada correctamente.")
            return None

    def get_document(self, collection_name, document_id):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                document = collection.find_one({"_id": document_id})
                if document:
                    return document
                else:
                    print("No se encontró ningún documento con ese ID.")
                    return None
            except Exception as e:
                print(f"Error al buscar documento: {e}")
                return None

    def read_documents(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        if collection is not None:
            if query is None:
                query = {}
            documents = collection.find(query)
            return list(documents)

    def update_attribute_by_document(self, collection_name, document_id, name_attribute, new_value):
        document = self.get_document(collection_name=collection_name, document_id=document_id)
        if document:
            collection = self.get_collection(collection_name)
            try:
                update_query = {"$set": {name_attribute: new_value}}
                filter_query = {"_id": document_id}
                result = collection.update_one(filter_query, update_query)
                if result.modified_count > 0:
                    print(f"[MONGODB] Atributo '{name_attribute}' actualizado exitosamente.")
                    document = self.get_document(collection_name=collection_name, document_id=document_id)
                    print(f"Documento modificado: {document}")
                else:
                    print(f"[MONGODB] No hubo cambios en el atributo '{name_attribute}'.")
            except Exception as e:
                print(f"[MONGODB] Error al actualizar documento: {e}")
        else:
            print(f"[MONGODB] Documento con ID '{document_id}' no encontrado.")

    def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        if collection is not None:
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                print("Documento eliminado.")
            else:
                print("No se encontró ningún documento que coincida con la consulta.")

    def obtain_latest_message(self, db_name: str):
        self.select_database(db_name)
        messages = self.get_collection("Messages")
        last_message = messages.find_one(sort=[("date", -1)])
        return last_message if last_message is not None else None

    def create_new_message(self, db_name: str, game_id: str, strategy_id: str, message: str):
        self.select_database(db_name)
        new_message = {
            "game_id": game_id,
            "strategy_id": strategy_id,
            "content": message,
            "date": datetime.now(),
            "socialsId": {"telegram": "62"}
        }
        last_message = self.obtain_latest_message(db_name)
        if last_message is not None:
            last_socialsId = last_message["socialsId"]
            new_socialsId = {
                social: str(int(id) + 1) for social, id in last_socialsId.items()
            }
            new_message["socialsId"] = new_socialsId
        return new_message

    def obtain_win_lose_daily(self, db_name: str):
        self.select_database(db_name)
        predictions = self.get_collection('Predictions')
        wins, loses = 0, 0
        if predictions is not None:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow = today + timedelta(days=1)
            query = {"date": {"$gte": today, "$lt": tomorrow}}
            for prediction in predictions.find(query):
                if prediction['status'] == 'acierto':
                    wins += 1
                if prediction['status'] == 'fallo':
                    loses += 1
        return wins, loses

    def create_report_win_lose_monthly(self, db_name: str):
        self.select_database(db_name)
        predictions = self.get_collection('Predictions')
        wins, loses = 0, 0
        if predictions is not None:
            first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = (first_day_of_month.replace(day=28) + timedelta(days=4)).replace(day=1)
            query = {"date": {"$gte": first_day_of_month, "$lt": next_month}}
            for prediction in predictions.find(query):
                if prediction['status'] == 'acierto':
                    wins += 1
                if prediction['status'] == 'fallo':
                    loses += 1
        wins_percentage = 0 if wins == 0 else round((wins/(wins+loses))*100, 2)
        int_win_percentage = int(wins_percentage)
        decimal_win_percentage = int((wins_percentage - int_win_percentage) * 10)
        wins_percentage = int_win_percentage if decimal_win_percentage == 0 else f"{int_win_percentage}\\.{decimal_win_percentage}"
        report = (f"🚀 Resultado del día 🟢 {wins} 🔴 {loses}\n" f"🎯 Aciertos {wins_percentage}% de las veces")
        print(f"Reporte mensual generado: {wins_percentage}")
        return report

    def create_report_win_lose_all(self, db_name: str):
        self.select_database(db_name)
        predictions = self.get_collection('Predictions')
        wins, loses = 0, 0
        if predictions is not None:
            for prediction in predictions.find({}):
                if prediction['status'] == 'acierto':
                    wins += 1
                if prediction['status'] == 'fallo':
                    loses += 1
        wins_percentage = 0 if wins == 0 else round((wins/(wins+loses))*100, 2)
        int_win_percentage = int(wins_percentage)
        decimal_win_percentage = int((wins_percentage - int_win_percentage) * 10)
        wins_percentage = int_win_percentage if decimal_win_percentage == 0 else f"{int_win_percentage}\\.{decimal_win_percentage}"
        report = (f"🚀 Resultado del día 🟢 {wins} 🔴 {loses}\n" f"🎯 Aciertos {wins_percentage}% de las veces")
        print(f"Reporte anual generado: {wins_percentage}")
        return report

    def close(self):
        if self.client:
            self.client.close()
            print("Conexión cerrada.")