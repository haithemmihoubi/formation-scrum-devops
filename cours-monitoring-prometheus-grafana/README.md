# Cours : Monitoring avec Prometheus & Grafana

Support de formation DevOps **avec illustrations** qui enseigne le **monitoring** avec
Prometheus, Grafana et Alertmanager, à travers un fil rouge : **superviser nginx**.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : l'observabilité (métriques, logs, traces) |
| 01 | L'architecture de Prometheus (modèle pull, scraping, TSDB, service discovery) |
| 02 | Les métriques : types (Counter/Gauge/Histogram/Summary), exporters, RED |
| 03 | PromQL : sélecteurs, rate, agrégation, % d'erreurs, quantiles |
| 04 | Grafana : data source, panneaux, variables, dashboards |
| 05 | L'alerting : règles, Alertmanager, routage, notifications |
| 06 | Pratique sur Kubernetes (kube-prometheus-stack, ServiceMonitor) & checklist |

## Illustrations

Cinq diagrammes vectoriels (SVG) : architecture pull de Prometheus, les 4 types de
métriques, anatomie d'une métrique + requêtes PromQL, la chaîne complète du monitoring, et
le pipeline d'alerting.

## Générer le PDF

```bash
pip install markdown weasyprint
python3 build_pdf.py    # régénère les illustrations puis Cours-Monitoring-Prometheus-Grafana.pdf
```

`build_pdf.py` appelle automatiquement `make_illustrations.py`. Chaque module est un `.md`
autonome.
