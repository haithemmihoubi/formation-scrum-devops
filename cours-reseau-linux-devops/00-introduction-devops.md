# Module 00 — Introduction au DevOps

🎯 **Objectif** : comprendre ce qu'est le DevOps et pourquoi Linux et le réseau en sont les fondations.

## 1. Qu'est-ce que le DevOps ?

Le **DevOps** est une culture et un ensemble de pratiques qui rapprochent les équipes de **développement** (Dev) et d'**exploitation/opérations** (Ops). L'objectif est de livrer des logiciels **plus vite**, **plus souvent** et **plus fiablement**.

Avant le DevOps, on avait un « mur de confusion » :
- Les **Devs** écrivaient le code et le « jetaient par-dessus le mur ».
- Les **Ops** devaient le déployer et le maintenir, souvent sans contexte.

Le DevOps casse ce mur grâce à l'automatisation, la collaboration et le partage de responsabilités.

## 2. Les piliers du DevOps (modèle CALMS)

| Pilier | Signification |
|--------|---------------|
| **C**ulture | Collaboration, responsabilité partagée, pas de blâme |
| **A**utomation | Automatiser builds, tests, déploiements, infrastructure |
| **L**ean | Réduire le gaspillage, livrer de petites itérations |
| **M**easurement | Mesurer tout (perf, erreurs, temps de déploiement) |
| **S**haring | Partager connaissances, outils, retours d'expérience |

## 3. Le cycle de vie DevOps (l'infini ∞)

```
   PLAN → CODE → BUILD → TEST → RELEASE → DEPLOY → OPERATE → MONITOR → (retour à PLAN)
```

- **Plan** : Jira, backlog, user stories (lien avec Scrum)
- **Code** : Git, revue de code
- **Build** : Maven, Gradle, npm
- **Test** : tests unitaires, intégration
- **Release/Deploy** : CI/CD (GitLab CI, Jenkins, GitHub Actions)
- **Operate** : Kubernetes, Docker, serveurs Linux
- **Monitor** : Prometheus, Grafana, logs

## 4. Pourquoi Linux est incontournable en DevOps

- **~90 %** des serveurs en production tournent sous Linux.
- Docker, Kubernetes, la majorité des outils cloud sont nés sur Linux.
- Les serveurs web (Nginx, Apache), bases de données et CI/CD runners tournent sous Linux.
- Tout s'automatise en ligne de commande → maîtriser le shell est vital.

## 5. Pourquoi le réseau est incontournable en DevOps

Un DevOps passe son temps à connecter des choses :
- Une application qui parle à une base de données
- Un load balancer qui répartit le trafic
- Des conteneurs qui communiquent dans un cluster
- Des appels d'API entre microservices

Sans comprendre **IP, ports, DNS, TCP, HTTP, pare-feu**, impossible de diagnostiquer un « ça ne marche pas ».

## 6. Outils que vous croiserez

| Catégorie | Exemples |
|-----------|----------|
| OS | Ubuntu, Debian, CentOS, Rocky Linux, Alpine |
| Conteneurs | Docker, Podman, containerd |
| Orchestration | Kubernetes, Docker Swarm |
| CI/CD | Jenkins, GitLab CI, GitHub Actions |
| IaC | Terraform, Ansible |
| Monitoring | Prometheus, Grafana, ELK |
| Cloud | AWS, Azure, GCP |

## 7. Quiz de fin de module

1. Que signifie l'acronyme CALMS ?
2. Citez 3 raisons pour lesquelles un DevOps doit maîtriser Linux.
3. Dans le cycle DevOps, quelle phase suit le « Deploy » ?
4. Pourquoi parle-t-on de « mur de confusion » avant le DevOps ?

> ✅ Une fois ce module compris, passez au [Module 01 — Linux Fondamentaux](01-linux-fondamentaux.md).
