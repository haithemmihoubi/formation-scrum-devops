# Introduction : Docker & le build multi-stage

## 1. Rappels essentiels

Docker permet d'empaqueter une application **avec tout son environnement d'exécution**
(runtime, dépendances, fichiers) dans une **image** portable. Un **conteneur** est une
instance en cours d'exécution de cette image.

| Notion | Définition courte |
|--------|-------------------|
| **Image** | Modèle en lecture seule, construit à partir d'un `Dockerfile`. |
| **Conteneur** | Instance exécutée d'une image (processus isolé). |
| **Layer (couche)** | Chaque instruction du Dockerfile crée une couche mise en cache. |
| **Registry** | Dépôt d'images (Docker Hub, GitLab Registry, ECR…). |
| **Volume** | Stockage persistant indépendant du cycle de vie du conteneur. |

## 2. Le problème que résout le multi-stage

Pour compiler une application (Java, Angular, React…), on a besoin d'**outils de build**
lourds : JDK + Maven, Node.js + npm, compilateurs… Mais pour **exécuter** l'application,
on n'a besoin que du **résultat** (un `.jar`, des fichiers statiques).

Sans multi-stage, l'image finale contient tout : outils de build **+** code source **+**
caches. Résultat : une image de **800 Mo à 1,5 Go**, plus lente à transférer et avec une
surface d'attaque plus grande.

> Le **build multi-stage** sépare la phase de **compilation** de la phase d'**exécution**.
> On compile dans une première image (« stage build »), puis on copie **uniquement
> l'artefact final** dans une seconde image minimale (« stage runtime »).

## 3. Syntaxe d'un build multi-stage

```dockerfile
# ---------- Stage 1 : build ----------
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY . .
RUN mvn -B clean package -DskipTests

# ---------- Stage 2 : runtime ----------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/app.jar app.jar   # on ne copie QUE le jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Points clés :

- `FROM ... AS build` : on **nomme** le premier stage.
- `COPY --from=build` : on copie depuis ce stage nommé, pas depuis la machine hôte.
- Tout ce qui reste dans le stage `build` (JDK, Maven, `.m2`, sources) **n'est pas**
  dans l'image finale.

## 4. Gain typique

| Approche | Taille image | Surface d'attaque |
|----------|--------------|-------------------|
| Mono-stage (JDK + Maven inclus) | ~750 Mo | Élevée |
| Multi-stage (JRE Alpine seul) | ~180 Mo | Faible |

## 5. Les 3 règles d'or de ce cours

1. **Séparer build et runtime** → image finale minimale.
2. **Optimiser le cache** → copier les fichiers de dépendances *avant* le code source.
3. **Ne jamais tourner en `root`** → créer un utilisateur dédié dans l'image.

Les modules suivants appliquent ces règles à Spring Boot, au multi-environnement,
puis à Angular, React et Python.
