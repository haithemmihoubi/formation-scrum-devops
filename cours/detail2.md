# MODULE 2 — Culture & outils DevOps

## Chapitre 9 — Qu'est-ce que le DevOps, vraiment ?

### 9.1 Le problème : le « mur de la confusion »

Pour comprendre le DevOps, il faut comprendre le conflit qu'il résout. Dans une organisation informatique classique, il existe deux équipes aux objectifs **opposés** :

- Les **développeurs** (*Dev*) sont récompensés quand ils livrent du **changement** : de nouvelles fonctionnalités, vite. Leur instinct est de pousser des modifications en permanence.
- Les **opérations** (*Ops*) — ceux qui exploitent les serveurs en production — sont récompensés quand le système est **stable**. Or, chaque changement est une source potentielle de panne. Leur instinct est donc de **freiner** les changements.

Ces deux équipes se renvoyaient la responsabilité par-dessus un « mur » imaginaire. Le développeur livrait son code en disant « ça marche sur ma machine », et l'opérationnel, quand ça plantait en production, répondait « ce n'est pas un problème de serveur, c'est votre code ». Personne n'était responsable de bout en bout. Les déploiements étaient donc **rares, manuels, stressants et risqués** — on déployait parfois une fois par trimestre, en pleine nuit, en croisant les doigts.

### 9.2 La réponse : réunir Dev et Ops

Le mouvement **DevOps** (le mot est la contraction de *Development* et *Operations*), popularisé vers 2009 lors des premières conférences *DevOpsDays*, propose de **détruire ce mur**. L'idée : Dev et Ops partagent désormais une **responsabilité commune**, du code jusqu'à la production, soutenue par une forte **automatisation**.

<div class="callout note"><span class="title">📘 Ce que DevOps n'est pas</span>
Le DevOps n'est <b>ni un métier</b> (« je recrute un DevOps » est un abus de langage répandu), <b>ni un outil</b> qu'on installerait. C'est avant tout une <b>culture</b> et un ensemble de <b>pratiques</b> visant à raccourcir le temps entre une idée et sa mise en production, de manière fiable et répétable. Les outils (Docker, Kubernetes, etc.) ne sont que des moyens au service de cette culture.
</div>

### 9.3 Le modèle CAMS : les quatre piliers

On résume la culture DevOps par l'acronyme **CAMS** :

| Pilier | Idée | Exemple concret |
|--------|------|-----------------|
| **C — Culture** | Collaboration et responsabilité partagée entre Dev et Ops | Les développeurs sont d'astreinte sur leur propre code en production |
| **A — Automation** | Automatiser tout ce qui est répétitif et manuel | Le build, les tests et le déploiement se déclenchent tout seuls |
| **M — Measurement** | Mesurer pour pouvoir décider et s'améliorer | On suit le délai de livraison, le taux d'échec, le temps de réparation |
| **S — Sharing** | Partager le savoir et apprendre des incidents sans blâmer | On rédige des post-mortems « sans coupable » après chaque incident |

### 9.4 Comment mesurer si on fait du « bon » DevOps : les métriques DORA

Un programme de recherche (le *DevOps Research and Assessment*, ou DORA, racheté par Google) a identifié **quatre indicateurs** qui distinguent les équipes très performantes des autres :

1. **Fréquence de déploiement** — à quelle fréquence livre-t-on en production ? (Les meilleures équipes déploient plusieurs fois par jour.)
2. **Délai de livraison d'un changement** (*Lead Time for Changes*) — combien de temps s'écoule entre l'écriture du code et sa mise en production ?
3. **Taux d'échec des changements** (*Change Failure Rate*) — quel pourcentage de déploiements provoque un incident ?
4. **Temps moyen de rétablissement** (*MTTR*, *Mean Time To Restore*) — quand un incident survient, combien de temps faut-il pour rétablir le service ?

Les deux premières mesurent la **vitesse**, les deux dernières mesurent la **stabilité**. L'enseignement majeur de DORA est contre-intuitif : **vitesse et stabilité ne s'opposent pas**. Les meilleures équipes déploient à la fois plus souvent **et** avec moins de pannes — parce que de petits changements fréquents sont plus faciles à tester et à corriger que de gros changements rares.

### 9.5 CI, CD et CD : trois marches à ne pas confondre

Trois sigles très proches sèment la confusion. Distinguons-les clairement :

