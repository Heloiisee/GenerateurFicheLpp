# Utilise une image légère avec Python
FROM python:3.11-slim

# Empêche les messages d'interaction
ENV DEBIAN_FRONTEND=noninteractive

# Installe les dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crée le répertoire de l'application
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

# Copie tout le code dans l'image
COPY . .

# Définit la commande de lancement
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
