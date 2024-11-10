# Usa la imagen oficial de Python
FROM python:3.10-slim

# ------------------------
# Configuración de la aplicación
# ------------------------
WORKDIR /app
COPY . /app

# Establece el PYTHONPATH para la aplicación
ENV PYTHONPATH="/app/src"

# ------------------------
# Añade el repositorio inestable (Sid) para instalar Firefox
# ------------------------
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends firefox && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------
# Creación del entorno virtual e Instalación de dependencias de Python
# ------------------------
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# ------------------------
# Definimos las variables de entorno
# ------------------------
ENV PATH="/env/bin:$PATH"
ENV DATA_PLATFORMS='{"roobet": {"name": "Roobet", "url": "https://roobet.com/?modal=auth&tab=login", "url_games": {"lightning_roulette": "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login"}, "account": {"username": "jmusayonscar92", "password": "Los8musa."}}}'
ENV DATA_CLIENTS='{"mongodb": {"uri": "mongodb+srv://everavendano:Galaxyj2prime123@casinobot.w7hs8.mongodb.net/CasinoBot?retryWrites=true&w=majority"}}'
ENV DATA_CONNECTORS='{"telegram": {"endpoint": "https://api.telegram.org/bot", "bots": {"en": {"token": "7824866804:AAHmjFJFJDjJldP1ahKt6gYe2IT89V0VIVY", "username": "athenas_en_bot", "chat_id": "-1002389708028"}, "es": {"token": "7907522262:AAGGKCnG93huWYN9UPvd_IqW7qF3rmaGKUY", "username": "nesos0_bot", "chat_id": "-1002174291131"}, "fr": {"token": "7508380116:AAFsE8avSNGN_lD0nXceHP0H-rPvO7YQN1g", "username": "athenas_fr_bot", "chat_id": "-1002424831565"}}}}'

# ------------------------
# Comando para ejecutar la aplicación con Xvfb
# ------------------------
CMD ["python3", "app.py"]