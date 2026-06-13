# Charts, Releases & Repositories

Avant de manipuler Helm, posons précisément les trois concepts qui structurent tout :
le **Chart**, la **Release** et le **Repository**.

## 1. Le Chart : le paquet

Un **chart** est un dossier (ou une archive `.tgz`) qui contient **tout le nécessaire**
pour déployer une application :

- des **modèles** de manifestes Kubernetes (`templates/`) ;
- des **valeurs par défaut** configurables (`values.yaml`) ;
- des **métadonnées** (`Chart.yaml` : nom, version, description) ;
- éventuellement des **dépendances** (sous-charts).

> Un chart est **inerte** : c'est une recette. Tant qu'on ne l'installe pas, rien ne tourne.
> On peut le partager, le versionner, le publier sur un repository.

## 2. La Release : l'instance installée

Quand on **installe** un chart, Helm crée une **release** : une instance nommée et
**versionnée** de ce chart dans le cluster.

```bash
helm install nginx-prod ./nginx        # release "nginx-prod" à partir du chart ./nginx
helm install nginx-dev  ./nginx --set replicaCount=1   # autre release, autres valeurs
```

Points clés :

- Un **même chart** → **plusieurs releases** (dev, prod, par client…), chacune isolée.
- Chaque release a un **historique de révisions** : install = révision 1, chaque upgrade
  incrémente. C'est ce qui permet le **rollback**.
- Helm stocke l'état de chaque release dans le cluster (dans des Secrets du namespace).

```bash
helm list                  # lister les releases installées
helm status nginx-prod     # état détaillé d'une release
helm history nginx-prod    # toutes les révisions
```

## 3. Le Repository : le dépôt de charts

Un **repository** est un serveur HTTP qui héberge des charts packagés, avec un `index.yaml`
qui les catalogue. C'est l'équivalent d'un registre de paquets.

```bash
# Ajouter un repository public
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Chercher et installer un chart tout prêt
helm search repo nginx
helm install mon-nginx bitnami/nginx
```

> On n'écrit pas toujours ses charts : pour des briques standard (nginx, PostgreSQL, Redis,
> Prometheus…), on **réutilise** des charts publics éprouvés, en surchargeant juste les
> valeurs qui nous intéressent.

## 4. Le schéma mental complet

```
Repository  ──(helm pull / install)──►  Chart  ──(helm install + values)──►  Release  ──►  Objets K8s
 (catalogue)                          (la recette)                       (l'instance)    (Pods, Service…)
```

| Question | Réponse |
|----------|---------|
| « Où je trouve des charts ? » | dans un **Repository** |
| « Qu'est-ce que je télécharge ? » | un **Chart** |
| « Qu'est-ce qui tourne dans le cluster ? » | une **Release** (instance du chart) |
| « Comment je change la config ? » | les **values** passées à l'install |

## 5. Helm vs kubectl vs Kustomize

| Outil | Rôle | Quand |
|-------|------|-------|
| **kubectl** | applique des manifestes bruts | objets simples, apprentissage |
| **Kustomize** | superpose des patches sur des YAML de base | variations légères, intégré à kubectl |
| **Helm** | **package** + **templatise** + **versionne** + **cycle de vie** | applications réutilisables, multi-environnements, écosystème de charts |

> **Helm et Kustomize ne s'excluent pas.** Helm brille pour packager/distribuer et pour le
> cycle de vie (upgrade/rollback) ; Kustomize pour de simples surcharges. Beaucoup
> d'équipes utilisent Helm pour les briques tierces et Kustomize pour leurs ajustements.

## 6. Les commandes à connaître dès maintenant

```bash
helm create <nom>           # créer un chart squelette
helm lint <chart>           # vérifier la validité du chart
helm template <chart>       # rendre les manifestes SANS installer (debug)
helm install <release> <chart>     # installer
helm upgrade <release> <chart>     # mettre à jour
helm rollback <release> <rev>      # revenir à une révision
helm uninstall <release>           # désinstaller (supprime tous les objets)
helm list / helm history <release> # observer
```

Dans le module suivant, on ouvre un chart et on examine **chaque fichier**.
