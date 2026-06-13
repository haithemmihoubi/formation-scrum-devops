# Formation Agile · DevOps · Sécurité

Supports de formation complets — **Scrum/Kanban, Docker, Réseau & Linux, CI/CD GitHub
Actions, Kubernetes, Helm, Monitoring et GitOps** — avec slides, cours PDF illustrés et
ateliers pratiques autour du projet fil rouge **QuickBite**.

**Formateur : Haithem Mihoubi**

---

## 📚 Les cours PDF illustrés

Chaque cours est un dossier autonome : des modules Markdown + un générateur d'illustrations
SVG + un script `build_pdf.py` (WeasyPrint). On édite les `.md` et on régénère le PDF.

| Cours | Dossier | PDF | Thème |
|-------|---------|-----|-------|
| **Réseau & Linux pour le DevOps** | [cours-reseau-linux-devops/](cours-reseau-linux-devops/) | [PDF](cours-reseau-linux-devops/Cours-Reseau-Linux-DevOps.pdf) | Fondamentaux système & réseau |
| **Dockeriser ses applications** | [cours-docker-multistage/](cours-docker-multistage/) | [PDF](cours-docker-multistage/Cours-Docker-Multistage.pdf) | Multi-stage : Spring Boot, Angular, React, Python |
| **Déployer Angular avec GitHub Actions** | [cours-github-actions-angular/](cours-github-actions-angular/) | [PDF](cours-github-actions-angular/Cours-GitHub-Actions-Angular.pdf) | CI/CD complet build → image → SSH |
| **Apprendre Kubernetes avec nginx** | [cours-kubernetes-nginx/](cours-kubernetes-nginx/) | [PDF](cours-kubernetes-nginx/Cours-Kubernetes-nginx.pdf) | Pods, Deployments, Services, Ingress… |
| **Packager Kubernetes avec Helm** | [cours-helm-kubernetes/](cours-helm-kubernetes/) | [PDF](cours-helm-kubernetes/Cours-Helm-Kubernetes.pdf) | Charts, values, templates, releases |
| **Monitoring Prometheus & Grafana** | [cours-monitoring-prometheus-grafana/](cours-monitoring-prometheus-grafana/) | [PDF](cours-monitoring-prometheus-grafana/Cours-Monitoring-Prometheus-Grafana.pdf) | Métriques, PromQL, dashboards, alerting |
| **GitOps avec Argo CD** | [cours-gitops-argocd/](cours-gitops-argocd/) | [PDF](cours-gitops-argocd/Cours-GitOps-ArgoCD.pdf) | Git source de vérité, sync, rollback |

> Les quatre derniers cours (GitHub Actions, Kubernetes, Helm, Monitoring, GitOps) forment
> un **parcours DevOps cohérent** : on conteneurise, on déploie en CI/CD, on orchestre, on
> package, on observe, puis on automatise le tout depuis Git.

## 🎓 Cours détaillés & ateliers (dossier `cours/`)

| Document | Fichier |
|----------|---------|
| Module 1 — Agile, Scrum & Kanban | [PDF](cours/out/Module1-Agile-Scrum-Kanban.pdf) |
| Module 2 — DevOps, CI/CD, Docker & Kubernetes | [PDF](cours/out/Module2-DevOps-CICD-Docker-Kubernetes.pdf) |
| Module 3 — Spring Security | [PDF](cours/out/Module3-Spring-Security.pdf) |
| Keycloak & Spring Security | [PDF](cours/out/Cours-Keycloak-Spring-Security.pdf) |
| Ateliers — Projet QuickBite | [PDF](cours/out/Ateliers-Projet-QuickBite.pdf) |
| Cours complet — Agile, DevOps & Sécurité | [PDF](cours/out/Cours-Complet-Agile-DevOps-Securite.pdf) |

## 🖥️ Présentations (slides)

- [presentation/](presentation/) — slides Scrum (génération PPTX/images).
- [presentation-pdf/](presentation-pdf/) — slides au format PDF.
- [Programme détaillé.pdf](Programme%20détaillé.pdf) — programme de la formation.

## 🍔 Projet fil rouge : QuickBite

Application de démonstration utilisée dans les ateliers et les pipelines :

| Composant | Dossier |
|-----------|---------|
| Frontend Angular | [quickbite-frontend/](quickbite-frontend/) |
| Frontend Angular + Keycloak | [quickbite-frontend-keycloak/](quickbite-frontend-keycloak/) |
| Backend / Keycloak | [quickbite-keycloak/](quickbite-keycloak/) |
| Atelier complet | [atelier-quickbite/](atelier-quickbite/) |

Le pipeline CI/CD réel de ce projet se trouve dans
[.github/workflows/frontend-deploy.yml](.github/workflows/frontend-deploy.yml) (il sert
d'exemple concret au cours GitHub Actions).

---

## 🔧 Générer un cours PDF

Pré-requis (déjà installés sur la machine de formation) :

```bash
pip install markdown weasyprint
```

Puis, dans le dossier d'un cours :

```bash
python3 build_pdf.py          # régénère les illustrations puis le PDF
# (ou) python3 make_illustrations.py   # uniquement les SVG
```
