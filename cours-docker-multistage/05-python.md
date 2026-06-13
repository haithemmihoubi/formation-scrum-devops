# Dockeriser une application Python (Flask / FastAPI / Django)

## 1. Particularité de Python

Python est **interprété** : pas de compilation en binaire. Le « build » consiste à
**installer les dépendances** (`pip install`). Le multi-stage sert surtout à
**séparer les dépendances de build** (compilateurs C pour certaines libs) du runtime.

## 2. Dockerfile — FastAPI / Flask (avec serveur de production)

```dockerfile
# ---------- Étape 1 : build des dépendances ----------
FROM python:3.12-slim AS build
WORKDIR /app

# Outils de compilation nécessaires à certaines libs (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances dans un répertoire isolé
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Étape 2 : runtime minimal ----------
FROM python:3.12-slim
WORKDIR /app

# Utilisateur non-root
RUN useradd --create-home --shell /bin/bash app

# On copie UNIQUEMENT les paquets installés (pas gcc ni les caches)
COPY --from=build /install /usr/local
COPY . .

USER app
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000
# Gunicorn + Uvicorn workers pour FastAPI (production)
CMD ["gunicorn", "main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", "--workers", "4"]
```

Pour **Flask**, remplacer la commande finale par :

```dockerfile
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

> ❌ Ne **jamais** utiliser le serveur de développement (`flask run`,
> `uvicorn --reload`, `python manage.py runserver`) en production : utiliser
> **Gunicorn** (ou Uvicorn pour l'ASGI pur).

## 3. Dockerfile — Django

```dockerfile
# ---------- build ----------
FROM python:3.12-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- runtime ----------
FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home app
COPY --from=build /install /usr/local
COPY . .

# Fichiers statiques collectés au build de l'image
RUN python manage.py collectstatic --noinput

USER app
ENV PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=projet.settings
EXPOSE 8000
CMD ["gunicorn", "projet.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

## 4. Multi-environnement avec Django/Flask

Comme pour Spring, on sépare la configuration et on choisit via une variable :

```bash
docker run -e DJANGO_SETTINGS_MODULE=projet.settings.prod app
docker run -e DJANGO_SETTINGS_MODULE=projet.settings.dev  app
```

Ou via `.env` + Compose :

```yaml
services:
  web:
    build: .
    environment:
      DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE}
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}     # injecté par le CI/CD
```

## 5. Le `requirements.txt` et le cache

Copier `requirements.txt` **avant** le code permet à Docker de réutiliser la couche
`pip install` tant que les dépendances ne changent pas — même logique que `pom.xml`
pour Maven ou `package.json` pour npm.

## 6. `.dockerignore`

```gitignore
__pycache__/
*.pyc
.venv/
venv/
.git/
.env
*.sqlite3
.pytest_cache/
```

## 7. Bonnes pratiques Python en conteneur

| Bonne pratique | Pourquoi |
|----------------|----------|
| Image `python:3.12-slim` | ~10× plus petite que `python:3.12` |
| `PYTHONUNBUFFERED=1` | Les logs sortent immédiatement (utile en conteneur) |
| `pip install --no-cache-dir` | Évite de stocker le cache pip dans l'image |
| Serveur WSGI/ASGI (Gunicorn) | Le serveur de dev ne tient pas la charge |
| `USER app` non-root | Sécurité |

## 8. Commandes

```bash
docker build -t mon-api-python:1.0 .
docker run -p 8000:8000 -e PORT=8000 mon-api-python:1.0
curl http://localhost:8000/health
```
