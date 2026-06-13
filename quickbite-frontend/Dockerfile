# ---- Build stage ----
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package.json package-lock.json ./
RUN npm ci

# Build the Angular app in production mode
COPY . .
RUN npm run build

# ---- Runtime stage ----
FROM nginx:alpine

# SPA-aware nginx config (deep links fall back to index.html)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the compiled browser bundle from the build stage
COPY --from=build /app/dist/quickbite-frontend/browser /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1

LABEL org.opencontainers.image.title="QuickBite Frontend" \
      org.opencontainers.image.description="Frontend Angular de l'API QuickBite" \
      org.opencontainers.image.version="1.0.0"

CMD ["nginx", "-g", "daemon off;"]
