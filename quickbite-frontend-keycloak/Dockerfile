# ---- Build stage ----
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package.json package-lock.json ./
RUN npm ci

# Build the Angular app in production mode
COPY . .
RUN npm run build -- --configuration production

# ---- Runtime stage ----
FROM nginx:alpine

# SPA-aware nginx config (deep links fall back to index.html)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the compiled browser bundle from the build stage
COPY --from=build /app/dist/quickbite-frontend-keycloak/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
