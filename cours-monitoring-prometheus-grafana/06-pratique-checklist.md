# Pratique sur Kubernetes & checklist

On rassemble tout : déployer la stack de monitoring sur un cluster Kubernetes, superviser
nginx de bout en bout, puis une checklist finale.

## 1. La voie rapide : kube-prometheus-stack

Sur Kubernetes, on **n'installe pas** Prometheus, Grafana et Alertmanager à la main. On
déploie le **chart Helm** `kube-prometheus-stack`, qui livre l'ensemble **préconfiguré et
intégré**.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

On obtient d'un coup :

| Composant | Rôle |
|-----------|------|
| **Prometheus** | collecte (déployé via l'**Operator**) |
| **Grafana** | dashboards (avec des dashboards K8s pré-installés) |
| **Alertmanager** | alerting |
| **node-exporter** | métriques de chaque node |
| **kube-state-metrics** | état des objets K8s (Pods, Deployments…) |

```bash
# Accéder à Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# → http://localhost:3000  (admin / prom-operator)
```

## 2. Le Prometheus Operator : surveiller de façon déclarative

L'Operator introduit des objets Kubernetes dédiés. Au lieu d'éditer `prometheus.yml`, on
**déclare** quoi surveiller avec un **ServiceMonitor**.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: nginx
  namespace: monitoring
  labels:
    release: monitoring        # pour que Prometheus l'adopte
spec:
  selector:
    matchLabels:
      app: nginx               # cible le Service nginx
  endpoints:
    - port: metrics            # le port nommé "metrics" du Service
      interval: 15s
```

> **C'est du monitoring déclaratif, cohérent avec Kubernetes :** on crée un Service nginx +
> un ServiceMonitor, et Prometheus se met à le scraper **automatiquement**. Pas de
> rechargement de config manuel.

## 3. Superviser nginx de bout en bout

```bash
# 1) Déployer nginx avec son exporter (sidecar) — Deployment + Service
kubectl apply -f nginx-with-exporter.yaml -n monitoring

# 2) Déclarer le ServiceMonitor
kubectl apply -f nginx-servicemonitor.yaml -n monitoring

# 3) Vérifier que Prometheus voit la cible
#    UI Prometheus ▸ Status ▸ Targets  →  nginx = UP

# 4) Dans Grafana : importer le dashboard "NGINX exporter" (ID 12708)

# 5) Créer une PrometheusRule pour l'alerte taux d'erreurs
kubectl apply -f nginx-alert-rule.yaml -n monitoring
```

Règle d'alerte au format Operator (`PrometheusRule`) :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: nginx-rules
  labels: { release: monitoring }
spec:
  groups:
    - name: nginx
      rules:
        - alert: NginxHighErrorRate
          expr: |
            sum(rate(nginx_http_requests_total{status=~"5.."}[5m]))
            / sum(rate(nginx_http_requests_total[5m])) > 0.05
          for: 10m
          labels: { severity: critical }
          annotations:
            summary: "nginx : taux d'erreurs 5xx > 5 %"
```

## 4. Que surveiller en priorité (rappel)

| Niveau | Méthode | Métriques |
|--------|---------|-----------|
| **Service** (nginx) | **RED** | Rate (req/s), Errors (% 5xx), Duration (latence p95) |
| **Machine / node** | **USE** | Utilization, Saturation, Errors (CPU, RAM, disque) |
| **Kubernetes** | — | Pods non prêts, redémarrages, `up == 0` |

## 5. Erreurs fréquentes & solutions

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Cible `DOWN` | endpoint `/metrics` injoignable | vérifier le port, le réseau, l'exporter |
| Aucune métrique nginx | exporter mal configuré | tester `curl <exporter>:9113/metrics` |
| ServiceMonitor ignoré | label `release` manquant | aligner sur le label attendu par Prometheus |
| Trop de séries, Prometheus lent | **cardinalité** des labels | retirer les labels à forte variabilité |
| Grafana « No data » | mauvaise source / requête | vérifier la data source et le PromQL dans *Explore* |
| Alerte jamais déclenchée | `for` trop long / `expr` fausse | tester l'`expr` dans l'UI Prometheus |
| Pluie d'alertes | pas de `for` / pas de regroupement | ajouter `for`, `group_by` dans Alertmanager |

## 6. Checklist d'un monitoring sain

- [ ] Stack déployée (`kube-prometheus-stack` ou équivalent).
- [ ] Chaque service expose `/metrics` (natif ou via un **exporter**).
- [ ] Cibles **UP** dans *Status ▸ Targets*.
- [ ] Métriques **RED** suivies pour chaque service clé (nginx).
- [ ] Métriques **USE** suivies pour les nodes.
- [ ] Dashboards Grafana en place (importés ou versionnés en JSON).
- [ ] Alertes sur les **symptômes** (erreurs, latence, `up == 0`), avec un `for`.
- [ ] Alertmanager routé vers un vrai canal (Slack/mail/astreinte) et **testé**.
- [ ] **Cardinalité** des labels maîtrisée.
- [ ] Rétention et stockage long terme pensés si besoin (Thanos/Mimir).

---

## Conclusion

Avec **nginx** comme fil rouge, vous avez bâti une chaîne de monitoring complète : exposer
des **métriques**, les **collecter** avec Prometheus (modèle pull), les interroger en
**PromQL**, les **visualiser** dans Grafana, et **alerter** via Alertmanager — le tout
déployé de façon **déclarative** sur Kubernetes.

Le monitoring n'est pas un luxe : c'est ce qui permet de **voir venir** les problèmes,
de **comprendre** les pannes et de **dormir tranquille** parce qu'on sera prévenu à temps.

> **Pour aller plus loin :** les **logs** avec Loki (et l'exploration corrélée dans
> Grafana), les **traces** distribuées avec Tempo/Jaeger (OpenTelemetry), les **SLO/SLI**
> et budgets d'erreur, et le stockage longue durée multi-cluster (Thanos, Mimir).
