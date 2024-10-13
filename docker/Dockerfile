# syntax=docker/dockerfile

# usa imagen oficial de python
FROM python:3.9-slim

# define versiones de chorme y chromedriver
ENV CHROME_VERSION=115.0.5790.170
ENV CHROMEDRIVER_VERSION=115.0.5790.170

# actualiza dependencias, instala wget, unzip y elimina archivos basura
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# instala chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb && \
    apt-get install -y ./google-chrome-stable_${CHROME_VERSION}-1_amd64.deb && \
    rm ./google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

# descarga e instala chromedriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver-linux64.zip

# establece el display de Chrome en modo headless
ENV DISPLAY=:99

# crea un entorno virtual
RUN python -m venv /env

# define la ruta del entorno virtual
ENV PATH="/env/bin:$PATH"

# define variables de entorno
ENV DATA_PLATFORMS='{"roobet": {"name": "Roobet", "url": "https://roobet.com", "url_games": { "lightning_roulette": "https://roobet.com/game/evolution:lightning_roulette" }, "account": {"username": "diegoafarrua", "password": "N36root654$$"}}}'
ENV DATA_DRIVERS='{"chrome": {"path": "/usr/bin/chromedriver", "options": ["--headless", "--disable-gpu"]}}'
ENV DATA_CONNECTORS='{"telegram":{"endpoint": "https://api.telegram.org/bot"}, "token": "7500841529:AAGvLC_SjJffNOP5gVO_LDWnocM0TyBixDY", "chat_id": "-4563626142"}'
ENV USER_MONGODB='everavendano'
ENV PASSWORD_MONGODB='Galaxyj2prime123'
ENV CLUSTER='casinobot.w7hs8.mongodb.net'
ENV DATABASE='CasinoBot'
ENV URI_MONGODB='mongodb+srv://${USER_MONGODB}:${PASSWORD_MONGODB}@${CLUSTER}/${DATABASE}?retryWrites=true&w=majority'

# copia e instala dependencias del entorno virtual
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# copia la aplicación al contenedor
COPY . /app
WORKDIR /app

# ejecuta el script principal de la aplicación
CMD ["python", "src/main.py"]