- **CI — Intégration Continue** (*Continuous Integration*) : à **chaque** modification du code, on l'intègre automatiquement au reste et on lance les tests. But : détecter les problèmes **immédiatement**, pas des semaines plus tard.
- **CD — Livraison Continue** (*Continuous Delivery*) : on va plus loin : à tout moment, l'application est dans un état **déployable**. Le déploiement vers la production reste déclenché **manuellement** (par un humain qui appuie sur le bouton).
- **CD — Déploiement Continu** (*Continuous Deployment*) : la dernière marche : le déploiement en production devient lui aussi **automatique**, sans intervention humaine, dès que les tests passent.

<div class="callout tip"><span class="title">💡 On gravit ces marches dans l'ordre</span>
On ne saute pas directement au déploiement continu. On commence par maîtriser l'<b>intégration continue</b> (avoir une suite de tests fiable), puis on automatise jusqu'à un produit toujours <b>déployable</b> (livraison continue), et enfin, lorsque la confiance est suffisante, on automatise le déploiement lui-même.
</div>

### 9.6 Le cycle de vie DevOps

On représente souvent le DevOps comme une boucle infinie, car le travail ne s'arrête jamais : ce qu'on apprend en production alimente la planification suivante.

```
   PLAN ─► CODE ─► BUILD ─► TEST ─► RELEASE ─► DEPLOY ─► OPERATE ─► MONITOR
     ▲                                                                  │
     └────────────────── boucle de feedback continue ───────────────────┘
```

