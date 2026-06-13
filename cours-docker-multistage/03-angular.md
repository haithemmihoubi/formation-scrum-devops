# Dockeriser une application Angular (multi-stage + Nginx)

## 1. Principe

Une application Angular est **compilée** en fichiers statiques (HTML/CSS/JS) par Node.js,
puis **servie** par un serveur web léger (Nginx). On a donc deux stages :

1. **build** : Node.js compile (`ng build`).
2. **runtime** : Nginx sert le dossier `dist/` — **pas de Node.js en production**.

## 2. Dockerfile complet

```dockerfile
# ---------- Étape 1 : build ----------
FROM node:20-alpine AS build
WORKDIR /app

# Dépendances d'abord (cache de couche)
COPY package.json package-lock.json ./
RUN npm ci

# Puis le code, puis le build de production
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

## 3. La configuration Nginx (`nginx.conf`)

Indispensable pour une **SPA** : toutes les routes inconnues doivent renvoyer
`index.html`, sinon un rafraîchissement sur `/orders` donne une erreur 404.

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Compression
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;

    # Cache agressif des assets versionnés (nom avec hash)
    location ~* \.(?:js|css|woff2?|ttf|svg|png|jpg|jpeg|gif|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }

    # Routage SPA : tout le reste retombe sur index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 4. Le `.dockerignore`

```gitignore
node_modules
dist
.angular
.git
Dockerfile
.dockerignore
*.md
```

## 5. Configurer l'URL de l'API selon l'environnement

Problème : l'URL de l'API back-end change entre dev et prod, mais on ne veut pas
recompiler l'image. Solution : **injecter la configuration au démarrage** via un
fichier `env.js` généré par un point d'entrée.

**`docker-entrypoint.sh`**
```bash
#!/bin/sh
# Génère un fichier JS lu par l'application au chargement
cat > /usr/share/nginx/html/assets/env.js <<EOF
window.__env = {
  apiUrl: "${API_URL:-http://localhost:8080}"
};
EOF
exec nginx -g "daemon off;"
```

Dans `index.html` : `<script src="assets/env.js"></script>` avant le bundle Angular.
On lance ensuite :

```bash
docker run -p 8080:80 -e API_URL=https://api.prod.exemple.com quickbite-frontend
```

## 6. Commandes

```bash
docker build -t quickbite-frontend:1.0 .
docker run -p 8080:80 quickbite-frontend:1.0
# → http://localhost:8080
```

Image finale typique : **~50 Mo** (Nginx Alpine + fichiers statiques), contre ~1 Go
si on avait gardé Node.js et `node_modules`.
