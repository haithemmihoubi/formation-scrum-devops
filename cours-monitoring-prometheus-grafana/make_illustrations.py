#!/usr/bin/env python3
"""Génère les illustrations SVG du cours Monitoring (Prometheus & Grafana).

Fil rouge : on supervise une application nginx.
"""
from pathlib import Path

IMG = Path(__file__).parent / "img"
IMG.mkdir(exist_ok=True)

# ---- Palette ----
INK     = "#1f2328"
MUTED   = "#57606a"
LINE    = "#d0d7de"
PROM    = "#e6522c"   # orange Prometheus
PROM_L  = "#fdeae4"
GRAF    = "#f46800"   # orange Grafana
GRAF_L  = "#fff1e5"
BLUE    = "#326ce5"
BLUE_L  = "#e8f0fe"
GREEN   = "#1a7f37"
GREEN_L = "#dafbe1"
PURPLE  = "#8250df"
PURPLE_L= "#fbefff"
TEAL    = "#0d7d7d"
TEAL_L  = "#d7f5f5"
GREY_L  = "#f6f8fa"
DARK    = "#24292e"
YELLOW_L= "#fff8c5"
RED     = "#cf222e"
RED_L   = "#ffebe9"

FONT = "font-family='DejaVu Sans, Segoe UI, sans-serif'"


def svg(w, h, body, bg="#ffffff"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
            f"viewBox='0 0 {w} {h}'><rect width='{w}' height='{h}' rx='10' fill='{bg}'/>"
            f"{body}</svg>")


def box(x, y, w, h, fill, stroke, r=10, sw=2, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' "
            f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}' {d}/>")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, fill=INK, weight="normal", anchor="middle"):
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill}' "
            f"font-weight='{weight}' text-anchor='{anchor}' {FONT}>{esc(s)}</text>")


def mono(x, y, s, size=11, fill=INK, anchor="start"):
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill}' "
            f"text-anchor='{anchor}' font-family='DejaVu Sans Mono, monospace'>{esc(s)}</text>")


