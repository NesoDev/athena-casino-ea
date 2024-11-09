# Athena Casino EA - Guía de Configuración y Ejecución

Esta guía te ayudará a configurar y ejecutar el proyecto en tu máquina local. Sigue los pasos específicos para tu sistema operativo.

---

## **MacOS**

### 1. Configura tu usuario de Git:

```bash
git config --global user.name "nombre de usuario en GitHub"
git config --global user.email "correo en GitHub"
```

### 2. Clona el repositorio:
```bash
git clone "https://github.com/NesoDev/athena-casino-ea.git"
cd athena-casino-ea
```

### 3. Cambiamos de rama:
```bash
git checkout "test/test-roobet-lightningroulette"
```

### 4. Creamos y activamos un entorno virtual:
```bash
python3 -m venv env
source env/bin/activate
```

### 5. Configura las variables de entorno:
```bash
export PATH="/env/bin:$PATH"
```
```bash
export DATA_PLATFORMS='{
  "roobet": {
    "name": "Roobet",
    "url": "https://roobet.com/?modal=auth&tab=login",
    "url_games": {
      "lightning_roulette": "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login"
    },
    "account": {
      "username": "diegoaferrua",
      "password": "N36root654$$"
    }
  }
}'
```
```bash
export DATA_CLIENTS='{
  "mongodb": {
    "uri": "mongodb+srv://everavendano:Galaxyj2prime123@casinobot.w7hs8.mongodb.net/CasinoBot?retryWrites=true&w=majority"
  }
}'
```
```bash
export DATA_CONNECTORS='{
  "telegram": {
    "endpoint": "https://api.telegram.org/bot",
    "bots": {
      "en": {
        "token": "7824866804:AAHmjFJFJDjJldP1ahKt6gYe2IT89V0VIVY",
        "username": "athenas_en_bot",
        "chat_id": "-1002389708028"
      },
      "es": {
        "token": "7907522262:AAGGKCnG93huWYN9UPvd_IqW7qF3rmaGKUY",
        "username": "nesos0_bot",
        "chat_id": "-1002174291131"
      },
      "fr": {
        "token": "7508380116:AAFsE8avSNGN_lD0nXceHP0H-rPvO7YQN1g",
        "username": "athenas_fr_bot",
        "chat_id": "-1002424831565"
      }
    }
  }
}'
```

### 6. Ejecutamos la aplicación
```bash
python app.py
```
