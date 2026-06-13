# Cours : Déployer une application Angular avec GitHub Actions

Support de formation DevOps **avec illustrations** couvrant la mise en place d'un pipeline
**CI/CD complet** : build Angular, image Docker, publication sur GHCR et **déploiement SSH**
automatique sur un serveur. Basé sur le workflow réel du projet **QuickBite Frontend**.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : CI/CD & GitHub Actions (vue d'ensemble) |
| 01 | Anatomie de GitHub Actions (workflow, job, step, runner, events) |
| 02 | Préparer l'application Angular (Dockerfile multi-stage + Nginx) |
| 03 | Préparer le serveur et les accès (Docker, utilisateur, clés SSH, secrets) |
| 04 | Le workflow CI/CD complet (build → push → deploy) |
| 05 | Le déploiement SSH sur le serveur |
| 06 | Secrets, registry GHCR & sécurité |
| 07 | Aller plus loin, dépannage & checklist |

## Illustrations

Six diagrammes vectoriels (SVG) générés par script expliquent visuellement GitHub Actions :
pipeline d'ensemble, anatomie d'un workflow, événements déclencheurs, flux des 3 jobs,
déploiement SSH et gestion des secrets.

## Générer le PDF

Pré-requis (déjà présents sur la machine de formation) :

```bash
pip install markdown weasyprint
```

Puis :

```bash
python3 build_pdf.py
# → régénère les illustrations puis Cours-GitHub-Actions-Angular.pdf (31 pages, A4)
```

`build_pdf.py` appelle automatiquement `make_illustrations.py` avant l'assemblage.
On peut aussi (re)générer les SVG seuls :

```bash
python3 make_illustrations.py   # → dossier img/
```

Chaque module est un fichier `.md` autonome : on peut les éditer puis relancer
`build_pdf.py` pour régénérer le PDF.
