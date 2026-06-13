# Secrets, bonnes pratiques & checklist

Le GitOps soulève une question évidente : **comment gérer les secrets** si tout est dans
Git ? Plus les pratiques qui font un GitOps sain, et une checklist finale.

## 1. Le défi des secrets en GitOps

On ne peut **jamais** committer un mot de passe ou une clé **en clair** dans Git : le dépôt
est historisé, cloné, parfois public. Or le GitOps veut **tout** dans Git. Solution :
committer les secrets **chiffrés**.

| Approche | Principe |
|----------|----------|
| **Sealed Secrets** (Bitnami) | on committe un secret **chiffré** ; un contrôleur le déchiffre **dans** le cluster |
| **SOPS** (+ age/KMS) | chiffre les valeurs dans le YAML ; déchiffré au déploiement |
| **External Secrets Operator** | le secret reste dans un **coffre** externe (Vault, AWS/GCP) ; l'opérateur le **synchronise** |

### Exemple : Sealed Secrets

```bash
# Chiffrer un secret classique en "SealedSecret" (sûr à committer)
kubeseal -f secret.yaml -w sealed-secret.yaml
git add sealed-secret.yaml && git commit -m "secret nginx-tls (chiffré)"
# → dans le cluster, le controller le déchiffre en vrai Secret
```

> **La règle :** ce qui est dans Git doit être **chiffré** ou n'être qu'une **référence**
> vers un coffre. Jamais de secret en clair, même dans un dépôt privé.

## 2. Sécuriser Argo CD

- **RBAC + Projects** : limiter chaque application aux dépôts, clusters et namespaces
  autorisés (principe du moindre privilège).
- **SSO** : connecter Argo CD au fournisseur d'identité de l'entreprise (OIDC, GitHub).
- **Désactiver l'admin** local une fois le SSO en place.
- **Protéger la branche** déployée (`main`) : Pull Requests obligatoires, revue, statut CI.
- **Signer les commits** pour garantir l'origine des changements.

## 3. Organisation et qualité

- **Deux dépôts** : code applicatif d'un côté, configuration GitOps de l'autre.
- **Base + overlays** (ou chart + values) : zéro duplication entre environnements.
- **App of Apps / ApplicationSet** : ne pas créer les Applications à la main.
- **Tag d'image figé en prod** (jamais `latest`) : déploiements déterministes et rollback fiable.
- **Sync manuelle en prod**, automatique en dev/staging.

## 4. Fiabilité du déploiement

- **`selfHeal`** pour empêcher toute dérive (sauf raison précise de l'éviter).
- **`prune`** pour que la suppression dans Git supprime réellement dans le cluster.
- **Hooks `PreSync`** pour les migrations de base de données.
- **Webhook Git** pour des synchros quasi instantanées.
- **Notifications** (Slack, e-mail) sur les échecs de synchro (`argocd-notifications`).

## 5. CI et GitOps : qui fait quoi

Frontière nette entre **intégration** (CI) et **déploiement** (GitOps) :

| Étape | Outil | Action |
|-------|-------|--------|
| 1. Build & test | **GitHub Actions** | construit l'image, la pousse sur le registry |
| 2. Mise à jour de config | **GitHub Actions** | met à jour le **tag d'image** dans le dépôt GitOps (commit/PR) |
| 3. Déploiement | **Argo CD** | détecte le commit et **synchronise** le cluster |

```yaml
# Étape 2 dans un workflow CI : bump du tag, puis push (déclenche Argo CD)
- name: Mettre à jour le tag d'image dans le dépôt GitOps
  run: |
    yq -i '.image.tag = "${{ github.sha }}"' apps/nginx/overlays/prod/values.yaml
    git commit -am "nginx → ${{ github.sha }}" && git push
```

> **Le pipeline n'a plus accès au cluster.** Il s'arrête à Git ; Argo CD prend le relais.
> C'est plus simple **et** plus sûr.

## 6. Dépannage : pannes courantes

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Reste `OutOfSync` | sync auto désactivée, ou erreur de manifeste | `argocd app sync`, lire le diff |
| `Degraded` | un Pod plante | `kubectl logs`, `argocd app get` |
| Dérive qui revient sans cesse | un autre outil modifie le cluster | identifier l'acteur, ou désactiver `selfHeal` ciblé |
| Secret en clair commité | mauvaise pratique | **révoquer** le secret, passer à Sealed Secrets/SOPS |
| `ComparisonError` | dépôt inaccessible / mauvais `path` | vérifier `repoURL`, droits, chemin |
| Helm ne rend pas | mauvais `valueFiles` | vérifier le chemin des values dans la source |

## 7. Checklist d'un GitOps sain

- [ ] Git est la **source de vérité unique** ; aucun `kubectl apply` hors GitOps.
- [ ] Dépôt **applicatif** et dépôt **de config** séparés.
- [ ] **Aucun secret en clair** : Sealed Secrets / SOPS / External Secrets.
- [ ] **base + overlays** (ou chart + values) par environnement.
- [ ] **App of Apps** ou **ApplicationSet** pour la mise à l'échelle.
- [ ] `selfHeal` + `prune` activés (sauf exception justifiée).
- [ ] **Sync manuelle en prod**, automatique ailleurs ; tags d'image **figés** en prod.
- [ ] **RBAC/Projects** restrictifs ; **SSO** ; branche `main` protégée.
- [ ] **Webhook** Git pour des synchros rapides ; **notifications** sur échec.
- [ ] Rollback maîtrisé par **`git revert`**.

---

## Conclusion

Avec **nginx** comme fil rouge, vous avez mis en place un déploiement **GitOps** complet :
Git comme **source de vérité**, **Argo CD** comme agent de réconciliation, l'objet
**Application** comme lien Git→cluster, la **synchronisation** avec auto-réparation, une
structure **multi-environnements** (App of Apps / ApplicationSet), et une gestion **sûre**
des secrets.

Le déploiement n'est plus une action risquée : c'est un **commit revu en Pull Request**, que
le cluster reflète automatiquement et durablement. Combiné à la CI (GitHub Actions), à
l'orchestration (Kubernetes), au packaging (Helm) et au monitoring (Prometheus/Grafana),
le GitOps **boucle** une chaîne DevOps moderne et professionnelle.

> **Pour aller plus loin :** **Argo Rollouts** (canary & blue-green déclaratifs),
> **Argo Workflows** (pipelines dans le cluster), les **stratégies de promotion** multi-
> clusters, et la **policy as code** (OPA/Kyverno) pour valider les manifestes avant
> déploiement.
