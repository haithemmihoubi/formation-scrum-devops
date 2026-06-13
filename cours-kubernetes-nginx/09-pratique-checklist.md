# Pratique, santé & checklist

Ce dernier module rassemble les éléments qui rendent un déploiement **propre et fiable** :
namespaces, sondes de santé, limites de ressources, un TP complet et un aide-mémoire.

## 1. Les Namespaces : cloisonner le cluster

Un **namespace** est une cloison logique pour organiser les objets (par équipe, par
environnement…). Les noms doivent être uniques **dans** un namespace, pas entre eux.

```bash
kubectl create namespace dev
kubectl apply -f nginx-deployment.yaml -n dev   # déployer dans "dev"
kubectl get pods -n dev                         # lister dans "dev"
kubectl get pods -A                             # tous namespaces confondus
```

| Namespace | Contenu |
|-----------|---------|
| `default` | où atterrissent les objets sans namespace précisé |
| `kube-system` | les composants internes de Kubernetes |
| vos namespaces | `dev`, `staging`, `prod`, par équipe… |

## 2. Les sondes de santé (probes)

Kubernetes vérifie l'état des conteneurs avec des **sondes**. Sans elles, il croit un Pod
sain dès qu'il démarre — même si nginx n'est pas encore prêt.

| Sonde | Question | Si échec |
|-------|----------|----------|
| **liveness** | « le conteneur est-il vivant ? » | Kubernetes le **redémarre** |
| **readiness** | « peut-il recevoir du trafic ? » | il est **retiré** du Service |
| **startup** | « a-t-il fini de démarrer ? » | protège les démarrages lents |

```yaml
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
      livenessProbe:
        httpGet: { path: /, port: 80 }
        initialDelaySeconds: 5
        periodSeconds: 10
      readinessProbe:
        httpGet: { path: /, port: 80 }
        initialDelaySeconds: 3
        periodSeconds: 5
```

> **La readiness probe est cruciale pendant un rolling update** : Kubernetes n'envoie du
> trafic vers un nouveau Pod nginx que lorsque la sonde le déclare **prêt**. C'est ce qui
> garantit le « zéro coupure » du module 04.

## 3. Requests & limits : maîtriser les ressources

On déclare ce qu'un conteneur **demande** (`requests`, utilisé par le scheduler pour le
placer) et son **plafond** (`limits`, au-delà duquel il est bridé ou tué).

```yaml
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      resources:
        requests:           # le minimum garanti (pour le placement)
          cpu: "100m"       # 0,1 cœur
          memory: "64Mi"
        limits:             # le maximum autorisé
          cpu: "500m"
          memory: "128Mi"
```

| Champ | Rôle |
|-------|------|
| `requests` | réservation garantie ; sert au **scheduler** |
| `limits` | plafond ; dépassement mémoire → Pod tué (**OOMKilled**) |

> **Bonne pratique :** toujours définir `requests`/`limits` en production, sinon un Pod
> peut monopoliser un node et affamer les autres.

## 4. TP complet : nginx de A à Z

Déployons nginx avec tout ce qu'on a vu, dans le namespace `demo`.

```bash
# 1) Namespace
kubectl create namespace demo

# 2) Config (ConfigMap)
kubectl create configmap nginx-conf --from-file=default.conf -n demo

# 3) Deployment : 3 réplicas
kubectl apply -f nginx-deployment.yaml -n demo
kubectl get pods -n demo                       # 3 Pods Running

# 4) Service : adresse stable
kubectl expose deployment nginx --port=80 -n demo
kubectl get svc -n demo

# 5) Exposition externe (Ingress)
kubectl apply -f nginx-ingress.yaml -n demo

# 6) Mise à jour sans coupure
kubectl set image deployment/nginx nginx=nginx:1.28 -n demo
kubectl rollout status deployment/nginx -n demo

# 7) Oups, on revient en arrière
kubectl rollout undo deployment/nginx -n demo

# 8) Scaling
kubectl scale deployment nginx --replicas=5 -n demo

# 9) Nettoyage complet
kubectl delete namespace demo                  # supprime TOUT le namespace
```

## 5. Aide-mémoire kubectl

```bash
# Observer
kubectl get pods|svc|deploy|ingress|pvc        # lister un type d'objet
kubectl get all -n <ns>                         # tout dans un namespace
kubectl get pods -o wide                        # avec IP et node
kubectl get pods -w                             # mode "watch" (temps réel)

# Comprendre / déboguer
kubectl describe pod <nom>                       # événements détaillés
kubectl logs <pod> [-f]                          # logs (-f = suivre)
kubectl exec -it <pod> -- sh                     # shell dans le conteneur
kubectl get events --sort-by=.lastTimestamp      # derniers événements

# Agir
kubectl apply -f fichier.yaml                    # créer/mettre à jour (déclaratif)
kubectl delete -f fichier.yaml                   # supprimer
kubectl scale deploy/<nom> --replicas=N          # scaler
kubectl rollout undo deploy/<nom>                # rollback
kubectl explain <objet>.spec                     # doc d'un champ YAML
```

## 6. Erreurs fréquentes & solutions

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| `ImagePullBackOff` | image introuvable / mal taguée | vérifier le nom et le tag de l'image |
| `CrashLoopBackOff` | l'app plante au démarrage | `kubectl logs <pod>` |
| `Pending` qui dure | pas assez de ressources / pas de PV | `kubectl describe pod` (events) |
| Service ne répond pas | selector ≠ labels des Pods | vérifier les `Endpoints` |
| PVC en `Pending` | pas de StorageClass / PV | `kubectl get sc`, `describe pvc` |
| Ingress 404 | pas de contrôleur / mauvais host | installer ingress-nginx, vérifier `host:` |

> **Méthode universelle :** `kubectl get pods` → repérer le statut anormal →
> `kubectl describe pod <nom>` (section *Events*) → `kubectl logs <nom>`. 90 % des pannes
> se diagnostiquent ainsi.

## 7. Checklist d'un déploiement propre

- [ ] Application déployée via un **Deployment** (jamais un Pod nu).
- [ ] **Labels** cohérents entre Deployment, Pods et Service (`app=nginx`).
- [ ] **Service** pour une adresse stable ; **Ingress** pour l'accès HTTP externe.
- [ ] **liveness** et **readiness** probes définies.
- [ ] **requests/limits** CPU et mémoire fixées.
- [ ] Config externalisée en **ConfigMap**, secrets en **Secret** (jamais dans l'image).
- [ ] **PVC** pour les données à conserver ; éphémère sinon.
- [ ] Images **taguées précisément** (pas `latest` en prod).
- [ ] Objets rangés dans un **namespace** dédié.
- [ ] Stratégie de **rolling update** + rollback validée.

---

## Conclusion

Avec une seule image — **nginx** — vous avez parcouru tous les concepts essentiels de
Kubernetes : **Pods**, **Deployments**, **rolling updates**, **Services**, **ConfigMaps**
et **Secrets**, **volumes persistants** et **Ingress**, plus les sondes de santé, les
ressources et les namespaces.

Le fil conducteur reste toujours le même : on **déclare un état désiré** en YAML, et
Kubernetes **converge** vers cet état, en réparant et en répliquant tout seul. C'est ce qui
transforme des conteneurs fragiles en applications **résilientes, scalables et
auto-réparées**.

> **Pour aller plus loin :** Helm (packager ses manifestes), RBAC (droits d'accès), les
> NetworkPolicies (cloisonnement réseau), le monitoring (Prometheus/Grafana), les Operators,
> et le GitOps (Argo CD / Flux) pour déployer sur Kubernetes… depuis Git.
