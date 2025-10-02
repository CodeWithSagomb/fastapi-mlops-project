# 1. Image de base : python:3.11-slim (ou 3.12-slim si vous avez changé)
# C'est la base de notre environnement d'exécution léger.
FROM python:3.11-slim

# 2. Définir l'encodage pour l'environnement (bonne pratique)
ENV PYTHONIOENCODING=utf-8

# 3. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 4. Copier et installer les dépendances
# On suppose que requirements.txt est propre et ne contient que le nécessaire (y compris uvicorn)
COPY requirements.txt .

# 5. Installer les dépendances (sans cache pour réduire la taille)
# Le solveur de dépendances (pip) va travailler ici pour trouver les versions compatibles.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier le reste de l'application (le code FastAPI)
# On n'inclut PAS le dossier 'tests' dans l'image de production !
COPY app/ app/

# 7. Exposer le port par défaut (pour l'API)
EXPOSE 8000

# 8. Commande de démarrage (Entrypoint)
# Démarrer le serveur Uvicorn avec l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]