# Dockeriser une application React (Vite / CRA + Nginx)

## 1. Principe

Comme Angular, React se **compile** en fichiers statiques servis par Nginx. La seule
différence est le **dossier de sortie** du build, qui dépend de l'outil :

| Outil | Commande de build | Dossier de sortie |
|-------|-------------------|-------------------|
| **Vite** | `npm run build` | `dist/` |
| **Create React App (CRA)** | `npm run build` | `build/` |
| **Next.js (export statique)** | `next build && next export` | `out/` |

## 2. Dockerfile — React + Vite

```dockerfile
# ---------- Étape 1 : build ----------
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build          # Vite → dossier dist/

# ---------- Étape 2 : runtime ----------
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 3. Dockerfile — Create React App (CRA)

Seul le dossier copié change (`build` au lieu de `dist`) :

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build          # CRA → dossier build/

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 4. Configuration Nginx (routage SPA)

Identique à Angular — une SPA React (React Router) a besoin du fallback `index.html` :

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;

    location ~* \.(?:js|css|woff2?|svg|png|jpg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 5. Variables d'environnement React

⚠️ Avec Vite/CRA, les variables `VITE_*` / `REACT_APP_*` sont **figées au build**
(injectées dans le bundle). Deux stratégies :

**Option 1 — au build (simple, une image par environnement) :**
```dockerfile
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build
```
```bash
docker build --build-arg VITE_API_URL=https://api.prod.com -t app .
```

**Option 2 — au runtime (une seule image, recommandé) :** générer un `config.js`
au démarrage, comme pour Angular :

```bash
#!/bin/sh
cat > /usr/share/nginx/html/config.js <<EOF
window.APP_CONFIG = { apiUrl: "${API_URL:-http://localhost:8080}" };
EOF
exec nginx -g "daemon off;"
```

## 6. `.dockerignore`

```gitignore
node_modules
dist
build
.git
Dockerfile
*.md
.env.local
```

## 7. Commandes

```bash
docker build -t react-app:1.0 .
docker run -p 3000:80 react-app:1.0
# → http://localhost:3000
```
