# syntax=docker/dockerfile

# Usa la imagen oficial de Python
FROM python:3.9-slim

# Actualiza dependencias y prepara herramientas necesarias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instala Google Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Instala Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt ANTES de copiar el código completo
COPY requirements.txt /tmp/

# Crea el entorno virtual y usa pip para instalar dependencias
RUN python -m venv /env && \
    /env/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Define la ruta del entorno virtual en el PATH
ENV PATH="/env/bin:$PATH"

# Copia el resto de la aplicación
COPY . /app
WORKDIR /app

# Define variables de entorno necesarias para tu aplicación
ENV DATA_PLATFORMS='{"roobet": {"name": "Roobet", "url": "https://roobet.com/?modal=auth&tab=login", "url_games": { "lightning_roulette": "https://roobet.com/game/evolution:lightning_roulette" }, "account": {"username": "diegoafarrua", "password": "N36root654$$"}}}'
ENV DATA_DRIVERS='{"options": ["--headless", "--disable-gpu"]}'
ENV DATA_CONNECTORS='{"telegram": {"endpoint": "https://api.telegram.org/bot", "token": "7907522262:AAGGKCnG93huWYN9UPvd_IqW7qF3rmaGKUY", "chat_id": "-1002467157850"}}'
ENV DATA_CLIENTS='{"mongodb": { "uri": "mongodb+srv://everavendano:Galaxyj2prime123@casinobot.w7hs8.mongodb.net/CasinoBot?retryWrites=true&w=majority"}}'

# Comando para ejecutar la aplicación
CMD ["python", "src/main.py"]