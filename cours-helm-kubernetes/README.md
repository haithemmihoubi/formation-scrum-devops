# Cours : Packager Kubernetes avec Helm

Support de formation DevOps **avec illustrations** qui enseigne **Helm**, le gestionnaire
de paquets de Kubernetes, à travers un fil rouge unique : un **chart nginx**.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : pourquoi Helm ? (le problème des YAML répétitifs) |
| 01 | Charts, Releases & Repositories (les 3 concepts clés) |
| 02 | La structure d'un chart (Chart.yaml, values.yaml, templates/) |
| 03 | Templates & values (templating Go, if/range, fonctions) |
| 04 | Releases : install, upgrade, rollback, historique |
| 05 | Dépendances & repositories (sous-charts, OCI, Artifact Hub) |
| 06 | Bonnes pratiques, débogage & checklist |

## Illustrations

Cinq diagrammes vectoriels (SVG) : vue d'ensemble de Helm, arborescence d'un chart,
mécanisme de templating (values + modèle → manifeste), cycle de vie d'une release
(révisions + rollback) et dépendances/sous-charts.

## Générer le PDF

```bash
pip install markdown weasyprint
python3 build_pdf.py        # régénère les illustrations puis Cours-Helm-Kubernetes.pdf
```

`build_pdf.py` appelle automatiquement `make_illustrations.py`. Chaque module est un `.md`
autonome.
