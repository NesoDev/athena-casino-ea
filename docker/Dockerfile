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
ENV DATA_CASINOS='{"roobet": {"name": "Roobet", "url": "https://roobet.com", "games": [{"name": "Lightning Roulette", "game_url": "https://roobet.com/game/evolution:lightning_roulette", "login_url": "https://roobet.com/game/evolution:lightning_roulette?modal=auth&tab=login"}], "account": {"username": "diegoafarrua", "password": "N36root654$$"}}}'

ENV DATA_DRIVERS='[{"name": "Chrome", "path": "/usr/bin/chromedriver", "options": ["--headless", "--disable-gpu"]}]'

# copia e instala dependencias del entorno virtual
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# copia la aplicación al contenedor
COPY . /app
WORKDIR /app

# ejecuta el script principal de la aplicación
CMD ["python", "src/main.py"]