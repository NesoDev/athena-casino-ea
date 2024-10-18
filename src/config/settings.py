import os
import json

def load_env_variable(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"La variable de entorno {name} no está configurada.")
    return json.loads(value)