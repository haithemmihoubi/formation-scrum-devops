# QuickBite — version JWT « maison » · Documentation complète

Formateur : **Haithem Mihoubi**

API REST Spring Boot 3 sécurisée par **JWT** géré par l'application (sans
serveur d'identité externe). Idéale pour comprendre la mécanique interne :
filtre JWT, génération/validation des tokens, refresh avec rotation, RBAC.

> Pour la variante **enterprise déléguée à Keycloak**, voir le projet voisin
> `../quickbite-keycloak`.

---

## 1. Architecture

```
Client ──► [Filtre JWT] ──► SecurityFilterChain ──► Contrôleurs (@PreAuthorize)
                │                                          │
          valide le token                            JPA / base
                                                  ┌─────────────┐
                                                  │ H2 (dev) ou │
                                                  │ PostgreSQL  │
                                                  └─────────────┘
```

- Authentification **stateless** par token JWT signé (HMAC).
- **Access token** court + **refresh token** persistant avec **rotation**.
- Utilisateurs/rôles en base, mots de passe **BCrypt**.
- RBAC par `@PreAuthorize` (`ROLE_ADMIN`, `ROLE_CLIENT`).

---

## 2. Pré-requis
- **JDK 21**, **Maven 3.8+** (base **H2** par défaut, aucune installation de DB).
- Optionnel : **Docker** (profil PostgreSQL + compose).

## 3. Commandes

```bash
# Lancer (H2 en mémoire)
mvn spring-boot:run                 # http://localhost:8080

# Tests automatiques (9 tests : auth, RBAC, signup)
mvn test

# Packager un jar exécutable
mvn clean package
java -jar target/quickbite-api-1.0.0.jar

# Stack conteneurisée (API + PostgreSQL)
docker compose up -d --build

# Déploiement Kubernetes (manifestes fournis)
kubectl apply -f k8s/
```

Comptes de démo créés au démarrage :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| `admin`  | `admin123`  | ADMIN |
| `client` | `client123` | CLIENT |

---

## 4. Référence de l'API

Base URL : `http://localhost:8080`

### Authentification (public)

| Méthode | Endpoint | Corps | Réponse |
|--------|----------|-------|---------|
| POST | `/auth/register` | `{username,password}` (≥ 6 car.) | `201` `{accessToken,refreshToken,tokenType}` |
| POST | `/auth/login` | `{username,password}` | `200` `{accessToken,refreshToken,tokenType}` |
| POST | `/auth/refresh` | `{refreshToken}` | `200` `{accessToken,refreshToken,tokenType}` |
| GET | `/auth/me` | Bearer | identité + autorités |

### Ressources protégées (Bearer accessToken)

| Méthode | Endpoint | Accès |
|--------|----------|-------|
| GET | `/health` | public |
| GET | `/orders` | authentifié |
| POST | `/orders` | CLIENT ou ADMIN — `{item,price}` |
| DELETE | `/orders/{id}` | ADMIN |
| GET | `/admin/users` | ADMIN |

Codes : **401** non authentifié · **403** authentifié sans droit · **429** trop de tentatives de login (rate limiting).

### Exemple bout en bout

```bash
API=http://localhost:8080
# Signup (renvoie directement des tokens)
TOKEN=$(curl -s -X POST $API/auth/register -H "Content-Type: application/json" \
  -d '{"username":"sarah","password":"secret123"}' | jq -r .accessToken)
curl -s $API/auth/me -H "Authorization: Bearer $TOKEN"
curl -s -X POST $API/orders -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"item":"Tacos","price":7.5}'
```

---

## 5. Postman
Importer **`postman/QuickBite.postman_collection.json`**.
Ordre : `Register` (ou `Login ADMIN` / `Login CLIENT`) → `Me` → `Orders` →
`Refresh` → `Admin users`. Les tokens sont enregistrés automatiquement.

---

## 6. Sécurité appliquée
- Mots de passe **BCrypt**, jamais en clair.
- **Stateless** (`SessionCreationPolicy.STATELESS`), CSRF désactivé (API token).
- **Rate limiting** sur `/auth/login` (5/min → 429).
- Gestion d'erreurs neutre, CORS restreint, en-têtes de sécurité.
- Refresh tokens **persistés et révocables** (rotation).

## 7. Le cours associé
Le déroulé pas-à-pas de construction est dans **`ATELIERS.md`** (avec le code de chaque fichier).

## 8. Dépannage
| Symptôme | Solution |
|----------|----------|
| Port 8080 occupé | Arrêter l'autre service ou changer `server.port` |
| `429` au login en test | Attendre 1 min (fenêtre de rate limiting) |
| Passer à PostgreSQL | `SPRING_PROFILES_ACTIVE=postgres` (voir `application-postgres.yml`) |
