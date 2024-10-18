import time
from pymongo import MongoClient as PyMongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from config.settings import load_env_variable

class Mongo:
    def __init__(self):
        self.uri = load_env_variable('DATA_CLIENTS')['mongodb']['uri']
        self.client = None
        self.database = None

    def connect(self):
        delay = 5
        while True:
            try:
                self.client = PyMongoClient(self.uri)
                print("[CLIENT] Conexion exitosa")
                break
            except Exception as e:
                print(f"[ERROR] Fallo en la conexión. Reintentando en {delay} segundos")
                time.sleep(delay)
        
    def select_database(self, db_name):
        if self.client != None:
            self.database = self.client[db_name]
            print(f"[CLIENT] Base de datos '{db_name} se seleccionó.'")
        else:
            print("[ERROR] Aún no ha iniciado un cliente.")

    def get_collection(self, collection_name):
        if self.database:
            return self.database[collection_name]
        else:
            print("[ERROR] Aún no ha seleccionado una Base de datos")

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                result = collection.insert_one(document)
                print(f"[CLIENT] Nuevo documento insertado en '{collection_name}'.")
                return str(result.inserted_id)
            except DuplicateKeyError:
                print(f"[ERROR] Inserción un documento ya existente en '{collection_name}'.")
                return None
            except Exception as e:
                print(f"[ERROR] Fallo en la inserción en la colección {collection_name}")
                return None
        else:
            print(f"[ERROR] No se encontró la colección {collection_name}.")
            return None
            
    def get_document(self, collection_name, document_id):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                document = collection.find_one({"_id": ObjectId(document_id)})
                if document:
                    return document
                else:
                    print(f"[ERROR] Documento con id '{document_id}' no encontrado en colección '{collection_name}'.")
                    return None
            except Exception as e:
                print(f"[ERROR] Fallo en la obtención de un documento de la colección '{collection_name}'.")
                return None

    def read_documents(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        if collection is not None:
            if query is None:
                query = {}
            documents = collection.find(query)
            return list(documents)

    def update_attribute_by_document(self, collection_name, document_id, name_attribute, new_value):
        collection = self.get_collection(collection_name)
        if collection is not None:
            query = {"_id": document_id}
            new_values = {"$set": {name_attribute: new_value}}
            result = collection.update_one(query, new_values)
            if result.modified_count > 0:
                print(f"[CLIENT] Documento con id {document_id} de la colección '{collection_name}' actualizado correctamente.")
            else:
                print(f"[ERROR] No se encontró ningún documento con id {document_id} en la colección '{collection_name}'.")
        else:
            print(f"[ERROR] No se encontró la colección {collection_name}.")


    def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        if collection:
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                print("Documento eliminado.")
            else:
                print("No se encontró ningún documento que coincida con la consulta.")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            print("[CLIENT] Conexión cerrada.")