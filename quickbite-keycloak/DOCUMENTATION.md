# QuickBite — Keycloak (enterprise) · Documentation complète

Formateur : **Haithem Mihoubi**

API REST sécurisée par **Keycloak** (OAuth2 / OpenID Connect). L'API est un
**resource server** ; une **façade `/auth`** expose signup / login / refresh /
logout pour que les clients (front, mobile, Postman) n'aient pas à parler
directement à Keycloak.

---

## 1. Architecture

```
                 ┌─────────────────────── docker-compose ───────────────────────┐
  Client / Front │                                                               │
  (Postman,      │   ┌──────────┐   façade /auth   ┌────────────┐  OIDC/JWKS     │
   navigateur) ──┼──►│   API     │◄────────────────►│  Keycloak  │◄──── valide ───┤
                 │   │ (Spring) │   resource server │  (OIDC)    │   les tokens   │
                 │   └────┬─────┘                   └─────┬──────┘                │
                 │        │ JPA                            │ JPA                   │
                 │   ┌────┴─────┐                    ┌─────┴──────┐                │
                 │   │ app-db   │                    │ keycloak-db│                │
                 │   │(Postgres)│                    │ (Postgres) │                │
                 │   └──────────┘                    └────────────┘                │
                 └───────────────────────────────────────────────────────────────┘
```

- **Identité déléguée** : aucun mot de passe géré par l'API.
- **Signup** : l'API crée les comptes via l'**Admin API** de Keycloak, avec un
  **service account** (`quickbite-backend`) — pas d'identifiants admin en dur.
- **Rôles** : les rôles Keycloak (`realm_access.roles`) sont mappés en
  autorités Spring `ROLE_*` ; le RBAC est appliqué par `@PreAuthorize`.

| Composant | Image / techno | Port hôte |
|-----------|----------------|-----------|
| keycloak | quay.io/keycloak/keycloak:24.0 | 8080 |
| keycloak-db | postgres:16 | — |
| api | Spring Boot 3.3 (Java 21) | 8082 |
| app-db | postgres:16 | — |

---

## 2. Pré-requis
- **Docker** + **Docker Compose** (rien d'autre : Java/Maven sont dans l'image de build).

## 3. Commandes

```bash
# Démarrer toute la pile (build inclus)
docker compose up -d --build

# État des services (attendre "healthy")
docker compose ps

# Logs
docker compose logs -f api
docker compose logs -f keycloak

# Tests automatiques (signup/login/refresh/RBAC) dans le réseau docker
./test-api.sh

# Arrêt
docker compose down          # conserve les données
docker compose down -v       # supprime aussi les bases (réimporte le realm au prochain up)
```

- Console Keycloak : http://localhost:8080 — admin / admin
- API : http://localhost:8082

> ⚠️ Après modification du realm (`keycloak/realm-quickbite.json`), il faut
> `docker compose down -v` puis `up` : l'import ne s'exécute que sur une base vierge.

---

## 4. Comptes par défaut

| Utilisateur | Mot de passe | Rôles |
|-------------|--------------|-------|
| `admin`  | `admin`  | admin, client |
| `client` | `client` | client |

De nouveaux comptes se créent via `POST /auth/register` (rôle `client`).

---

## 5. Référence de l'API

Base URL : `http://localhost:8082`

### Authentification (façade publique)

| Méthode | Endpoint | Corps | Réponse |
|--------|----------|-------|---------|
| POST | `/auth/register` | `{username,email,password,firstName?,lastName?}` | `201` `{id,username,role}` |
| POST | `/auth/login` | `{username,password}` | `200` `{access_token,refresh_token,expires_in,...}` |
| POST | `/auth/refresh` | `{refreshToken}` | `200` `{access_token,refresh_token,...}` |
| POST | `/auth/logout` | `{refreshToken}` | `204` |

### Ressources protégées (Bearer access_token)

| Méthode | Endpoint | Accès | Description |
|--------|----------|-------|-------------|
| GET | `/health` | public | État du service |
| GET | `/me` | authentifié | Identité + rôles du token |
| GET | `/orders` | authentifié | Mes commandes |
| POST | `/orders` | `client` ou `admin` | Créer `{item,price}` |
| DELETE | `/orders/{id}` | `admin` | Supprimer |
| GET | `/admin/summary` | `admin` | Statistiques |

Codes : **401** non authentifié · **403** authentifié sans le rôle requis.

### Exemple de bout en bout (curl, depuis le poste)

```bash
API=http://localhost:8082

# 1) Signup
curl -s -X POST $API/auth/register -H "Content-Type: application/json" \
  -d '{"username":"sarah","email":"sarah@quickbite.local","password":"secret123"}'

# 2) Login -> récupérer le token
TOKEN=$(curl -s -X POST $API/auth/login -H "Content-Type: application/json" \
  -d '{"username":"sarah","password":"secret123"}' | jq -r .access_token)

# 3) Appels protégés
curl -s $API/me     -H "Authorization: Bearer $TOKEN"
curl -s $API/orders -H "Authorization: Bearer $TOKEN"
curl -s -X POST $API/orders -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"item":"Sushi","price":12}'
```

> La façade `/auth` proxy vers Keycloak en interne (`http://keycloak:8080`), donc
> depuis le poste **tout passe par `localhost:8082`** — pas besoin de modifier `/etc/hosts`.

---

## 6. Postman
Importer **`postman/QuickBite-Keycloak.postman_collection.json`**.
Ordre conseillé : `Register` → `Login` → `Me` / `Orders` → `Refresh` →
`Admin summary` (avec `Login ADMIN`) → `Logout`. Le login/refresh enregistrent
automatiquement `accessToken` et `refreshToken`.

---

## 7. Sécurité & points enterprise
- Provisioning des comptes par **service account** à droits limités (`manage-users`, `view-realm`).
- **Hostname stable** Keycloak → issuer de token constant pour tous.
- **Healthchecks** + `depends_on: service_healthy` sur chaque service.
- **Stateless**, CORS maîtrisé, méthodes protégées par `@PreAuthorize`.
- Bases **séparées et persistantes** (volumes) pour Keycloak et l'application.

## 8. Dépannage
| Symptôme | Cause / solution |
|----------|------------------|
| Keycloak `unhealthy` au 1er `up` | Laisser ~60 s (start_period) ; sinon `docker compose logs keycloak` |
| `401` au login d'un compte créé | Profil incomplet (Verify Profile) — déjà désactivé dans le realm |
| Realm non mis à jour | `docker compose down -v` puis `up` (réimport sur base vierge) |
| Port 8080/8082 occupé | Libérer le port ou adapter le mapping dans `docker-compose.yml` |
