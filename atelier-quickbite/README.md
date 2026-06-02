# QuickBite API — projet fil rouge de la formation

Petit projet **Spring Boot 3 / Java 21** qui grandit atelier après atelier, pour appliquer concrètement les notions de la formation (Agilité, DevOps, Spring Security).

Formateur : **Haithem Mihoubi**.

## Démarrage express

```bash
mvn spring-boot:run
curl http://localhost:8080/health
```

Base **H2 en mémoire** par défaut (aucune installation). Utilisateurs de test :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| `admin`  | `admin123`  | ADMIN |
| `client` | `client123` | CLIENT |

## Tester l'API

- **Postman** : importez [`postman/QuickBite.postman_collection.json`](postman/QuickBite.postman_collection.json). Le login enregistre automatiquement les tokens.
- **curl** : voir les exemples dans [`ATELIERS.md`](ATELIERS.md).

## Endpoints

| Méthode | URL | Accès |
|--------|-----|-------|
| GET | `/health` | public |
| POST | `/auth/login` | public |
| POST | `/auth/refresh` | public |
| GET | `/auth/me` | authentifié |
| GET/POST | `/orders` | authentifié / CLIENT |
| DELETE | `/orders/{id}` | ADMIN |
| GET | `/admin/users` | ADMIN |

## Le guide des ateliers

Le déroulé complet, étape par étape (0 → durcissement → DevOps), est dans **[ATELIERS.md](ATELIERS.md)**.

## DevOps

```bash
docker compose up -d --build      # API + PostgreSQL
kubectl apply -f k8s/             # déploiement Kubernetes
```

## Pile technique

Spring Boot 3.3, Spring Security 6, JWT (JJWT), JPA/Hibernate, H2 / PostgreSQL, Docker, GitHub Actions, Kubernetes.
