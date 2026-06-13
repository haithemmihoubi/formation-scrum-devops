# Gérer plusieurs environnements (dev / staging / prod)

## 1. Le principe : une image, plusieurs configurations

La règle DevOps fondamentale (« **Build once, run anywhere** ») :
on construit **une seule image** et on l'adapte à chaque environnement **au démarrage**,
via des **variables d'environnement** — jamais en recompilant une image par environnement.

```
   [ Image unique ]  ──>  dev      (variables dev)
                     ──>  staging  (variables staging)
                     ──>  prod     (variables prod)
```

## 2. Méthode A — Spring profiles + variables d'environnement

L'application lit son profil via `SPRING_PROFILES_ACTIVE`. On a un fichier de
configuration par environnement :

```
src/main/resources/
├── application.yml          # commun
├── application-dev.yml      # H2, logs DEBUG
├── application-staging.yml  # PostgreSQL de test
└── application-prod.yml     # PostgreSQL prod, logs INFO
```

Au lancement, on choisit l'environnement **sans changer l'image** :

```bash
docker run -e SPRING_PROFILES_ACTIVE=dev      app:1.0
docker run -e SPRING_PROFILES_ACTIVE=staging  app:1.0
docker run -e SPRING_PROFILES_ACTIVE=prod     app:1.0
```

## 3. Méthode B — Fichiers `.env` + docker-compose

Docker Compose lit automatiquement un fichier `.env` à côté du `docker-compose.yml`.
On crée un fichier par environnement.

**`.env.dev`**
```env
SPRING_PROFILES_ACTIVE=dev
DATABASE_URL=jdbc:postgresql://db:5432/quickbite_dev
DATABASE_PASSWORD=devsecret
LOG_LEVEL=DEBUG
```

**`.env.prod`**
```env
SPRING_PROFILES_ACTIVE=prod
DATABASE_URL=jdbc:postgresql://db:5432/quickbite
DATABASE_PASSWORD=${PROD_DB_PASSWORD}   # injecté par le CI/CD, jamais en clair
LOG_LEVEL=INFO
```

**`docker-compose.yml`**
```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: ${SPRING_PROFILES_ACTIVE}
      DATABASE_URL: ${DATABASE_URL}
      DATABASE_PASSWORD: ${DATABASE_PASSWORD}
```

Lancement selon l'environnement :

```bash
docker compose --env-file .env.dev  up -d --build
docker compose --env-file .env.prod up -d --build
```

## 4. Méthode C — Fichiers `compose.override` (dev vs prod)

Docker Compose fusionne automatiquement `docker-compose.yml` +
`docker-compose.override.yml`. On garde le commun dans le fichier de base et les
spécificités par environnement dans des fichiers séparés.

**`docker-compose.yml`** (commun)
```yaml
services:
  api:
    image: quickbite-api:1.0
    ports: ["8080:8080"]
```

**`docker-compose.dev.yml`** (surcharge dev)
```yaml
services:
  api:
    build: .
    environment:
      SPRING_PROFILES_ACTIVE: dev
    volumes:
      - ./src:/app/src        # hot-reload en dev
```

**`docker-compose.prod.yml`** (surcharge prod)
```yaml
services:
  api:
    environment:
      SPRING_PROFILES_ACTIVE: prod
    restart: always
    deploy:
      resources:
        limits:
          memory: 512m
```

Lancement :

```bash
# Développement
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 5. Méthode D — `ARG` au build vs `ENV` au runtime

| Mécanisme | Quand ? | Exemple |
|-----------|---------|---------|
| `ARG` | Au **build** de l'image | version, URL d'un dépôt privé |
| `ENV` | Au **runtime** du conteneur | profil, mot de passe, URL de base de données |

```dockerfile
# ARG : valeur fixée au moment du build
ARG APP_VERSION=1.0.0
LABEL version=$APP_VERSION

# ENV : valeur par défaut, surchargée au docker run -e
ENV SPRING_PROFILES_ACTIVE=prod
```

```bash
docker build --build-arg APP_VERSION=2.3.1 -t app:2.3.1 .
docker run -e SPRING_PROFILES_ACTIVE=staging app:2.3.1
```

> **Règle de sécurité** : un `ARG` ou un `ENV` n'est **pas** secret — il reste visible
> dans `docker history`. Les vrais secrets (mots de passe, clés) doivent venir d'un
> gestionnaire de secrets (Docker secrets, Vault, variables CI/CD), **jamais** écrits
> dans le Dockerfile ou commités dans Git.

## 6. Tableau récapitulatif des méthodes

| Méthode | Cas d'usage idéal |
|---------|-------------------|
| A — Spring profiles + `-e` | Simple, un seul conteneur |
| B — `.env` par environnement | Stack Compose, séparation claire dev/prod |
| C — `compose.override` | Comportements très différents (volumes, limites) |
| D — `ARG` / `ENV` | Paramétrer le build vs le runtime |

Le plus courant en production : **B + D** — une image paramétrée par `ENV`, des fichiers
`.env` distincts, et les secrets injectés par le pipeline CI/CD.
