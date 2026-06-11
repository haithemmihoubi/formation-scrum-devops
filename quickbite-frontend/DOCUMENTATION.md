# QuickBite — Front Angular · Documentation complète

Formateur : **Haithem Mihoubi**

Front **Angular 17** (standalone) qui consomme l'API QuickBite : login JWT,
intercepteur de token, routes protégées par guards, affichage selon le rôle.

---

## 1. Architecture

```
Navigateur ──► Angular (4200) ──HTTP + Bearer──► API QuickBite (8080 ou 8082)
                  │
                  ├─ AuthService   : login/refresh/logout, décodage du JWT, signals
                  ├─ Interceptor   : ajoute Authorization, gère le 401
                  └─ Guards        : authGuard, adminGuard
```

## 2. Pré-requis
- **Node.js 18+** et **npm**
- Une API QuickBite démarrée (projet `../atelier-quickbite` sur `:8080`,
  ou `../quickbite-keycloak` sur `:8082`).

## 3. Commandes

```bash
npm install            # installer les dépendances
npm start              # serveur de dev -> http://localhost:4200
npm run build          # build de production (dist/)
```

## 4. Configuration
L'URL de l'API est dans **`src/environments/environment.ts`** (`apiUrl`).

| Backend visé | `apiUrl` |
|--------------|----------|
| JWT maison (`atelier-quickbite`) | `http://localhost:8080` |
| Keycloak (`quickbite-keycloak`) | `http://localhost:8082` |

> Le CORS de chaque API autorise déjà `http://localhost:4200`.

## 5. Comptes de démonstration

| Utilisateur | Mot de passe | Voit la console Admin ? |
|-------------|--------------|--------------------------|
| `admin` (`admin123` JWT / `admin` Keycloak) | … | ✅ |
| `client` (`client123` JWT / `client` Keycloak) | … | ❌ |

## 6. Fonctionnalités démontrées
- Page **Login** → stockage des tokens, décodage du rôle.
- **Intercepteur** : `Authorization: Bearer …` + déconnexion automatique sur 401.
- **Guards** : `authGuard` (connecté), `adminGuard` (rôle admin).
- **Commandes** : lister / créer ; *Supprimer* visible uniquement pour ADMIN.
- **Admin** : page réservée au rôle admin.

## 7. Structure
```
src/app/
├── app.component.ts        barre de navigation + état connecté
├── app.config.ts           router + HttpClient + intercepteur
├── app.routes.ts           routes protégées par guards
├── core/  (auth.service, auth.interceptor, auth.guard, api.service, models)
└── pages/ (login, orders, admin)
```

## 8. Tester l'API derrière le front
Les collections **Postman** sont fournies dans les projets backend :
- `../atelier-quickbite/postman/QuickBite.postman_collection.json`
- `../quickbite-keycloak/postman/QuickBite-Keycloak.postman_collection.json`

## 9. Dépannage
| Symptôme | Solution |
|----------|----------|
| Erreur CORS | Vérifier que l'API tourne et autorise `localhost:4200` |
| 401 immédiat | Token expiré → se reconnecter ; vérifier `apiUrl` |
| Port 4200 occupé | `ng serve --port 4300` |
