FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Mise à jour + Python + dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crée le dossier de l'app
WORKDIR /app

# Copie des fichiers
COPY requirement.txt .
RUN pip3 install --no-cache-dir -r requirement.txt

COPY . .

# Variables d’environnement pour Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
