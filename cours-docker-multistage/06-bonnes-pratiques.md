# Bonnes pratiques, sécurité & checklist

## 1. Récapitulatif des images de base recommandées

| Technologie | Stage build | Stage runtime |
|-------------|-------------|---------------|
| Spring Boot | `maven:3.9-eclipse-temurin-21` | `eclipse-temurin:21-jre-alpine` |
| Angular / React | `node:20-alpine` | `nginx:alpine` |
| Python | `python:3.12-slim` | `python:3.12-slim` |

Préférer toujours les variantes **`-alpine`** ou **`-slim`** : images minimales,
moins de vulnérabilités, transfert plus rapide.

## 2. Les 10 règles d'or

1. **Multi-stage** : séparer build et runtime.
2. **Cache des dépendances** : copier `pom.xml` / `package.json` / `requirements.txt`
   *avant* le code source.
3. **`.dockerignore`** : ne pas envoyer `node_modules`, `.git`, `target`, `.env`…
4. **Non-root** : créer et utiliser un utilisateur applicatif (`USER app`).
5. **Tags précis** : `node:20-alpine`, jamais `node:latest` (non reproductible).
6. **Une seule responsabilité** par conteneur (un process principal).
7. **Configuration par variables d'environnement**, pas en dur dans l'image.
8. **Secrets hors de l'image** : jamais de mot de passe dans le Dockerfile ou Git.
9. **Healthcheck** : permettre à l'orchestrateur de connaître l'état de l'app.
10. **Versionner les images** : `app:1.4.2`, pas seulement `latest`.

## 3. Sécurité : ce qu'il ne faut jamais faire

```dockerfile
# ❌ MAUVAIS
FROM node:latest                       # tag flottant, non reproductible
ENV DB_PASSWORD=Sup3rSecret            # secret en clair dans l'image !
USER root                              # tourne en root
COPY . .                               # copie tout, y compris .env et .git
```

```dockerfile
# ✅ BON
FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --chown=app:app . .
# Le secret vient du runtime : docker run -e DB_PASSWORD=... (ou Docker secret)
```

## 4. Healthchecks par technologie

```yaml
# Spring Boot (Actuator)
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:8080/actuator/health"]
  interval: 10s
  timeout: 3s
  retries: 5

# Nginx (Angular / React)
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:80/"]
  interval: 10s
  retries: 3

# Python (endpoint /health applicatif)
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
  interval: 10s
  retries: 3
```

## 5. Réduire la taille des images

| Technique | Gain |
|-----------|------|
| Multi-stage | -70 % à -90 % |
| Image `alpine` / `slim` | -50 % à -80 % |
| `.dockerignore` complet | Évite des dizaines de Mo inutiles |
| `--no-cache-dir` (pip), `npm ci --omit=dev` | Pas de caches dans l'image |
| Fusionner les `RUN apt-get` + nettoyer `/var/lib/apt/lists` | -10 à -50 Mo |

## 6. Commandes de diagnostic

```bash
docker images                     # tailles des images
docker history mon-image:1.0      # poids de chaque couche
docker scout cves mon-image:1.0   # scan de vulnérabilités (si Docker Scout)
docker exec -it conteneur sh      # ouvrir un shell dans le conteneur
docker stats                      # CPU / mémoire en temps réel
docker compose logs -f api        # suivre les logs d'un service
```

## 7. Checklist finale avant la production

- [ ] Build **multi-stage** (image finale sans outils de build)
- [ ] Image de base **alpine/slim** avec un **tag précis**
- [ ] **`.dockerignore`** présent et complet
- [ ] Conteneur en **utilisateur non-root**
- [ ] Aucune valeur secrète dans le Dockerfile ni dans Git
- [ ] Configuration injectée par **variables d'environnement**
- [ ] **Healthcheck** défini
- [ ] Image **scannée** (vulnérabilités) et **taggée par version**
- [ ] Limites **mémoire/CPU** définies en production
- [ ] `docker compose config` valide et stack testée (`up -d --build`)

## 8. Pour aller plus loin

- **Docker Compose** : orchestrer plusieurs conteneurs (front + API + DB).
- **CI/CD** : construire et pousser l'image automatiquement (GitLab CI, GitHub Actions).
- **Kubernetes** : déployer et mettre à l'échelle les images en production.
- **Registry privé** : héberger ses images (Docker Hub, GitLab, AWS ECR).

> Ces sujets prolongent naturellement ce cours : une fois l'application correctement
> dockerisée, l'étape suivante est son déploiement automatisé et son orchestration.