def line(x1, y1, x2, y2, color=MUTED, sw=2, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' {d}/>")


def arrow(x1, y1, x2, y2, color=MUTED, sw=2.5, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' marker-end='url(#arr-{color.lstrip('#')})' {d}/>")


def marker(color):
    return (f"<marker id='arr-{color.lstrip('#')}' viewBox='0 0 10 10' refX='9' refY='5' "
            f"markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0 L10 5 L0 10 z' fill='{color}'/></marker>")


COLORS = [MUTED, PROM, GRAF, BLUE, GREEN, PURPLE, TEAL, RED, DARK]
DEFS = "<defs>" + "".join(marker(c) for c in COLORS) + "</defs>"


# ============================================================
# 1. Architecture Prometheus (modèle pull)
# ============================================================
def illu_architecture():
    W, H = 1100, 470
    b = DEFS
    b += text(W/2, 34, "L'architecture de Prometheus (modèle pull)", 20, INK, "bold")

    # Cibles (targets) à gauche
    targets = [("nginx", "/metrics", GREEN, GREEN_L, 80),
               ("node-exporter", "/metrics", BLUE, BLUE_L, 175),
               ("app backend", "/metrics", PURPLE, PURPLE_L, 270)]
    for name, path, c, cl, yy in targets:
        b += box(60, yy, 200, 70, cl, c, 10)
        b += text(160, yy+30, name, 13, c, "bold")
        b += mono(160-40, yy+52, path, 11, MUTED, "middle")
        b += arrow(360, 215, 262, yy+35, PROM, 2.5)
    b += text(160, 372, "Cibles exposant des métriques", 11, MUTED)

    # Prometheus (centre)
    b += box(360, 130, 280, 200, PROM_L, PROM, 14, 2.5)
    b += text(500, 158, "Prometheus", 16, PROM, "bold")
    b += text(500, 180, "scrape toutes les 15s (pull)", 10, MUTED)
    b += box(382, 196, 236, 50, "#ffffff", PROM, 9)
    b += text(500, 226, "TSDB", 13, INK, "bold")
    b += text(500, 244, "(base temps-réel)", 9.5, MUTED)
    b += box(382, 256, 236, 50, "#ffffff", PROM, 9)
    b += text(500, 280, "Moteur de règles", 12, INK, "bold")
    b += text(500, 297, "+ PromQL", 9.5, MUTED)

    # Grafana
    b += arrow(640, 200, 740, 200, GRAF, 3)
    b += box(740, 150, 180, 100, GRAF_L, GRAF, 12)
    b += text(830, 184, "Grafana", 15, GRAF, "bold")
    b += text(830, 208, "dashboards", 11, MUTED)
    b += text(830, 228, "(PromQL → courbes)", 9, MUTED)

    # Alertmanager
    b += arrow(640, 290, 740, 300, RED, 3)
    b += box(740, 275, 180, 75, RED_L, RED, 12)
    b += text(830, 304, "Alertmanager", 14, RED, "bold")
    b += text(830, 326, "notifie (mail, Slack)", 10, MUTED)

    b += text(W/2, 405, "Prometheus VA CHERCHER (pull) les métriques sur /metrics, les stocke, les interroge en PromQL.",
              11, MUTED)
    b += text(W/2, 428, "Grafana les visualise ; Alertmanager déclenche les alertes.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 2. Les 4 types de métriques
# ============================================================
def illu_metrics():
    W, H = 1040, 380
    b = DEFS
    b += text(W/2, 34, "Les quatre types de métriques Prometheus", 20, INK, "bold")

    types = [
        ("Counter", "ne fait qu'augmenter", "requêtes totales,\nerreurs cumulées", PROM, PROM_L,
         "nginx_requests_total"),
        ("Gauge", "monte et descend", "connexions actives,\nmémoire utilisée", BLUE, BLUE_L,
         "nginx_connections_active"),
        ("Histogram", "réparti en tranches", "latence des requêtes\n(buckets)", GREEN, GREEN_L,
         "request_duration_seconds"),
        ("Summary", "quantiles calculés", "p50, p90, p99\ncôté application", PURPLE, PURPLE_L,
         "rpc_duration_seconds"),
    ]
    bw, gap = 235, 18
    x0 = (W - (4*bw + 3*gap)) / 2
    for i, (name, desc, ex, c, cl, metric) in enumerate(types):
        x = x0 + i*(bw+gap)
        b += box(x, 80, bw, 250, cl, c, 12)
        b += text(x+bw/2, 110, name, 16, c, "bold")
        b += text(x+bw/2, 132, desc, 11, INK)
        b += box(x+16, 150, bw-32, 70, "#ffffff", c, 8)
        for k, ln in enumerate(ex.split("\n")):
            b += text(x+bw/2, 176+k*20, ln, 10.5, MUTED)
        b += box(x+16, 232, bw-32, 80, GREY_L, LINE, 8)
        b += text(x+bw/2, 254, "exemple", 9, MUTED, "bold")
        b += mono(x+bw/2, 278, metric.split("_")[0]+"_...", 10, c, "middle")
        b += mono(x+bw/2, 296, "_"+metric.split("_",1)[1] if "_" in metric else metric, 9, MUTED, "middle")
    b += text(W/2, 360, "Counter et Gauge couvrent 90 % des besoins. Histogram pour les latences.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 3. Anatomie d'une métrique + PromQL
# ============================================================
def illu_promql():
    W, H = 1040, 420
    b = DEFS
    b += text(W/2, 34, "Anatomie d'une métrique & requêtes PromQL", 20, INK, "bold")

    # métrique annotée
    b += box(60, 80, W-120, 90, GREY_L, PROM, 12)
    b += mono(90, 130, 'nginx_http_requests_total{method="GET", status="200"}  42', 16, INK)
    b += line(95, 138, 290, 138, PROM, 2)
    b += text(190, 158, "nom de la métrique", 10, PROM, "bold")
    b += line(300, 138, 560, 138, BLUE, 2)
    b += text(430, 158, "labels (dimensions)", 10, BLUE, "bold")
    b += line(640, 138, 690, 138, GREEN, 2)
    b += text(665, 158, "valeur", 10, GREEN, "bold")

    # requêtes PromQL
    queries = [
        ("Taux de requêtes / s (sur 5 min)", "rate(nginx_http_requests_total[5m])"),
        ("Filtrer par label", 'nginx_http_requests_total{status="500"}'),
        ("Total par méthode", "sum by (method) (rate(nginx_http_requests_total[5m]))"),
        ("% d'erreurs 5xx", 'sum(rate(...{status=~"5.."}[5m])) / sum(rate(...[5m]))'),
        ("Latence p95", "histogram_quantile(0.95, rate(req_duration_seconds_bucket[5m]))"),
    ]
    y = 210
    for label, q in queries:
        b += text(80, y+18, label, 11.5, INK, "bold", "start")
        b += box(360, y, W-420, 32, "#1f2328", DARK, 7)
        b += mono(378, y+21, q, 11, "#7ee787")
        y += 42

    return svg(W, H, b)


# ============================================================
# 4. La stack de monitoring (collecte -> stockage -> visu -> alerte)
# ============================================================
def illu_stack():
    W, H = 1080, 360
    b = DEFS
    b += text(W/2, 34, "La chaîne complète du monitoring", 20, INK, "bold")

    steps = [
        ("1. Exposer", "nginx + exporter\n/metrics", GREEN, GREEN_L),
        ("2. Collecter", "Prometheus\nscrape (pull)", PROM, PROM_L),
        ("3. Stocker", "TSDB\nséries temporelles", BLUE, BLUE_L),
        ("4. Visualiser", "Grafana\ndashboards", GRAF, GRAF_L),
        ("5. Alerter", "Alertmanager\nmail / Slack", RED, RED_L),
    ]
    bw, gap = 180, 28
    x0 = (W - (5*bw + 4*gap)) / 2
    for i, (title, desc, c, cl) in enumerate(steps):
        x = x0 + i*(bw+gap)
        b += box(x, 110, bw, 120, cl, c, 12)
        b += text(x+bw/2, 142, title, 14, c, "bold")
        for k, ln in enumerate(desc.split("\n")):
            b += text(x+bw/2, 172+k*22, ln, 11, INK)
        if i < 4:
            b += arrow(x+bw+2, 170, x+bw+gap-4, 170, MUTED, 3)

    b += text(W/2, 290, "On instrumente l'application, Prometheus collecte et stocke, Grafana affiche, Alertmanager prévient.",
              11.5, MUTED)
    b += text(W/2, 316, "Les 3 piliers de l'observabilité : métriques (ici), logs, traces.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 5. Pipeline d'alerting
# ============================================================
def illu_alerting():
    W, H = 1040, 380
    b = DEFS
    b += text(W/2, 34, "Le pipeline d'alerting", 20, INK, "bold")

    # règle
    b += box(50, 100, 300, 150, PROM_L, PROM, 12)
    b += text(200, 126, "Règle d'alerte (Prometheus)", 12, PROM, "bold")
    b += box(66, 140, 268, 96, "#1f2328", DARK, 8)
    b += mono(82, 162, "alert: HighErrorRate", 10.5, "#ff7b72")
    b += mono(82, 182, "expr: rate(5xx[5m])", 10.5, "#79c0ff")
    b += mono(82, 198, "      > 0.05", 10.5, "#79c0ff")
    b += mono(82, 218, "for: 10m", 10.5, "#7ee787")

    b += arrow(350, 175, 430, 175, PROM, 3)
    b += text(390, 160, "déclenche", 9.5, MUTED, "bold")

    # Alertmanager
    b += box(430, 110, 220, 130, RED_L, RED, 12)
    b += text(540, 138, "Alertmanager", 14, RED, "bold")
    b += text(540, 162, "regroupe", 10.5, INK)
    b += text(540, 182, "déduplique", 10.5, INK)
    b += text(540, 202, "route + silence", 10.5, INK)
    b += text(540, 222, "respecte les horaires", 9.5, MUTED)

    # destinations
    dests = [("Email", TEAL, TEAL_L, 90), ("Slack", PURPLE, PURPLE_L, 175), ("PagerDuty", BLUE, BLUE_L, 260)]
    for name, c, cl, yy in dests:
        b += arrow(650, 175, 740, yy+25, c, 2.5)
        b += box(740, yy, 200, 50, cl, c, 10)
        b += text(840, yy+30, name, 13, c, "bold")

    b += text(W/2, 320, "Une alerte ne se déclenche que si la condition tient pendant la durée 'for'.", 11, MUTED)
    b += text(W/2, 344, "Alertmanager évite le spam : il regroupe et route intelligemment.", 11, MUTED)
    return svg(W, H, b)


def main():
    illus = {
        "01-architecture.svg": illu_architecture(),
        "02-metrics.svg":      illu_metrics(),
        "03-promql.svg":       illu_promql(),
        "04-stack.svg":        illu_stack(),
        "05-alerting.svg":     illu_alerting(),
    }
    for name, content in illus.items():
        (IMG / name).write_text(content, encoding="utf-8")
        print(f"  + img/{name}")
    print(f"\n{len(illus)} illustrations générées dans {IMG}")


if __name__ == "__main__":
    main()
