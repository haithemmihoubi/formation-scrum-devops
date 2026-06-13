# Grafana : visualiser les métriques

Prometheus stocke et calcule ; **Grafana** transforme ces chiffres en **tableaux de bord**
lisibles, partageables et dynamiques.

## 1. Le rôle de Grafana

- Se connecte à une **source de données** (Prometheus, mais aussi Loki, Elasticsearch…).
- Affiche des **panneaux** (panels) : courbes, jauges, compteurs, tableaux.
- Organise les panneaux en **dashboards** réutilisables.
- Offre des **variables**, des **annotations** et ses propres **alertes**.

> Grafana ne stocke pas les métriques : il **interroge** Prometheus en PromQL à chaque
> affichage. C'est une **fenêtre** sur les données, pas un entrepôt.

## 2. Connecter Prometheus comme source de données

Dans Grafana (`http://localhost:3000`, défaut `admin`/`admin`) :

**Configuration ▸ Data sources ▸ Add ▸ Prometheus**, puis l'URL :

```
http://prometheus:9090      # nom du service Prometheus (ou localhost:9090)
```

On peut aussi la déclarer en **YAML** (provisioning, versionnable) :

```yaml
# datasources.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## 3. Créer un dashboard pour nginx

**Dashboards ▸ New ▸ Add visualization**, choisir la source Prometheus, puis saisir une
requête PromQL par panneau.

| Panneau | Requête PromQL | Type de visu |
|---------|----------------|--------------|
| Requêtes/s | `sum(rate(nginx_http_requests_total[5m]))` | Time series |
| % d'erreurs 5xx | `sum(rate(...{status=~"5.."}[5m])) / sum(rate(...[5m]))` | Gauge / Stat |
| Connexions actives | `nginx_connections_active` | Time series |
| Latence p95 | `histogram_quantile(0.95, ...)` | Time series |

## 4. Les types de panneaux courants

| Type | Pour |
|------|------|
| **Time series** | l'évolution dans le temps (le plus utilisé) |
| **Stat** | une grande valeur unique (req/s actuelles) |
| **Gauge** | une valeur sur une échelle (% CPU, % erreurs) |
| **Bar gauge** | comparer des catégories |
| **Table** | données détaillées par série |
| **Heatmap** | distribution (idéal pour les histograms de latence) |

## 5. Les variables : des dashboards dynamiques

Plutôt qu'un dashboard figé, on ajoute des **variables** (menus déroulants) pour filtrer.

```promql
# Variable $instance : liste des instances disponibles
label_values(nginx_http_requests_total, instance)

# Dans les panneaux, on filtre par la variable
rate(nginx_http_requests_total{instance="$instance"}[5m])
```

→ un **seul** dashboard sert pour **toutes** les instances : on choisit dans le menu.

## 6. Ne pas réinventer la roue : importer des dashboards

Des milliers de dashboards prêts à l'emploi existent sur **grafana.com/dashboards**. On les
importe par leur **ID**.

**Dashboards ▸ Import**, entrer l'ID (ex. *NGINX exporter* ou *Node Exporter Full*),
choisir la source Prometheus. Le dashboard apparaît, complet.

| Dashboard | ID indicatif |
|-----------|--------------|
| Node Exporter Full | 1860 |
| NGINX (exporter) | 12708 |
| Kubernetes cluster | 7249 |

## 7. Bonnes pratiques de dashboard

- **Une intention par dashboard** : « santé de nginx », « ressources du cluster »…
- Placer les **métriques RED** en haut (débit, erreurs, latence).
- Des **unités** correctes (req/s, %, ms, octets) pour des axes lisibles.
- Des **seuils** colorés (vert/orange/rouge) pour repérer l'anormal d'un coup d'œil.
- **Versionner** les dashboards en JSON (provisioning) plutôt que les cliquer à la main.

```yaml
# dashboards provisioning : Grafana charge les JSON d'un dossier
apiVersion: 1
providers:
  - name: 'default'
    folder: 'nginx'
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

## 8. Grafana vs l'UI Prometheus

| | UI Prometheus | Grafana |
|---|--------------|---------|
| Explorer/déboguer une requête | ✅ rapide | ✅ (Explore) |
| Dashboards présentables | ✗ | ✅ |
| Partage, variables, seuils | ✗ | ✅ |
| Multi-sources (logs, métriques) | ✗ | ✅ |

> **À retenir :** Grafana = la couche de visualisation. On branche Prometheus en source, on
> compose des panneaux PromQL (priorité aux métriques RED), on rend tout dynamique avec des
> variables, et on importe des dashboards existants pour gagner du temps.
