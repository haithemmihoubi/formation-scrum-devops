# QuickBite — version Keycloak (enterprise, tout en Docker Compose)

API REST sécurisée par **Keycloak** (OAuth2 / OpenID Connect). L'API est un
**resource server** : elle ne gère ni login ni mots de passe — c'est Keycloak
qui authentifie les utilisateurs et émet les tokens JWT. Toute la pile démarre
en **une commande**.

> ✅ Vérifié de bout en bout : Keycloak émet les tokens, l'API les valide, les
> rôles Keycloak sont mappés (`realm_access.roles` → `ROLE_*`) et le RBAC est
> appliqué (admin → 200, client → 403).

## Architecture (docker-compose)

| Service | Rôle | Port hôte |
|---------|------|-----------|
| **keycloak** | Serveur d'identité (import auto du realm `quickbite`) | 8080 |
| **keycloak-db** | PostgreSQL dédié à Keycloak | — |
| **api** | API Spring Boot (resource server OIDC) | 8082 |
| **app-db** | PostgreSQL de l'application | — |

## Démarrage

```bash
docker compose up -d --build
# Attendre que tout soit "healthy" :
docker compose ps
```

- Console Keycloak : http://localhost:8080  (admin / admin)
- API : http://localhost:8082

## Utilisateurs (créés par l'import du realm)

| Utilisateur | Mot de passe | Rôles |
|-------------|--------------|-------|
| `admin`  | `admin`  | admin, client |
| `client` | `client` | client |

## Tester

### Option A — script fourni (dans le réseau docker)
```bash
./test-api.sh
```

### Option B — manuellement depuis votre poste
L'issuer des tokens est `http://keycloak:8080`. Pour que votre poste utilise la
même URL que les conteneurs, ajoutez une ligne à `/etc/hosts` :

```
127.0.0.1   keycloak
```

Puis :
```bash
# 1) obtenir un token (grant password, client public "quickbite")
TOKEN=$(curl -s -X POST http://keycloak:8080/realms/quickbite/protocol/openid-connect/token \
  -d client_id=quickbite -d grant_type=password \
  -d username=admin -d password=admin | jq -r .access_token)

# 2) appeler l'API
curl -s http://localhost:8082/me            -H "Authorization: Bearer $TOKEN"
curl -s http://localhost:8082/admin/summary -H "Authorization: Bearer $TOKEN"
```

## Endpoints

| Méthode | URL | Accès |
|--------|-----|-------|
| GET | `/health` | public |
| GET | `/me` | authentifié |
| GET | `/orders` | authentifié |
| POST | `/orders` | rôle `client` ou `admin` |
| DELETE | `/orders/{id}` | rôle `admin` |
| GET | `/admin/summary` | rôle `admin` |

## Points « enterprise »
- **Séparation des responsabilités** : l'identité est entièrement déléguée à Keycloak.
- **Bases dédiées** : Keycloak et l'application ont chacun leur PostgreSQL persistant (volumes).
- **Hostname stable** : `KC_HOSTNAME=keycloak` → l'issuer des tokens est constant pour tous (conteneurs et poste).
- **Healthchecks** sur chaque service + `depends_on: condition: service_healthy`.
- **Mapping de rôles** Keycloak → autorités Spring dans `SecurityConfig`.
- **Stateless**, CORS maîtrisé, méthode sécurisée par `@PreAuthorize`.

## Arrêter
```bash
docker compose down          # garde les données (volumes)
docker compose down -v       # supprime aussi les bases
```

## Réutiliser le front Angular
Le front [`../quickbite-frontend`](../quickbite-frontend) peut être adapté pour
se connecter à Keycloak (Authorization Code + PKCE, client `quickbite`,
`issuer http://keycloak:8080/realms/quickbite`) au lieu du JWT maison.
