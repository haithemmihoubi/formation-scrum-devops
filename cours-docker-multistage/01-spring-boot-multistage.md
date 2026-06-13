# Dockeriser une application Java Spring Boot (multi-stage)

## 1. Objectif

Construire une image Spring Boot **petite, sécurisée et rapide à reconstruire**, en
utilisant un build multi-stage avec **Maven** (puis une variante **Gradle**).

## 2. Dockerfile complet — Maven

```dockerfile
# ---------- Étape 1 : build ----------
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# 1) On copie d'abord le pom.xml seul → couche de dépendances réutilisable
COPY pom.xml .
RUN mvn -B dependency:go-offline       # télécharge les dépendances (mises en cache)

# 2) Puis le code source → seule cette couche change quand on code
COPY src ./src
RUN mvn -B clean package -DskipTests

# ---------- Étape 2 : runtime ----------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Ne pas tourner en root : on crée un utilisateur applicatif
RUN addgroup -S app && adduser -S app -G app
USER app

# Variable d'environnement par défaut (surchargée au run)
ENV SPRING_PROFILES_ACTIVE=prod

# On copie UNIQUEMENT le jar produit par le stage build
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Pourquoi cet ordre de `COPY` ?

Docker met chaque couche en cache. Si on copie le `pom.xml` **avant** le code, alors
tant que les dépendances ne changent pas, Docker **réutilise le cache** de
`dependency:go-offline`. On ne re-télécharge pas Internet à chaque modification de code.
C'est la règle d'or n°2 (optimisation du cache).

## 3. Variante Gradle

```dockerfile
# ---------- build ----------
FROM gradle:8-jdk21 AS build
WORKDIR /app
COPY build.gradle settings.gradle ./
RUN gradle dependencies --no-daemon || true   # cache des dépendances
COPY src ./src
RUN gradle bootJar --no-daemon -x test

# ---------- runtime ----------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## 4. Optimisation avancée : les « layered jars » Spring Boot

Spring Boot peut découper le `.jar` en couches (dépendances, loader, classes de
l'application). Les dépendances changent rarement → couche en cache ; seul votre code
change → couche minuscule reconstruite.

```dockerfile
# ---------- build ----------
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src ./src
RUN mvn -B clean package -DskipTests

# ---------- extraction des couches ----------
FROM eclipse-temurin:21-jre-alpine AS extract
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

# ---------- runtime ----------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --from=extract /app/dependencies/ ./
COPY --from=extract /app/spring-boot-loader/ ./
COPY --from=extract /app/snapshot-dependencies/ ./
COPY --from=extract /app/application/ ./
EXPOSE 8080
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

## 5. Le fichier `.dockerignore` (indispensable)

Évite d'envoyer des fichiers inutiles au démon Docker (build plus rapide, image propre) :

```gitignore
target/
.git/
.idea/
*.iml
.mvn/
README.md
*.md
.env
```

## 6. Bonnes pratiques Spring Boot en conteneur

| Bonne pratique | Pourquoi |
|----------------|----------|
| JRE Alpine plutôt que JDK complet | Image ~5× plus petite |
| `USER app` (non-root) | Sécurité : limite l'impact d'une faille |
| Externaliser la config (`SPRING_PROFILES_ACTIVE`, env) | Une même image pour tous les environnements |
| Healthcheck via Actuator `/actuator/health` | Orchestrateur sait si l'app est prête |
| `-XX:MaxRAMPercentage=75` | La JVM respecte la limite mémoire du conteneur |

Exemple de healthcheck dans `docker-compose.yml` :

```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:8080/actuator/health"]
  interval: 10s
  timeout: 3s
  retries: 5
```

## 7. Commandes utiles

```bash
docker build -t quickbite-api:1.0 .
docker run -p 8080:8080 -e SPRING_PROFILES_ACTIVE=prod quickbite-api:1.0
docker images quickbite-api          # vérifier la taille
docker history quickbite-api:1.0     # voir les couches
```
