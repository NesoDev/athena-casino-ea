from pymongo import MongoClient as PyMongoClient
from pymongo.errors import DuplicateKeyError
from src.loggers.logger import Logger
from src.config.settings import load_env_variable
from datetime import datetime, timedelta
from bson import ObjectId
import time
from pytz import timezone  # Importamos pytz para manejar la zona horaria

# Define la zona horaria de Lima/Perú
lima_tz = timezone('America/Lima')

class Mongo:
    def __init__(self, logger: Logger):
        self._uri = load_env_variable('DATA_CLIENTS')['mongodb']['uri']
        self._client = None
        self._database = None
        self._logger = logger

    def connect(self):
        max_retries = 5
        retrie_count = 0
        while retrie_count < max_retries:
            try:
                self._client = PyMongoClient(self._uri)
                return True
            except Exception as e:
                retrie_count += 1
                self._logger.log("Fallo en la conexión. Reintentando en 5 segundos...", "ERROR")
                time.sleep(5)
        return False

    def select_database(self, db_name):
        if self._client is not None:
            self._database = self._client[db_name]
        else:
            self._logger.log("Error. Primero debes conectarte al servidor MongoDB.", "ERROR")

    def get_collection(self, collection_name):
        if self._database is not None:
            return self._database[collection_name]
        else:
            self._logger.log("Error. Primero debes seleccionar una base de datos.", "ERROR")
            return None

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                result = collection.insert_one(document)
                self._logger.log(f"Documento insertado con ID: {result.inserted_id}", "PROCESS")
                return str(result.inserted_id)
            except DuplicateKeyError:
                self._logger.log("El documento ya existe.", "ERROR")
                return None
            except Exception as e:
                self._logger.log(f"Error al insertar documento: {e}", "ERROR")
                return None
        else:
            self._logger.log("La colección no existe o no fue seleccionada correctamente.", "ERROR")
            return None

    def get_document(self, collection_name, document_id):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                document = collection.find_one({"_id": ObjectId(document_id)})
                if document:
                    return document
                else:
                    self._logger.log("No se encontró ningún documento con ese ID.", "INFO")
                    return None
            except Exception as e:
                self._logger.log(f"Error al buscar documento: {e}", "ERROR")
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
                filter_query = {"_id": ObjectId(document_id)}
                result = collection.update_one(filter_query, update_query)
                if result.modified_count > 0:
                    self._logger.log(f"Atributo '{name_attribute}' actualizado exitosamente.", "PROCESS")
                    document = self.get_document(collection_name=collection_name, document_id=document_id)
                    self._logger.log(f"Documento modificado: {document}", "INFO")
                else:
                    self._logger.log(f"No hubo cambios en el atributo '{name_attribute}'.", "INFO")
            except Exception as e:
                self._logger.log(f"Error al actualizar documento: {e}", "ERROR")
        else:
            self._logger.log(f"Documento con ID '{document_id}' no encontrado.", "ERROR")

    def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        if collection is not None:
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                self._logger.log("Documento eliminado.", "PROCESS")
            else:
                self._logger.log("No se encontró ningún documento que coincida con la consulta.", "INFO")

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
            "date": datetime.now(lima_tz),  # Aquí usamos la zona horaria de Lima
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
            today = datetime.now(lima_tz).replace(hour=0, minute=0, second=0, microsecond=0)
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
            first_day_of_month = datetime.now(lima_tz).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = (first_day_of_month.replace(day=28) + timedelta(days=4)).replace(day=1)
            query = {"date": {"$gte": first_day_of_month, "$lt": next_month}}
            for prediction in predictions.find(query):
                if prediction['status'] == 'acierto':
                    wins += 1
                if prediction['status'] == 'fallo':
                    loses += 1
        return wins, loses

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
        return wins, loses

    def close(self):
        self._logger.log(f"Cerrando conexión al clúster.", "MONGODB")
        if self._client:
            self._client.close()