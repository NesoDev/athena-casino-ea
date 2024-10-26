# Usa la imagen oficial de Python
FROM python:3.10

# ------------------------
# Configuración de la aplicación
# ------------------------
WORKDIR /app
COPY . /app

# Establece el PYTHONPATH para la aplicación
ENV PYTHONPATH="/app/src"

# ------------------------
# Creación del entorno virtual
# ------------------------
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# ------------------------
# Instalación de dependencias
# ------------------------
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# ------------------------
# Definimos las variables de entorno
# ------------------------
ENV PATH="/env/bin:$PATH"
ENV DATA_PLATFORMS='{"roobet": {"name": "Roobet", "url": "https://roobet.com/?modal=auth&tab=login", "url_games": {"lightning_roulette": "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login"}, "account": {"username": "diegoaferrua", "password": "N36root654$$"}}}'
ENV DATA_CLIENTS='{"mongodb": {"uri": "mongodb+srv://everavendano:Galaxyj2prime123@casinobot.w7hs8.mongodb.net/CasinoBot?retryWrites=true&w=majority"}}'
ENV DATA_CONNECTORS='{"telegram": {"endpoint": "https://api.telegram.org/bot", "bots": {"en": {"token": "7824866804:AAHmjFJFJDjJldP1ahKt6gYe2IT89V0VIVY", "username": "athenas_en_bot", "chat_id": "-4594636328"}, "es": {"token": "7907522262:AAGGKCnG93huWYN9UPvd_IqW7qF3rmaGKUY", "username": "nesos0_bot", "chat_id": "-4585652451"}, "fr": {"token": "7508380116:AAFsE8avSNGN_lD0nXceHP0H-rPvO7YQN1g", "username": "athenas_fr_bot", "chat_id": "-4580092366"}}}}'

# ------------------------
# Comando para ejecutar la aplicación
# ------------------------
CMD ["python3", "app.py"]
