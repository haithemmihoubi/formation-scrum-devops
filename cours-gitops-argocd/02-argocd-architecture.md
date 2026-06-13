# Argo CD : installation & architecture

**Argo CD** est l'agent qui met en œuvre le GitOps sur Kubernetes. Il tourne **dans** le
cluster, surveille un dépôt Git et synchronise les manifestes.

## 1. Installer Argo CD

Argo CD s'installe… de façon déclarative, dans son propre namespace :

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Accéder à l'interface web :

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# → https://localhost:8080

# Mot de passe initial de l'admin
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

Et la CLI :

```bash
argocd login localhost:8080            # se connecter
argocd app list                        # lister les applications
```

## 2. Les composants d'Argo CD

Argo CD se compose de quelques services, chacun avec un rôle précis :

| Composant | Rôle |
|-----------|------|
| **API Server** | l'interface (UI web, CLI, API) ; gère l'authentification |
| **Repository Server** | clone les dépôts Git et **génère les manifestes** (Helm, Kustomize…) |
| **Application Controller** | le **cœur** : compare Git ↔ cluster et **réconcilie** |
| **Redis** | cache interne |
| **Dex** (optionnel) | intégration SSO (OIDC, LDAP…) |

> **L'Application Controller** est l'élément central : c'est lui qui exécute la boucle de
> réconciliation pour chaque application, en continu.

## 3. Ce qu'Argo CD sait déployer

Argo CD ne se limite pas aux YAML bruts. Le **Repository Server** sait **rendre** plusieurs
formats avant d'appliquer :

| Format | Argo CD… |
|--------|----------|
| **Manifestes K8s** | applique les YAML tels quels |
| **Helm** | exécute `helm template` (avec vos values) puis applique |
| **Kustomize** | exécute `kustomize build` puis applique |
| **Jsonnet / plugins** | via des générateurs personnalisés |

> Vous pouvez donc faire du GitOps **sur vos charts Helm** : Argo CD pointe le chart dans
> Git, applique vos `values`, et maintient la release synchronisée. Helm + GitOps se marient
> parfaitement.

## 4. L'interface graphique : le GitOps visuel

L'UI d'Argo CD est un de ses atouts. Pour chaque application, elle affiche :

- l'**arbre des ressources** (Application → Deployment → ReplicaSet → Pods…) ;
- l'état de **synchronisation** (`Synced` / `OutOfSync`) ;
- l'état de **santé** (`Healthy` / `Degraded` / `Progressing`) ;
- le **diff** exact entre Git et le cluster ;
- l'historique des syncs, avec **rollback** en un clic.

> C'est extrêmement pédagogique : on **voit** la dérive apparaître en orange, puis
> disparaître après la synchronisation. Le concept GitOps devient concret.

## 5. Multi-cluster : un Argo CD, plusieurs clusters

Argo CD peut gérer **plusieurs clusters** depuis une seule instance :

```bash
argocd cluster add mon-cluster-prod      # enregistrer un cluster cible
argocd cluster list
```

→ une instance centrale d'Argo CD déploie sur le cluster `dev`, `staging` **et** `prod`,
chacun étant une **destination** différente (voir le module suivant).

## 6. Sécurité et accès (RBAC)

Argo CD gère ses propres droits, distincts de ceux du cluster :

- **Projects** : regroupent des applications et **restreignent** ce qu'elles peuvent faire
  (quels dépôts, quels clusters, quels namespaces).
- **RBAC** : qui peut voir/synchroniser/supprimer quelles applications.
- **SSO** : connexion via le fournisseur d'identité de l'entreprise (OIDC, GitHub…).

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: quickbite
  namespace: argocd
spec:
  sourceRepos:
    - 'https://github.com/mon-orga/quickbite-config'   # dépôts autorisés
  destinations:
    - server: https://kubernetes.default.svc
      namespace: 'prod'                                 # namespaces autorisés
```

## 7. Vue d'ensemble

```
[ Dépôt Git ]  ──(clone)──►  [ Repository Server ]  ──(rend les manifests)──►
                                                                              │
[ UI / CLI ] ──► [ API Server ]      [ Application Controller ] ──(applique)──┘──► [ Cluster ]
                                       (compare & réconcilie en boucle)
```

> **À retenir :** Argo CD s'installe dans le cluster, son **Application Controller** exécute
> la boucle de réconciliation, le **Repository Server** rend les manifestes (YAML/Helm/
> Kustomize), et l'**UI** rend tout visible. Reste à lui dire **quoi** déployer : l'objet
> **Application**.
