# Introduction : pourquoi Kubernetes ?

## 1. Le problème : faire tourner des conteneurs « en vrai »

Avec Docker, on sait lancer un conteneur nginx :

```bash
docker run -d -p 80:80 nginx
```

Parfait sur **une** machine, pour **un** conteneur. Mais en production, on veut :

- **Plusieurs copies** (réplicas) pour tenir la charge.
- Qu'une copie **redémarre toute seule** si elle plante.
- **Répartir** ces copies sur plusieurs serveurs.
- Mettre à jour la version **sans coupure**.
- Une **adresse stable** alors que les conteneurs vont et viennent.
- Gérer **config, secrets, stockage, réseau**…

Faire tout cela à la main avec `docker run`, c'est ingérable. Il faut un **orchestrateur**.

## 2. La solution : Kubernetes (K8s)

> **Kubernetes** est le système open source qui **orchestre** des conteneurs sur un
> ensemble de machines : il les déploie, les réplique, les surveille, les répare, les
> met à jour et les expose au réseau — **automatiquement**.

Le mot vient du grec *kubernêtês* (« timonier »). On l'abrège **K8s** (k + 8 lettres + s).

### L'idée centrale : le modèle déclaratif

Avec Docker, on donne des **ordres** (« lance ce conteneur »). Avec Kubernetes, on décrit
un **état désiré** (« je veux **3** nginx en permanence ») dans un fichier YAML. Kubernetes
travaille **en boucle** pour que l'état réel corresponde toujours à l'état désiré.

| Approche impérative (Docker) | Approche déclarative (Kubernetes) |
|------------------------------|-----------------------------------|
| « Lance un conteneur » | « Je veux qu'il y ait 3 nginx » |
| Si ça plante, c'est fini | Si ça plante, K8s le recrée |
| Vous gérez chaque étape | Vous décrivez la cible, K8s s'en charge |

C'est la notion de **réconciliation** : un Pod meurt ? Kubernetes en relance un. Vous
demandez 5 réplicas au lieu de 3 ? Il en crée 2 de plus. **Vous décrivez, il exécute.**

## 3. Notre fil rouge : nginx

Tout au long de ce cours, **un seul exemple** sert à illustrer chaque concept : l'image
**`nginx`** (un serveur web léger, public, qui démarre en une seconde). C'est l'idéal pour
apprendre : on se concentre sur **Kubernetes**, pas sur l'application.

À la fin, vous saurez déployer nginx :

- en **plusieurs réplicas** auto-réparés (Pods, Deployment) ;
- avec une **adresse stable** et un accès externe (Service, Ingress) ;
- **configuré** sans rebuild (ConfigMap, Secret) ;
- avec du **stockage persistant** (PV, PVC) ;
- mis à jour **sans coupure** (rolling update) et avec **rollback**.

## 4. Le vocabulaire en une page

| Objet | Rôle (avec nginx) |
|-------|-------------------|
| **Pod** | La plus petite unité : enveloppe le conteneur nginx |
| **ReplicaSet** | Maintient N copies identiques du Pod nginx |
| **Deployment** | Gère les ReplicaSets : mises à jour, rollback, scaling |
| **Service** | Adresse réseau stable devant les Pods nginx |
| **Ingress** | Routeur HTTP/HTTPS à l'entrée du cluster |
| **ConfigMap / Secret** | Configuration et données sensibles de nginx |
| **PV / PVC** | Stockage persistant monté dans le Pod |
| **Namespace** | Cloison logique pour organiser les objets |

## 5. Comment essayer Kubernetes

Pas besoin d'un cloud pour apprendre : un cluster local suffit.

| Outil | Pour |
|-------|------|
| **minikube** | Cluster local à un node, simple |
| **kind** | Kubernetes « in Docker », rapide pour tester |
| **k3s** | Distribution légère, idéale petits serveurs |
| **Docker Desktop** | Active Kubernetes en une case à cocher |

```bash
# Exemple avec minikube
minikube start
kubectl get nodes      # le cluster répond ?
```

`kubectl` (prononcé « cube-cti-el ») est l'outil en ligne de commande pour **parler au
cluster**. On l'utilisera dans tout le cours.

> **Pré-requis :** connaître Docker (images, conteneurs, ports) — voir le cours
> *« Dockeriser ses applications »*. Aucune connaissance préalable de Kubernetes n'est requise.
