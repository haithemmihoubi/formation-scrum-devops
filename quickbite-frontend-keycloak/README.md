# QuickBite — Front Angular (Keycloak)

Front **Angular 17** complet branché sur l'API **QuickBite sécurisée par Keycloak**
(projet `../quickbite-keycloak`), via la façade `/auth`.

Formateur : **Haithem Mihoubi**.

## Fonctionnalités
- **Inscription** (signup) → crée un compte Keycloak (rôle `client`) et connecte.
- **Connexion / Déconnexion** (login/logout).
- **Refresh automatique** du token (intercepteur : sur 401, rejoue après refresh).
- **Commandes** : lister / créer ; suppression réservée à `admin`.
- **Console admin** : statistiques, réservée au rôle `admin`.
- **Navigation selon le rôle** (décodé depuis le JWT Keycloak `realm_access.roles`).

## Pré-requis
- Node.js 18+ et npm.
- L'API Keycloak démarrée : `cd ../quickbite-keycloak && docker compose up -d --build`.

## Démarrage
```bash
npm install
npm start            # http://localhost:4300
```
> Port **4300** (pour coexister avec l'autre front sur 4200). Le CORS de l'API autorise déjà `:4300`.

## Comptes de démo
| Utilisateur | Mot de passe | Admin ? |
|-------------|--------------|---------|
| `admin`  | `admin`  | ✅ |
| `client` | `client` | ❌ |
…ou créez-en un via **Créer un compte**.

## Configuration
`src/environments/environment.ts` → `apiUrl: 'http://localhost:8082'`.

## Détails techniques
- `tokens` au format Keycloak (`access_token` / `refresh_token`).
- Rôles lus dans `realm_access.roles` du JWT.
- Intercepteur avec **refresh-on-401** (un seul essai, sinon déconnexion).