- **Plan / Code** : on planifie (lien direct avec l'Agile du Module 1) et on écrit le code, géré dans Git.
- **Build / Test** : on compile et on lance les tests automatisés, plus des analyses de qualité et de sécurité.
- **Release / Deploy** : on produit un artefact versionné et on le déploie.
- **Operate / Monitor** : on exploite et on surveille le système en production. Les anomalies détectées repartent dans le « Plan ».

---

## Chapitre 10 — Git et le travail collaboratif

Tout commence par le code, et le code se gère avec **Git**, le système de gestion de versions universel. Nous supposons les bases connues ; concentrons-nous sur l'usage collaboratif.

### 10.1 Les commandes du quotidien

```bash
git init                          # créer un nouveau dépôt local
git clone <url>                   # copier un dépôt existant
git switch -c feature/paiement    # créer une branche et basculer dessus
git add .                         # préparer les fichiers modifiés
git commit -m "feat: ajout du paiement"   # enregistrer un instantané
git push -u origin feature/paiement       # envoyer la branche sur le serveur
# puis on ouvre une « Pull Request » (PR) ou « Merge Request » (MR)
```

Une **branche** est une ligne de développement parallèle : elle permet de travailler sur une fonctionnalité sans perturber le code principal. Une **Pull Request** est une demande de fusion de votre branche dans la branche principale, accompagnée d'une **revue** par un collègue.

### 10.2 Bien nommer ses commits : les Conventional Commits

Pour que l'historique soit lisible (et pour automatiser la génération de notes de version), on adopte une convention de préfixes pour les messages de commit :

```
feat:     une nouvelle fonctionnalité
fix:      une correction de bug
docs:     de la documentation
refactor: une refonte du code sans changement de comportement
test:     l'ajout ou la modification de tests
chore:    des tâches techniques (mise à jour de dépendances, configuration)
```

### 10.3 Les stratégies de branches

Il existe plusieurs manières d'organiser les branches d'un projet. Les trois principales :

| Stratégie | Principe | Convient à… |
|-----------|----------|-------------|
| **Git Flow** | Des branches durables (`main`, `develop`) et temporaires (`feature/*`, `release/*`, `hotfix/*`) | Des produits avec des versions planifiées |
| **GitHub Flow** | Une seule branche durable (`main`) + des branches courtes + des PR + un déploiement fréquent | Le web et le SaaS, livraison continue |
| **Trunk-Based** | On commit très souvent directement sur `main`, en cachant les fonctionnalités inachevées derrière des « feature flags » | Les équipes matures avec une CI solide |

<div class="callout warn"><span class="title">⚠️ Les branches qui vivent trop longtemps font mal</span>
Plus une branche reste isolée longtemps, plus elle diverge du code principal, et plus sa fusion devient un cauchemar de conflits. C'est exactement ce que l'<b>intégration continue</b> cherche à éviter : elle encourage des branches <b>courtes</b> (quelques jours au maximum) et des fusions <b>fréquentes</b>.
</div>

---

## Chapitre 11 — L'intégration continue (CI) expliquée

### 11.1 Ce qu'est un pipeline

Un **pipeline** est une suite d'étapes automatisées (on les appelle *stages*) qui se déclenchent toutes seules en réponse à un événement — typiquement, un `push` de code ou l'ouverture d'une Pull Request. Un pipeline d'intégration continue classique enchaîne :

```
push ─► [récupérer le code] ─► [installer les dépendances] ─► [analyser le style]
     ─► [compiler] ─► [lancer les tests] ─► [produire l'artefact] ─► (✓ ou ✗)
```

Trois principes guident un bon pipeline :

- **Rapide** : le retour doit arriver en quelques minutes, sinon les développeurs ne l'attendent pas.
- **Reproductible** : il doit s'exécuter de la même façon partout, avec les mêmes versions d'outils. C'est ce qui élimine le « ça marche sur ma machine ».
- **Fail fast** (« échouer vite ») : si une étape échoue, on arrête tout de suite et on prévient. Et la règle d'or : **on ne fusionne jamais une branche dont le pipeline est rouge.**

### 11.2 Un pipeline concret avec GitHub Actions

Avec GitHub Actions, on décrit le pipeline dans un fichier YAML placé dans le dossier `.github/workflows/`. Décortiquons un exemple pour une application Node.js :

```yaml
name: CI                          # nom du pipeline
on:                               # quand se déclenche-t-il ?
  push:
    branches: [ main ]            # à chaque push sur main
  pull_request:                   # et à chaque Pull Request
jobs:
  build-test:                     # un "job" = un ensemble d'étapes
    runs-on: ubuntu-latest        # sur quelle machine il tourne
    steps:
      - uses: actions/checkout@v4         # 1) récupère le code
      - uses: actions/setup-node@v4       # 2) installe Node.js
        with:
          node-version: '20'
          cache: 'npm'                    # met en cache les dépendances
      - run: npm ci                       # 3) installe les dépendances
      - run: npm run lint --if-present    # 4) vérifie le style du code
      - run: npm test                     # 5) lance les tests
```

Chaque ligne sous `steps` est une étape exécutée dans l'ordre. Si l'une échoue (par exemple un test qui ne passe pas), le pipeline s'arrête et est marqué « rouge ». Voici le test minimal que ce pipeline exécute :

```javascript
const sum = (a, b) => a + b;

test('additionne deux nombres', () => {
  expect(sum(2, 3)).toBe(5);   // si ce n'est pas 5, le test échoue
});
```

### 11.3 Le même pipeline avec GitLab CI

L'équivalent chez GitLab se nomme `.gitlab-ci.yml` et fonctionne sur le même principe d'étapes :

```yaml
stages: [build, test]           # les phases, dans l'ordre

build:
  stage: build
  image: node:20                # l'image Docker dans laquelle on travaille
  script:
    - npm ci
    - npm run build --if-present

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test
```

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 1 : votre premier pipeline CI</span>
1. Créez un dépôt avec une petite application et <b>un</b> test ; vérifiez d'abord que <code>npm test</code> passe en local.<br>
2. Ajoutez le fichier de workflow ci-dessus, poussez le code, et observez l'exécution du pipeline.<br>
3. <b>Cassez volontairement</b> le test (remplacez <code>toBe(5)</code> par <code>toBe(6)</code>) et poussez : constatez le pipeline qui devient rouge.<br>
4. Configurez la <b>protection de branche</b> sur <code>main</code> pour interdire toute fusion si le pipeline est rouge.
</div>

<div class="callout note"><span class="title">📘 Le moment où tout devient clair</span>
L'étape 3 de l'exercice est le déclic pédagogique : voir une fusion <b>bloquée</b> par un test qui échoue fait comprendre, mieux que n'importe quel discours, à quoi sert l'intégration continue. C'est un filet de sécurité qui empêche le code cassé d'atteindre la branche principale.
</div>

---

## Chapitre 12 — Docker et la conteneurisation

### 12.1 Le problème que Docker résout

Le « ça marche sur ma machine » a une cause technique précise : une application dépend de son **environnement** (la version exacte du langage, des bibliothèques, des variables système…). Si cet environnement diffère entre la machine du développeur, le serveur de test et la production, l'application peut se comporter différemment, voire planter.

**Docker** résout cela en **empaquetant l'application avec tout son environnement** dans une unité standardisée appelée un **conteneur**. Ce conteneur s'exécute de façon identique partout. Le « ça marche sur ma machine » devient « ça marche partout, à l'identique ».

### 12.2 Conteneur ou machine virtuelle ?

On compare souvent les conteneurs aux machines virtuelles. La différence est fondamentale :

```
   MACHINES VIRTUELLES                  CONTENEURS
 ┌──────────┬──────────┐            ┌──────────┬──────────┐
 │  App A   │  App B   │            │  App A   │  App B    │
 │  Libs    │  Libs    │            │  Libs    │  Libs     │
 │ OS invité│ OS invité│            ├──────────┴──────────┤
 ├──────────┴──────────┤            │   Moteur Docker     │
 │     Hyperviseur     │            ├─────────────────────┤
 ├─────────────────────┤            │  OS hôte (le noyau  │
 │   OS hôte           │            │  est partagé)       │
 ├─────────────────────┤            ├─────────────────────┤
 │     Matériel        │            │     Matériel        │
 └─────────────────────┘            └─────────────────────┘
   chaque VM embarque un             les conteneurs partagent
   OS complet : lourd, lent          le noyau de l'hôte : léger, rapide
```

Une **machine virtuelle** embarque un **système d'exploitation complet** : elle pèse plusieurs gigaoctets et met une à deux minutes à démarrer. Un **conteneur**, lui, **partage le noyau** du système hôte et n'embarque que l'application et ses dépendances : il pèse quelques dizaines de mégaoctets et démarre en quelques **millisecondes**. C'est cette légèreté qui rend les conteneurs si pratiques.

### 12.3 Le vocabulaire de Docker

| Terme | Définition | Analogie |
|-------|------------|----------|
| **Image** | Un modèle figé, en lecture seule, contenant l'application et son environnement | Le moule à gâteau (ou une « classe » en programmation) |
| **Conteneur** | Une instance de cette image, en cours d'exécution | Le gâteau sorti du moule (ou un « objet ») |
| **Volume** | Un espace de stockage qui persiste même quand le conteneur est détruit | Un disque dur externe |
| **Réseau** | Un réseau virtuel qui relie les conteneurs entre eux | Un petit réseau local privé |
| **Registry** (registre) | Un dépôt où l'on stocke et partage les images | Un « app store » d'images |

### 12.4 Les commandes essentielles

```bash
docker run -d -p 8080:80 --name web nginx   # lance un conteneur en arrière-plan
docker ps                                     # liste les conteneurs actifs
docker logs -f web                            # affiche et suit les logs
docker exec -it web sh                        # ouvre un terminal dans le conteneur
docker stop web && docker rm web              # arrête puis supprime le conteneur
docker images                                 # liste les images locales
```

Une explication s'impose sur `-p 8080:80` : cela **publie** le port 80 *interne* du conteneur sur le port 8080 de votre machine. C'est ce qui vous permet d'ouvrir `http://localhost:8080` pour accéder à l'application qui, à l'intérieur, écoute sur le port 80.

### 12.5 Le Dockerfile : la recette de l'image

Pour créer sa propre image, on écrit un **Dockerfile**, un fichier texte qui décrit, étape par étape, comment construire l'image. Voici un exemple **commenté** pour une application Node.js, utilisant la technique du **multi-stage build** (construction en plusieurs étapes) :

```dockerfile
# ---------- Étape 1 : la construction ----------
FROM node:20-alpine AS build      # on part d'une image Node légère, nommée "build"
WORKDIR /app                      # le dossier de travail dans le conteneur
COPY package*.json ./             # on copie d'abord SEULEMENT les fichiers de dépendances
RUN npm ci                        # on installe toutes les dépendances (y compris de dev)
COPY . .                          # puis on copie le reste du code source
RUN npm run build                 # on compile l'application (ex. TypeScript -> dist/)

# ---------- Étape 2 : l'exécution ----------
FROM node:20-alpine               # on repart d'une image propre et légère
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev             # on installe UNIQUEMENT les dépendances de production
COPY --from=build /app/dist ./dist  # on récupère le résultat compilé de l'étape 1
EXPOSE 3000                       # on documente le port utilisé
USER node                         # on n'exécute PAS en tant que root (sécurité)
CMD ["node", "dist/server.js"]    # la commande qui démarre l'application
```

Pourquoi cette construction en deux étapes ? Parce que les **outils de compilation** (compilateurs, dépendances de développement) sont volumineux et inutiles en production. L'étape 1 compile ; l'étape 2 ne récupère que le **résultat compilé**, dans une image propre. Résultat : l'image finale est beaucoup plus **petite** et plus **sûre**.

### 12.6 Les bonnes pratiques du Dockerfile

- Partez d'une **image de base minimale** (`-alpine`, `-slim`, ou *distroless*).
- **Ordonnez les instructions du moins changeant au plus changeant.** Docker met en cache chaque étape ; en copiant `package.json` *avant* le code source, on évite de réinstaller toutes les dépendances à chaque modification du code. C'est un gain de temps considérable.
- Utilisez le **multi-stage build** pour ne pas embarquer les outils de compilation.
- Ajoutez un fichier **`.dockerignore`** pour exclure ce qui ne doit pas entrer dans l'image (par exemple `node_modules`, `.git`).
- N'exécutez **jamais** en tant que `root` (`USER node`).
- Donnez des **tags de version explicites** à vos images plutôt que `latest`.

```text
# .dockerignore
node_modules
.git
*.log
dist
```

<div class="callout danger"><span class="title">❗ Ne mettez JAMAIS de secret dans une image</span>
Les images Docker sont constituées de couches que <b>n'importe qui peut inspecter</b>. Si vous copiez un mot de passe, une clé d'API ou un token dans l'image, il est récupérable, même si vous le « supprimez » dans une étape ultérieure (il reste dans une couche). Les secrets doivent être fournis <b>à l'exécution</b>, via des variables d'environnement ou un gestionnaire de secrets.
</div>

### 12.7 Docker Compose : orchestrer plusieurs conteneurs

Une vraie application a rarement un seul conteneur : il y a souvent l'application **et** sa base de données, par exemple. **Docker Compose** permet de décrire **plusieurs services** dans un seul fichier et de les démarrer ensemble :

```yaml
services:
  api:                              # premier service : notre application
    build: .                        # construite depuis le Dockerfile local
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://app:secret@db:5432/quickbite
    depends_on:
      - db                          # démarre après la base
    networks: [app-net]

  db:                               # second service : la base PostgreSQL
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: quickbite
    volumes:
      - db-data:/var/lib/postgresql/data   # persiste les données
    networks: [app-net]

volumes:
  db-data:                          # le volume nommé, persistant
networks:
  app-net:                          # le réseau privé qui relie api et db
```

Remarquez que l'API se connecte à la base via l'adresse `db:5432` : à l'intérieur du réseau Compose, **chaque service est accessible par son nom**. Les commandes principales :

```bash
docker compose up -d --build     # construit et démarre tous les services
docker compose ps                # affiche l'état des services
docker compose logs -f api       # suit les logs d'un service
docker compose down -v           # arrête tout et supprime les volumes
```

### 12.8 Publier une image dans un registre

Une fois l'image construite, on la **pousse** vers un registre pour la partager :

```bash
docker login                                          # se connecter à Docker Hub
docker build -t monuser/quickbite-api:1.0.0 .         # construire avec un tag
docker push monuser/quickbite-api:1.0.0               # publier l'image
```

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 2 : conteneuriser QuickBite</span>
1. Écrivez le <code>Dockerfile</code> (multi-stage) et le <code>.dockerignore</code> ; construisez l'image et testez l'endpoint <code>/health</code>.<br>
2. Ajoutez une base PostgreSQL via <code>docker-compose.yml</code> et reliez l'API au service <code>db</code>.<br>
3. Ajoutez un <b>volume</b> et vérifiez que les données survivent à un <code>down</code> puis <code>up</code>.<br>
4. Taguez et <b>poussez</b> l'image sur un registre.<br><br>
<b>Critère de réussite :</b> l'image finale doit faire moins de 200 Mo (grâce au multi-stage), et <code>docker compose up</code> doit démarrer l'API et la base sans erreur.
</div>

---

## Chapitre 13 — Kubernetes, l'orchestration

### 13.1 Pourquoi a-t-on besoin de Kubernetes ?

Docker lance des conteneurs **sur une seule machine**. C'est parfait en développement. Mais en **production**, on veut bien plus :

- Faire tourner l'application sur **plusieurs machines** pour résister aux pannes.
- **Redémarrer automatiquement** un conteneur qui plante.
- **Augmenter ou diminuer** le nombre de copies selon la charge (la « mise à l'échelle »).
- Déployer de nouvelles versions **sans interruption de service**.
- **Répartir la charge** entre les copies.

Faire tout cela à la main est impossible. **Kubernetes** (souvent abrégé **K8s**) est l'**orchestrateur** qui automatise tout cela. C'est devenu le standard de l'industrie.

### 13.2 L'architecture en deux mots

```
┌──────────────── Control Plane (le cerveau) ────────────────┐
│   API Server  │  Scheduler  │  Controllers  │  etcd        │
└───────────────────────┬────────────────────────────────────┘
                        │ (on parle à l'API Server via "kubectl")
        ┌───────────────┼───────────────┐
     ┌──┴───┐        ┌──┴───┐        ┌──┴───┐
     │ Node │        │ Node │        │ Node │     (les "workers"
     │ Pods │        │ Pods │        │ Pods │      qui exécutent
     └──────┘        └──────┘        └──────┘      les conteneurs)
```

Le **Control Plane** est le cerveau qui prend les décisions ; les **Nodes** (nœuds) sont les machines qui exécutent réellement les conteneurs. On communique avec le cluster via l'outil en ligne de commande **`kubectl`**.

### 13.3 Les objets fondamentaux

| Objet | Son rôle |
|-------|----------|
| **Pod** | La plus petite unité déployable : un (ou plusieurs) conteneur(s) qui partagent un réseau et un stockage |
| **ReplicaSet** | Garantit qu'un nombre *N* de copies d'un Pod tourne en permanence |
| **Deployment** | Gère les ReplicaSet : il pilote les mises à jour progressives et les retours en arrière |
| **Service** | Fournit une adresse réseau **stable** et répartit le trafic entre les Pods |
| **Ingress** | Gère l'accès HTTP(S) **depuis l'extérieur** (noms de domaine, chemins d'URL) |

Une nuance importante : les Pods sont **éphémères** (ils naissent et meurent, leur adresse IP change). Le **Service** existe précisément pour fournir un point d'entrée **fixe** vers ces Pods changeants.

### 13.4 Un Deployment commenté

On décrit les objets dans des fichiers YAML appelés **manifestes**. Voici un Deployment :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quickbite-api
spec:
  replicas: 3                       # je veux 3 copies de mon application
  selector:
    matchLabels: { app: quickbite-api }
  template:                         # le modèle de Pod à créer
    metadata:
      labels: { app: quickbite-api }
    spec:
      containers:
        - name: api
          image: ghcr.io/monuser/quickbite-api:1.0.0
          ports:
            - containerPort: 3000
          readinessProbe:           # comment K8s sait que le Pod est prêt
            httpGet: { path: /health, port: 3000 }
            initialDelaySeconds: 5
          resources:                # les ressources allouées
            requests: { cpu: "100m", memory: "128Mi" }
            limits:   { cpu: "500m", memory: "256Mi" }
```

La `readinessProbe` est essentielle : elle dit à Kubernetes comment vérifier que le Pod est **prêt à recevoir du trafic** (ici, en appelant `/health`). Tant que la sonde échoue, Kubernetes n'envoie aucune requête à ce Pod. C'est ce qui permet les déploiements **sans coupure**.

### 13.5 Le Service et l'Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: quickbite-api
spec:
  selector: { app: quickbite-api }  # cible les Pods portant ce label
  ports:
    - port: 80
      targetPort: 3000              # redirige le port 80 vers le 3000 des Pods
  type: ClusterIP                   # accessible uniquement dans le cluster
```

L'**Ingress** ajoute l'accès externe par nom de domaine :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quickbite-ingress
spec:
  rules:
    - host: quickbite.local         # le nom de domaine
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: quickbite-api
                port: { number: 80 }
```

### 13.6 Les commandes kubectl à connaître

```bash
kubectl apply -f deployment.yaml      # crée ou met à jour depuis un manifeste
kubectl get pods,svc,deploy           # liste les objets
kubectl describe pod <nom>            # détails et événements (l'outil de debug n°1)
kubectl logs -f <pod>                 # affiche et suit les logs
kubectl scale deploy/quickbite-api --replicas=5   # passe à 5 copies
kubectl rollout undo deploy/quickbite-api         # revient à la version précédente
```

<div class="callout note"><span class="title">📘 Le déclaratif : la grande idée de Kubernetes</span>
On ne dit pas à Kubernetes <i>« lance ce conteneur »</i> (impératif). On lui décrit l'<b>état souhaité</b> : <i>« je veux 3 copies de cette application en permanence »</i> (déclaratif). Kubernetes compare en continu cet état souhaité à l'état réel, et <b>agit pour les faire correspondre</b>. Si un Pod meurt, il en recrée un, automatiquement, sans qu'on intervienne. C'est ce qu'on appelle l'<b>auto-réparation</b>, et c'est aussi le fondement du GitOps qu'on verra au chapitre 14.
</div>

### 13.7 Configuration et secrets

On ne met pas la configuration « en dur » dans l'image (sinon il faudrait reconstruire l'image à chaque changement de paramètre). On utilise des **ConfigMaps** (pour la configuration ordinaire) et des **Secrets** (pour les données sensibles) :

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: quickbite-config }
data:
  APP_MODE: "production"
  PAGE_SIZE: "20"
---
apiVersion: v1
kind: Secret
metadata: { name: quickbite-secret }
type: Opaque
stringData:
  DATABASE_PASSWORD: "secret-a-changer"
```

<div class="callout warn"><span class="title">⚠️ Un Secret Kubernetes est encodé, pas chiffré</span>
Attention à un piège classique : par défaut, un Secret est seulement encodé en base64 — ce qui se décode en une seconde. Ce n'est <b>pas</b> du chiffrement. Pour une vraie protection, il faut activer le chiffrement « au repos » du stockage de Kubernetes (etcd), ou utiliser un gestionnaire externe (Vault, Sealed Secrets). Et bien sûr, ne committez <b>jamais</b> un Secret en clair dans Git.
</div>

Les **Namespaces** (espaces de noms) cloisonnent les ressources, par exemple pour séparer `dev`, `staging` et `prod` dans un même cluster.

### 13.8 Un mot sur la sécurité (RBAC)

Le **RBAC** (*Role-Based Access Control*, contrôle d'accès basé sur les rôles) définit **qui** a le droit de faire **quoi** dans le cluster. On crée des `Role` (un ensemble de permissions) qu'on associe à des utilisateurs via des `RoleBinding`. Le principe directeur est celui du **moindre privilège** : chacun ne reçoit que les droits strictement nécessaires à son travail.

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 3 : déployer sur un cluster local</span>
Avec <b>Minikube</b> ou <b>K3s</b> :<br>
1. Démarrez le cluster (<code>minikube start</code>) et activez l'Ingress.<br>
2. Appliquez le Deployment et le Service ; vérifiez que 3 Pods sont « Running ».<br>
3. Ajoutez une ConfigMap et un Secret, et injectez-les dans l'application.<br>
4. Exposez l'application via l'Ingress et testez-la dans le navigateur.<br>
5. Passez à 5 réplicas avec <code>kubectl scale</code>, puis déployez une <b>mauvaise</b> image et faites un <code>rollout undo</code> pour revenir en arrière.<br><br>
<b>Réflexe de debug à acquérir :</b> en cas de souci, votre premier geste est toujours <code>kubectl describe pod &lt;nom&gt;</code> et de lire la section « Events » en bas.
</div>

---

## Chapitre 14 — La chaîne complète : Helm, observabilité, GitOps

### 14.1 Assembler une chaîne CI/CD de bout en bout

L'objectif final est qu'à chaque nouvelle version (par exemple un tag Git), le pipeline **construise l'image, la pousse dans le registre, et la déploie** automatiquement sur Kubernetes :

```yaml
name: CI-CD
on:
  push:
    tags: [ 'v*' ]                  # se déclenche sur un tag commençant par v
jobs:
  build-push:
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
  deploy:
    needs: build-push               # ne s'exécute qu'après le build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          kubectl set image deploy/quickbite-api \
            api=ghcr.io/${{ github.repository }}:${{ github.ref_name }} \
            --namespace=prod
```

### 14.2 Helm : le gestionnaire de paquets de Kubernetes

Quand on a plusieurs environnements (dev, staging, prod), on se retrouve à dupliquer des manifestes YAML quasi identiques, qui ne diffèrent que par quelques valeurs. C'est lourd et source d'erreurs. **Helm** résout cela en **transformant les manifestes en modèles paramétrables** (des *templates*).

Un *chart* Helm est un dossier structuré :

```
quickbite-chart/
├── Chart.yaml          # les métadonnées du chart
├── values.yaml         # les valeurs par défaut (paramètres)
└── templates/
    ├── deployment.yaml # un manifeste avec des {{ .Values.* }}
    ├── service.yaml
    └── ingress.yaml
```

Le fichier `values.yaml` centralise les paramètres :

```yaml
replicaCount: 3
image:
  repository: ghcr.io/monuser/quickbite-api
  tag: "1.0.0"
service:
  port: 80
```

Et le template y fait référence avec une syntaxe `{{ .Values.xxx }}` :

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: api
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

On peut alors déployer le même chart avec des valeurs différentes par environnement :

```bash
helm install quickbite ./quickbite-chart -n prod
helm upgrade quickbite ./quickbite-chart --set image.tag=1.1.0 -n prod
helm rollback quickbite 1 -n prod    # revenir à la version 1
```

### 14.3 L'observabilité : voir ce qui se passe en production

Une fois en production, comment sait-on que tout va bien ? Grâce à l'**observabilité**, qui repose sur trois piliers :

- Les **logs** (journaux) : *que s'est-il passé ?*
- Les **métriques** : *combien, et à quelle vitesse ?* (nombre de requêtes, temps de réponse…)
- Les **traces** : *quel chemin une requête a-t-elle suivi à travers les différents services ?*

Le duo le plus répandu pour les métriques est **Prometheus** (qui collecte et stocke les métriques) et **Grafana** (qui les affiche sous forme de tableaux de bord) :

```
Application (/metrics) ──collecte──► Prometheus ──affichage──► Grafana (dashboards)
                                          │
                                          └──► Alertmanager ──► email / Slack
```

<div class="callout tip"><span class="title">💡 Les quatre signaux dorés</span>
Par où commencer quand on supervise un service ? Les ingénieurs de fiabilité de Google recommandent de surveiller en priorité quatre indicateurs, les « <b>signaux dorés</b> » : la <b>latence</b> (temps de réponse), le <b>trafic</b> (nombre de requêtes), les <b>erreurs</b> (taux d'échec) et la <b>saturation</b> (à quel point les ressources sont remplies). Un tableau de bord qui couvre ces quatre signaux détecte la grande majorité des problèmes.
</div>

### 14.4 Le GitOps avec Argo CD

Le **GitOps** est l'aboutissement de la logique déclarative de Kubernetes. L'idée : l'**état souhaité du système vit entièrement dans Git**, qui devient la **source unique de vérité**. Un agent installé dans le cluster — par exemple **Argo CD** — compare en permanence ce qui est décrit dans Git avec ce qui tourne réellement, et **synchronise** automatiquement.

```
Développeur ─► commit / Pull Request ─► Dépôt Git (manifestes, charts Helm)
                                              │
                                      Argo CD surveille en continu
                                              ▼
                                   Cluster Kubernetes (se met à jour pour
                                   correspondre à ce qui est décrit dans Git)
```

Les avantages sont considérables : tout changement passe par Git, donc tout est **tracé et auditable** ; un retour en arrière se fait par un simple `git revert` ; et il n'y a plus de `kubectl apply` manuel et risqué en production. **Git devient le tableau de bord et le bouton de déploiement.**

<div class="callout lab"><span class="title">🧪 Exercice — Atelier final : du commit à la production</span>
Assemblez toute la chaîne du module : (1) un pipeline qui <b>teste</b> puis <b>construit et pousse</b> l'image ; (2) un <b>chart Helm</b> paramétré ; (3) un <b>déploiement</b> sur le cluster local exposé par Ingress ; (4) un tableau de bord <b>Grafana</b> affichant au moins un signal doré ; (5) en bonus, l'application placée sous <b>Argo CD</b> pour qu'un commit déclenche le déploiement.<br><br>
<b>Démonstration finale :</b> racontez, en partant d'une modification de code, tout le trajet « du commit à la production ». C'est la synthèse de tout le module.
</div>

### 14.5 Récapitulatif du Module 2

Retenez la chaîne logique : **Git** stocke le code, la **CI** le teste à chaque changement, **Docker** l'empaquète de façon portable, un **registre** le distribue, **Kubernetes** l'exécute de façon résiliente et scalable, **Helm** paramètre les déploiements, **l'observabilité** surveille le tout, et le **GitOps** boucle la boucle en pilotant la production depuis Git. Le but de toute cette mécanique n'est pas la technique pour la technique : c'est de **livrer la valeur agile du Module 1 plus vite et plus sûrement**.

Dans le Module 3, nous nous attaquons à une exigence non négociable de tout produit livré : sa **sécurité**.
