# QuickBite — Front Angular

Front **Angular 17** (standalone) pour l'API QuickBite. Démontre l'authentification **JWT**, la protection des routes, l'**intercepteur** de token et l'affichage **selon le rôle** (CLIENT / ADMIN).

## Pré-requis
- Node.js 18+ et npm
- L'API QuickBite démarrée sur `http://localhost:8080` (voir `../atelier-quickbite`)

## Démarrage
```bash
npm install
npm start            # ou : ng serve
# ouvrir http://localhost:4200
```

> L'API autorise déjà l'origine `http://localhost:4200` (CORS configuré dans `SecurityConfig`).

## Comptes de démonstration
| Utilisateur | Mot de passe | Rôle | Voit la console Admin ? |
|-------------|--------------|------|--------------------------|
| `admin`  | `admin123`  | ADMIN  | ✅ oui |
| `client` | `client123` | CLIENT | ❌ non |

## Ce que démontre le front
- **Login** → récupère `accessToken` + `refreshToken`, décode le rôle depuis le JWT.
- **Intercepteur** : ajoute `Authorization: Bearer …` sur chaque appel API ; sur **401**, déconnecte.
- **Guards** : `authGuard` (connecté), `adminGuard` (rôle ADMIN).
- **Commandes** : lister / créer ; bouton *Supprimer* visible seulement pour ADMIN (l'API renvoie **403** sinon).
- **Admin** : `/admin/users` accessible uniquement en ADMIN.

## Structure
```
src/app/
├── app.component.ts        (barre de navigation + état connecté)
├── app.config.ts           (router + HttpClient + intercepteur)
├── app.routes.ts           (routes protégées par guards)
├── core/
│   ├── auth.service.ts     (login/refresh/logout, décodage JWT, signals)
│   ├── auth.interceptor.ts (Bearer + gestion 401)
│   ├── auth.guard.ts       (authGuard, adminGuard)
│   ├── api.service.ts      (orders, admin/users)
│   └── models.ts
└── pages/
    ├── login.component.ts
    ├── orders.component.ts
    └── admin.component.ts
```

## Configuration
L'URL de l'API est dans [src/environments/environment.ts](src/environments/environment.ts) (`apiUrl`).
