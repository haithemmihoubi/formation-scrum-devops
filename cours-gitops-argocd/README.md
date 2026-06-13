# Cours : GitOps avec Argo CD

Support de formation DevOps **avec illustrations** qui enseigne le **GitOps** avec Argo CD :
Git comme source de vérité, déploiement déclaratif, synchronisation et rollback. Fil rouge :
**déployer nginx en GitOps**.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : qu'est-ce que le GitOps ? (push vs pull) |
| 01 | Les principes du GitOps (source de vérité, boucle de réconciliation) |
| 02 | Argo CD : installation & architecture |
| 03 | L'objet Application (source → destination → syncPolicy) |
| 04 | Synchronisation, auto-réparation (selfHeal) & rollback |
| 05 | Structurer le dépôt & gérer les environnements (App of Apps, ApplicationSet) |
| 06 | Secrets, bonnes pratiques & checklist |

## Illustrations

Cinq diagrammes vectoriels (SVG) : push (CI/CD) vs pull (GitOps), la boucle de
réconciliation, l'objet Application (Git→Cluster), les états de sync + auto-réparation, et
le motif App of Apps.

## Générer le PDF

```bash
pip install markdown weasyprint
python3 build_pdf.py        # régénère les illustrations puis Cours-GitOps-ArgoCD.pdf
```

`build_pdf.py` appelle automatiquement `make_illustrations.py`. Chaque module est un `.md`
autonome.
