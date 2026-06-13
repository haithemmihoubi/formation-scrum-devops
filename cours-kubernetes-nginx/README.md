# Cours : Apprendre Kubernetes avec nginx

Support de formation DevOps **avec illustrations** qui enseigne **tous les concepts
essentiels de Kubernetes** à travers un seul exemple fil rouge : l'image **nginx**.
L'apprenant se concentre sur Kubernetes, pas sur l'application.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : pourquoi Kubernetes ? (modèle déclaratif) |
| 01 | Architecture d'un cluster (Control Plane & Worker Nodes) |
| 02 | Les Pods (la plus petite unité) |
| 03 | Deployments & ReplicaSets (résilience, scaling, self-healing) |
| 04 | Mises à jour sans coupure & rollback (rolling update) |
| 05 | Services (ClusterIP, NodePort, LoadBalancer, labels/selector, DNS) |
| 06 | ConfigMap & Secret (configurer nginx sans rebuild) |
| 07 | Stockage persistant (PV, PVC, StorageClass, StatefulSet) |
| 08 | Ingress (routeur HTTP/HTTPS, TLS) |
| 09 | Pratique : namespaces, probes, ressources, TP complet & checklist |

## Illustrations

Huit diagrammes vectoriels (SVG) générés par script expliquent visuellement chaque
concept : architecture du cluster, anatomie d'un Pod, hiérarchie Deployment→ReplicaSet→Pods,
rolling update étape par étape, types de Services, ConfigMap/Secret, stockage PVC/PV/SC et
routage Ingress.

## Générer le PDF

Pré-requis (déjà présents sur la machine de formation) :

```bash
pip install markdown weasyprint
```

Puis :

```bash
python3 build_pdf.py
# → régénère les illustrations puis Cours-Kubernetes-nginx.pdf (38 pages, A4)
```

`build_pdf.py` appelle automatiquement `make_illustrations.py` avant l'assemblage.
On peut aussi (re)générer les SVG seuls :

```bash
python3 make_illustrations.py   # → dossier img/
```

Chaque module est un fichier `.md` autonome : on peut les éditer puis relancer
`build_pdf.py` pour régénérer le PDF.
