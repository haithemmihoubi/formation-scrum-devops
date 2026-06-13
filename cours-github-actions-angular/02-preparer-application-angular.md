# Préparer l'application Angular pour la production

GitHub Actions automatise un déploiement, mais encore faut-il que l'application sache
**se construire et se servir** de façon reproductible. La brique de base : une **image
Docker multi-stage**.

## 1. Pourquoi Docker plutôt que copier le `dist/` ?

| Approche | Problème |
|----------|----------|
| Copier `dist/` via `scp` | Il faut Node + Nginx déjà configurés sur le serveur, versions qui dérivent |
| **Image Docker** | Tout est figé dans l'image : « ça marche sur le runner = ça marche en prod » |

Une image Docker rend le déploiement **atomique** (on lance une image, point) et
**réversible** (on peut relancer l'ancienne en cas de souci).

## 2. Le Dockerfile multi-stage

Une application Angular se **compile** avec Node.js, puis se **sert** avec Nginx. On
sépare donc en deux étapes : Node ne survit pas en production, ce qui donne une image
finale minuscule (~50 Mo au lieu de ~1 Go).

```dockerfile
# ---------- Étape 1 : build ----------
FROM node:20-alpine AS build
WORKDIR /app

# Dépendances d'abord → cache de couche Docker
COPY package.json package-lock.json ./
RUN npm ci

# Puis le code et le build de production
COPY . .
RUN npm run build -- --configuration production

# ---------- Étape 2 : runtime ----------
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Angular 17+ : la sortie est dans dist/<app>/browser
COPY --from=build /app/dist/quickbite-frontend/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

> **Attention au chemin de sortie** selon la version d'Angular :
> - Angular **≤ 16** : `dist/<nom-app>`
> - Angular **17+** (builder `application`) : `dist/<nom-app>/browser`

## 3. La configuration Nginx pour une SPA

Indispensable : une application Angular est une **SPA** (Single Page Application). Toutes
les routes inconnues doivent retomber sur `index.html`, sinon rafraîchir la page sur
`/orders` renvoie une **erreur 404**.

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;

    # Cache long des assets versionnés (nom avec hash)
    location ~* \.(?:js|css|woff2?|svg|png|jpg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Routage SPA : tout le reste retombe sur index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 4. Le `.dockerignore`

On évite d'envoyer `node_modules` et `dist` dans le contexte de build (build plus rapide,
image plus saine) :

```gitignore
node_modules
dist
.angular
.git
Dockerfile
.dockerignore
*.md
```

## 5. Vérifier en local avant d'automatiser

**Règle d'or :** si ça ne marche pas en local, ça ne marchera pas dans le CI. On valide
l'image manuellement **une fois** :

```bash
docker build -t quickbite-frontend:test .
docker run -p 8080:80 quickbite-frontend:test
# → ouvrir http://localhost:8080 et tester les routes (F5 sur /orders)
```

Une fois cette image fonctionnelle, GitHub Actions ne fera que **rejouer ces mêmes
commandes** automatiquement à chaque push. C'est l'objet des modules suivants.

> Pour approfondir le multi-stage (Spring Boot, React, Python, multi-environnement),
> voir le cours dédié *« Dockeriser ses applications »*.
