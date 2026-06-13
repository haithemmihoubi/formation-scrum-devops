# Introduction : CI/CD & GitHub Actions

## 1. Le problème : déployer « à la main »

Déployer une application Angular sur un serveur **manuellement** ressemble souvent à ça :

1. On compile localement (`ng build`).
2. On copie les fichiers via FTP ou `scp`.
3. On se connecte en SSH au serveur.
4. On redémarre Nginx… en croisant les doigts.

Cette approche est **lente, non reproductible et risquée** : un oubli d'étape, une
mauvaise version compilée, une variable d'environnement différente, et c'est la panne
en production. Surtout, **une seule personne** sait comment déployer.

## 2. La solution : l'intégration et le déploiement continus (CI/CD)

| Sigle | Signification | Ce que ça automatise |
|-------|---------------|----------------------|
| **CI** | *Continuous Integration* | À chaque commit : installer, **builder**, **tester** le code |
| **CD** | *Continuous Delivery / Deployment* | Packager (image Docker), **publier**, **déployer** automatiquement |

> **L'idée centrale :** chaque `git push` déclenche une chaîne d'étapes automatiques.
> Le code part du poste du développeur et arrive **tout seul** en production, testé et
> packagé de façon **identique à chaque fois**.

## 3. Pourquoi GitHub Actions ?

**GitHub Actions** est le moteur de CI/CD **intégré à GitHub**. Aucun serveur d'intégration
à installer (pas de Jenkins à maintenir) : tout se déclare dans un simple fichier YAML
versionné avec le code.

- **Intégré** : déclenché par les événements GitHub (push, pull request…).
- **Gratuit** pour les dépôts publics, généreux pour les privés.
- **Des milliers d'actions réutilisables** sur le Marketplace (`actions/checkout`,
  `docker/build-push-action`…).
- **Des runners gérés** : GitHub fournit des machines Ubuntu / Windows / macOS jetables.
- **Secrets intégrés** : clés SSH, tokens, mots de passe stockés de façon chiffrée.

## 4. La vue d'ensemble de notre pipeline

Dans ce cours, nous construisons le pipeline complet d'une application Angular réelle
(**QuickBite Frontend**) : du `git push` jusqu'au conteneur Docker qui tourne sur un serveur.

![Vue d'ensemble du pipeline CI/CD](img/01-overview.svg)

<p class="caption">Du commit au serveur : GitHub Actions enchaîne build, test, packaging et déploiement.</p>

Le trajet complet :

1. Le développeur fait `git push` sur la branche `main`.
2. GitHub déclenche le **workflow** (événement `push`).
3. Un **runner Ubuntu** compile Angular et construit une **image Docker**.
4. L'image est testée (smoke test HTTP 200) puis **publiée** sur le registry **GHCR**.
5. Le runner se connecte en **SSH** au serveur, qui **télécharge et lance** la nouvelle image.

## 5. Ce que vous saurez faire à la fin

- Lire et écrire un fichier de workflow `.github/workflows/*.yml`.
- Comprendre les notions de **workflow, job, step, runner, action, secret**.
- Préparer une image Docker Angular prête pour la production.
- Configurer un serveur (Docker + accès SSH) et les **secrets** GitHub.
- Écrire un pipeline **build → push → deploy** complet et sécurisé.
- Dépanner un workflow qui échoue.

> **Pré-requis :** des bases de Git/GitHub, de Docker (voir le cours *Dockeriser ses
> applications*) et un accès SSH à un serveur Linux.
