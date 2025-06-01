FROM python:3.11-slim

# Empêche les messages interactifs
ENV DEBIAN_FRONTEND=noninteractive

# Mise à jour et installation des dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    fonts-liberation \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crée le répertoire de travail
WORKDIR /app

# Copie les fichiers requis
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copie le reste du projet
COPY . .

# Configuration Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose le port utilisé par l'app
EXPOSE 8000

# Lancement de l'app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
