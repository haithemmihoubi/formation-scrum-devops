# QuickBite — Front Angular (Keycloak) · Documentation complète

Formateur : **Haithem Mihoubi**

Front **Angular 17** (standalone, signals) pour l'API QuickBite déléguée à
**Keycloak**. Toutes les fonctionnalités d'authentification passent par la
**façade `/auth`** de l'API (pas de redirection Keycloak côté navigateur).

---

## 1. Architecture

```
Navigateur (4300) ──HTTP + Bearer──► API QuickBite-Keycloak (8082) ──► Keycloak
   │  AuthService    : register / login / refresh / logout, décodage du JWT
   │  Interceptor    : ajoute le Bearer ; sur 401 -> refresh puis rejoue
   └  Guards         : authGuard (connecté), adminGuard (rôle admin)
```

## 2. Pré-requis
- Node.js 18+, npm.
- API Keycloak en marche : `cd ../quickbite-keycloak && docker compose up -d --build`.

## 3. Commandes
```bash
npm install          # dépendances
npm start            # dev server -> http://localhost:4300
npm run build        # build de prod (dist/)
```

## 4. Configuration
`src/environments/environment.ts` :
```ts
export const environment = { production: false, apiUrl: 'http://localhost:8082' };
```
Le CORS de l'API autorise `http://localhost:4300` (variable `CORS_ORIGINS`).

## 5. Parcours fonctionnels

| Écran | Route | Accès | Action |
|-------|-------|-------|--------|
| Connexion | `/login` | public | `POST /auth/login` |
| Inscription | `/signup` | public | `POST /auth/register` puis login |
| Commandes | `/orders` | connecté | `GET/POST /orders`, `DELETE` (admin) |
| Admin | `/admin` | rôle admin | `GET /admin/summary` |

## 6. Gestion des tokens
- Stockés en `localStorage` (`qbkc_access`, `qbkc_refresh`).
- Le JWT Keycloak est décodé pour extraire `preferred_username` et `realm_access.roles`.
- **Refresh automatique** : sur une réponse `401`, l'intercepteur appelle
  `POST /auth/refresh`, met à jour le token et rejoue la requête ; en cas
  d'échec, déconnexion + redirection `/login`.

## 7. Structure
```
src/app/
├── app.component.ts        nav + état connecté (rôle)
├── app.config.ts           router + HttpClient + intercepteur
├── app.routes.ts           routes + guards (lazy)
├── core/
│   ├── auth.service.ts     register/login/refresh/logout, décodage realm_access
│   ├── auth.interceptor.ts Bearer + refresh-on-401
│   ├── auth.guard.ts       authGuard, adminGuard
│   ├── api.service.ts      orders + admin/summary
│   └── models.ts
└── pages/  (login, signup, orders, admin)
```

## 8. Vérifié
- `npm install` + `ng build` : **OK** (bundle généré).
- Chaîne navigateur (Origin `:4300`) → API `:8082` : signup **201**, login OK,
  `/orders` **200/201**, `/admin` (client) **403**. CORS préflight **OK**.

## 9. Dépannage
| Symptôme | Solution |
|----------|----------|
| Erreur CORS | Vérifier que l'API tourne et que `:4300` est dans `CORS_ORIGINS` (recréer le conteneur api) |
| 401 en boucle | Refresh token expiré → se reconnecter |
| Port 4300 occupé | `ng serve --port 4400` (penser au CORS) |
