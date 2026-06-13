# Bonnes pratiques, débogage & checklist

Un bon chart est **lisible, testable et sûr**. Voici les pratiques qui font la différence,
les commandes de débogage et une checklist finale.

## 1. Tester avant d'appliquer

**Ne jamais** installer un chart sans l'avoir validé. Trois filets de sécurité :

```bash
helm lint ./nginx                         # 1) structure et erreurs de syntaxe
helm template nginx-prod ./nginx          # 2) voir le YAML rendu (valeurs remplacées)
helm install nginx-prod ./nginx --dry-run --debug   # 3) simulation complète
```

| Commande | Vérifie |
|----------|---------|
| `helm lint` | la **validité** du chart (champs requis, conventions) |
| `helm template` | le **rendu** final des manifestes |
| `--dry-run --debug` | la **simulation** contre le cluster (sans rien créer) |

## 2. Bien gérer les valeurs

- **Documenter** chaque valeur dans `values.yaml` avec un commentaire.
- Fournir des **défauts sensés** : le chart doit s'installer sans surcharge.
- Un fichier de valeurs **par environnement** : `values-dev.yaml`, `values-prod.yaml`.
- Préférer `-f values-prod.yaml` à de longues rafales de `--set` (versionnable, relisible).

```bash
helm upgrade --install nginx-prod ./nginx -f values-prod.yaml
```

## 3. Versionner correctement (SemVer)

- Incrémenter `version` (du chart) **à chaque modification** du chart.
- Mettre à jour `appVersion` quand l'application embarquée change.
- Suivre le **versionnement sémantique** : `MAJEUR.MINEUR.CORRECTIF`.

| Changement | Incrémenter |
|------------|-------------|
| Correction sans impact | CORRECTIF (1.0.**1**) |
| Nouvelle option rétro-compatible | MINEUR (1.**1**.0) |
| Changement cassant (valeurs renommées…) | MAJEUR (**2**.0.0) |

## 4. Sécurité

- **Ne jamais** committer de secrets en clair dans `values.yaml`. Utiliser des **Secrets**
  Kubernetes, ou des outils comme **helm-secrets** / **Sealed Secrets** / un coffre externe.
- Définir **requests/limits** par défaut dans le chart.
- Épingler les **versions d'images** (`tag: "1.27"`), jamais `latest`.
- Fixer les **versions des dépendances** et committer `Chart.lock`.

## 5. Lisibilité des templates

- Factoriser le nommage et les labels dans `_helpers.tpl` (`{{ include "nginx.labels" . }}`).
- Utiliser `{{- ` et ` -}}` pour **maîtriser les espaces** et les lignes vides.
- Garder une indentation cohérente (`| nindent 4`).
- Rendre les fonctionnalités **optionnelles** avec `if` + une valeur `enabled`.

```yaml
metadata:
  labels:
    {{- include "nginx.labels" . | nindent 4 }}
```

## 6. Débogage : les pannes courantes

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| `helm install` échoue sur le YAML | erreur de template / indentation | `helm template` pour voir le rendu |
| Valeur non prise en compte | mauvais chemin dans `.Values` | `helm get values <release>` |
| `another operation in progress` | release bloquée en `pending` | `helm rollback` ou `--force` |
| Upgrade casse tout | changement non rétro-compatible | `helm rollback`, ou installer avec `--atomic` |
| Sous-chart absent | `charts/` non rempli | `helm dependency update` |
| Espaces/lignes en trop | gestion des whitespaces | utiliser `{{-` et `-}}` |

```bash
helm template ./nginx | kubectl apply --dry-run=client -f -   # double validation
helm get manifest <release>                                   # ce qui est réellement déployé
```

## 7. Helm en CI/CD

Le combo gagnant pour un pipeline (à enchaîner après le build d'image) :

```bash
helm lint ./nginx
helm upgrade --install nginx-prod ./nginx \
  -f values-prod.yaml \
  --set image.tag=$GIT_SHA \
  --atomic --wait --timeout 5m
```

- `--install` rend la commande **idempotente**.
- `--set image.tag=$GIT_SHA` déploie **exactement** l'image qu'on vient de construire.
- `--atomic --wait` : déploiement « tout ou rien », rollback auto si échec.

## 8. Checklist d'un chart de qualité

- [ ] `helm lint` passe sans erreur.
- [ ] `helm template` produit un YAML correct (vérifié visuellement).
- [ ] Toutes les valeurs sont **documentées** dans `values.yaml` avec des défauts sensés.
- [ ] Un fichier de valeurs **par environnement**.
- [ ] **requests/limits** définies ; images **taguées** précisément.
- [ ] **Aucun secret** en clair dans le chart.
- [ ] `version` / `appVersion` à jour ; dépendances figées (`Chart.lock`).
- [ ] Labels et nommage factorisés via `_helpers.tpl`.
- [ ] Déploiement testé avec `--dry-run`, puis `--atomic --wait` en réel.

---

## Conclusion

Avec un seul chart — celui de **nginx** — vous avez parcouru tout Helm : les **charts**, les
**releases** versionnées, le **templating** (`{{ .Values }}`, `if`, `range`, fonctions), le
cycle de vie (**install / upgrade / rollback**), les **dépendances** et les
**repositories**, jusqu'aux bonnes pratiques de production.

Helm transforme des piles de YAML en **applications packagées, paramétrables et
versionnées**. Combiné à un pipeline CI/CD et à GitOps, c'est la base d'un déploiement
Kubernetes professionnel.

> **Pour aller plus loin :** les **library charts** (mutualiser du template entre charts),
> **helmfile** (orchestrer plusieurs releases), les **tests de chart** (`helm test`), et
> l'intégration de Helm dans **Argo CD** pour le GitOps.
