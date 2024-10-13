from pymongo import MongoClient as PyMongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId 

class MongoClient:
    def __init__(self, uri):
        self.uri = uri
        self.client = None
        self.database = None

    def connect(self):
        try:
            self.client = PyMongoClient(self.uri)
            print("Conexión exitosa al servidor MongoDB.")
        except Exception as e:
            print(f"Error al conectar al servidor MongoDB: {e}")

    def select_database(self, db_name):
        if self.client:
            self.database = self.client[db_name]
            print(f"Base de datos seleccionada: {db_name}")
        else:
            print("Primero debes conectar al servidor MongoDB.")

    def get_collection(self, collection_name):
        if self.database:
            return self.database[collection_name]
        else:
            print("Primero debes seleccionar una base de datos.")

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                result = collection.insert_one(document)
                print(f"Documento insertado con ID: {result.inserted_id}")
                return str(result.inserted_id)
            except DuplicateKeyError:
                print("Error: El documento ya existe.")
                return None
            except Exception as e:
                print(f"Error al insertar documento: {e}")
                return None
            
    def get_document(self, collection_name, document_id):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                document = collection.find_one({"_id": ObjectId(document_id)})
                if document:
                    print("Documento encontrado:", document)
                    return document
                else:
                    print("No se encontró ningún documento con ese ID.")
                    return None
            except Exception as e:
                print(f"Error al buscar documento: {e}")
                return None

    def read_documents(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        if collection:
            if query is None:
                query = {}
            documents = collection.find(query)
            return list(documents)

    def update_attribute_by_document(self, collection_name, document_id, name_attribute, new_value):
        collection = self.get_collection(collection_name)
        if collection:
            query = {"_id": document_id}
            new_values = {"$set": {name_attribute: new_value}}
            result = collection.update_one(query, new_values)
            if result.modified_count > 0:
                print(f"Documento con ID {document_id} actualizado correctamente.")
            else:
                print(f"No se encontró ningún documento con ID {document_id}.")
        else:
            print(f"No se encontró la colección '{collection_name}'.")


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
            print("Conexión cerrada.")