#!/usr/bin/env python3
"""Génère les illustrations SVG du cours Helm (vectoriel, net à l'impression).

Fil rouge : un chart Helm qui déploie nginx illustre tous les concepts.
"""
from pathlib import Path

IMG = Path(__file__).parent / "img"
IMG.mkdir(exist_ok=True)

# ---- Palette ----
INK     = "#1f2328"
MUTED   = "#57606a"
LINE    = "#d0d7de"
HELM    = "#0f1689"   # bleu Helm
HELM_L  = "#e6e8fb"
BLUE    = "#326ce5"
BLUE_L  = "#e8f0fe"
GREEN   = "#1a7f37"
GREEN_L = "#dafbe1"
PURPLE  = "#8250df"
PURPLE_L= "#fbefff"
ORANGE  = "#bc4c00"
ORANGE_L= "#fff1e5"
TEAL    = "#0d7d7d"
TEAL_L  = "#d7f5f5"
GREY_L  = "#f6f8fa"
DARK    = "#24292e"
YELLOW_L= "#fff8c5"

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


def arrow(x1, y1, x2, y2, color=MUTED, sw=2.5, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' marker-end='url(#arr-{color.lstrip('#')})' {d}/>")


def marker(color):
    return (f"<marker id='arr-{color.lstrip('#')}' viewBox='0 0 10 10' refX='9' refY='5' "
            f"markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0 L10 5 L0 10 z' fill='{color}'/></marker>")


COLORS = [MUTED, HELM, BLUE, GREEN, PURPLE, ORANGE, TEAL, DARK]
DEFS = "<defs>" + "".join(marker(c) for c in COLORS) + "</defs>"


# ============================================================
# 1. Vue d'ensemble Helm
# ============================================================
def illu_overview():
    W, H = 1080, 400
    b = DEFS
    b += text(W/2, 34, "Helm : le gestionnaire de paquets de Kubernetes", 20, INK, "bold")

    # Chart (templates + values)
    b += box(50, 90, 250, 230, HELM_L, HELM, 14, 2.5)
    b += text(175, 116, "Chart nginx", 15, HELM, "bold")
    b += box(70, 132, 210, 80, "#ffffff", BLUE, 9)
    b += text(175, 154, "templates/", 12, BLUE, "bold")
    b += mono(90, 176, "deployment.yaml", 10, MUTED)
    b += mono(90, 194, "service.yaml", 10, MUTED)
    b += box(70, 222, 210, 80, "#ffffff", ORANGE, 9)
    b += text(175, 244, "values.yaml", 12, ORANGE, "bold")
    b += mono(90, 266, "replicaCount: 3", 10, MUTED)
    b += mono(90, 284, "image: nginx:1.27", 10, MUTED)

    # helm engine
    b += arrow(300, 205, 400, 205, HELM, 3)
    b += box(400, 165, 150, 80, DARK, DARK, 12)
    b += text(475, 198, "helm", 17, "#ffffff", "bold")
    b += text(475, 222, "render + apply", 10, "#c9d1d9")

    # manifests rendus
    b += arrow(550, 205, 650, 205, HELM, 3)
    b += box(650, 130, 200, 150, GREY_L, LINE, 12)
    b += text(750, 154, "Manifests rendus", 12, INK, "bold")
    b += mono(666, 178, "Deployment (3 répl.)", 9.5, MUTED)
    b += mono(666, 200, "Service nginx", 9.5, MUTED)
    b += mono(666, 222, "ConfigMap", 9.5, MUTED)
    b += text(750, 262, "= une Release", 11, GREEN, "bold")

    # cluster
    b += arrow(850, 205, 950, 205, HELM, 3)
    b += box(900, 150, 140, 110, BLUE_L, BLUE, 12)
    b += text(970, 178, "Cluster", 13, BLUE, "bold")
    b += text(970, 204, "Kubernetes", 10, MUTED)
    b += text(970, 230, "nginx déployé", 10, GREEN)

    b += text(W/2, 372, "Un Chart (modèles + valeurs) → helm les assemble → une Release versionnée tourne dans le cluster.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 2. Structure d'un chart
# ============================================================
def illu_structure():
    W, H = 760, 460
    b = DEFS
    b += text(W/2, 34, "L'arborescence d'un chart Helm", 20, INK, "bold")

    b += box(60, 70, W-120, 350, GREY_L, HELM, 14, 2.5)
    rows = [
        ("nginx/", "le dossier du chart", HELM, 0, True),
        ("Chart.yaml", "métadonnées : nom, version", INK, 1, False),
        ("values.yaml", "valeurs par défaut (configurables)", ORANGE, 1, False),
        ("templates/", "les modèles de manifestes", BLUE, 1, True),
        ("deployment.yaml", "Deployment nginx (templatisé)", MUTED, 2, False),
        ("service.yaml", "Service nginx (templatisé)", MUTED, 2, False),
        ("_helpers.tpl", "fonctions/labels réutilisables", MUTED, 2, False),
        ("NOTES.txt", "message affiché après install", MUTED, 2, False),
        ("charts/", "sous-charts (dépendances)", PURPLE, 1, True),
    ]
    y = 104
    for name, desc, col, depth, isdir in rows:
        x = 90 + depth*36
        if isdir:
            b += text(x, y, "▸ " + name, 13.5, col, "bold", "start")
        else:
            b += mono(x, y, name, 12.5, col)
        b += text(W-90, y, desc, 10.5, MUTED, "normal", "end")
        y += 36
    return svg(W, H, b)


# ============================================================
# 3. Le templating (values + template -> manifest)
# ============================================================
def illu_templating():
    W, H = 1060, 440
    b = DEFS
    b += text(W/2, 34, "Le templating : un modèle + des valeurs = un manifeste", 20, INK, "bold")

    # template
    b += box(40, 80, 380, 250, "#1f2328", DARK, 12)
    b += text(230, 104, "templates/deployment.yaml", 12, "#7ee787", "bold")
    tlines = [
        ("kind: Deployment", "#e6edf3"),
        ("spec:", "#e6edf3"),
        ("  replicas: {{ .Values.replicaCount }}", "#79c0ff"),
        ("  template:", "#e6edf3"),
        ("    spec:", "#e6edf3"),
        ("      containers:", "#e6edf3"),
        ("      - image: {{ .Values.image }}", "#79c0ff"),
    ]
    for i, (ln, c) in enumerate(tlines):
        b += mono(58, 134 + i*24, ln, 10.5, c)

    # values
    b += box(40, 348, 380, 56, ORANGE_L, ORANGE, 10)
    b += text(60, 370, "values.yaml :", 11, ORANGE, "bold", "start")
    b += mono(170, 370, "replicaCount: 3", 10, INK)
    b += mono(170, 392, "image: nginx:1.27", 10, INK)

    # arrow + helm
    b += arrow(420, 230, 540, 230, HELM, 3.5)
    b += text(480, 214, "helm", 12, HELM, "bold")
    b += text(480, 320, "+ values", 11, ORANGE, "bold")
    b += arrow(420, 376, 500, 300, ORANGE, 2.5, "4 3")

    # rendered
    b += box(560, 80, 460, 250, GREEN_L, GREEN, 12)
    b += text(790, 104, "Manifeste rendu (appliqué au cluster)", 12, GREEN, "bold")
    rlines = [
        "kind: Deployment",
        "spec:",
        "  replicas: 3",
        "  template:",
        "    spec:",
        "      containers:",
        "      - image: nginx:1.27",
    ]
    for i, ln in enumerate(rlines):
        col = HELM if ("replicas: 3" in ln or "nginx:1.27" in ln) else INK
        w = "bold" if col == HELM else "normal"
        b += mono(580, 134 + i*24, ln, 10.5, col)

    b += text(W/2, 426, "Le même chart, des valeurs différentes (dev/prod) → des manifestes différents, sans copier-coller.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 4. Cycle de vie d'une release
# ============================================================
def illu_release():
    W, H = 1080, 360
    b = DEFS
    b += text(W/2, 34, "Le cycle de vie d'une Release (révisions)", 20, INK, "bold")

    steps = [
        ("helm install", "Révision 1", "nginx:1.27\n3 réplicas", GREEN, GREEN_L),
        ("helm upgrade", "Révision 2", "nginx:1.28\n3 réplicas", BLUE, BLUE_L),
        ("helm upgrade", "Révision 3", "nginx:1.28\n5 réplicas", BLUE, BLUE_L),
        ("helm rollback 2", "→ Révision 2", "retour\nnginx:1.28 / 3", ORANGE, ORANGE_L),
    ]
    bw, gap = 230, 30
    x0 = (W - (4*bw + 3*gap)) / 2
    for i, (cmd, rev, state, c, cl) in enumerate(steps):
        x = x0 + i*(bw+gap)
        b += box(x, 90, bw, 50, DARK, DARK, 9)
        b += mono(x+bw/2, 120, cmd, 12, "#7ee787", "middle")
        b += box(x, 158, bw, 110, cl, c, 12)
        b += text(x+bw/2, 186, rev, 14, c, "bold")
        for k, ln in enumerate(state.split("\n")):
            b += text(x+bw/2, 212+k*20, ln, 11, INK)
        if i < 3:
            b += arrow(x+bw+2, 213, x+bw+gap-4, 213, c, 3)

    b += text(W/2, 312, "Helm garde l'historique : helm history nginx. Un upgrade raté ? helm rollback en une commande.",
              11, MUTED)
    b += text(W/2, 336, "Chaque install/upgrade crée une nouvelle révision ; rien n'est jamais perdu.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 5. Dépendances (sous-charts)
# ============================================================
def illu_dependencies():
    W, H = 980, 400
    b = DEFS
    b += text(W/2, 34, "Les dépendances : un chart qui en embarque d'autres", 20, INK, "bold")
    b += text(W/2, 58, "Chart.yaml › dependencies — déclarez, helm dependency update les télécharge", 12, MUTED)

    # parent
    b += box(360, 90, 260, 80, HELM_L, HELM, 12)
    b += text(490, 120, "Chart parent", 15, HELM, "bold")
    b += text(490, 142, "quickbite", 12, MUTED)
    b += text(490, 160, "version: 1.0.0", 10, MUTED)

    subs = [
        ("nginx", "le frontend", GREEN, GREEN_L, 120),
        ("redis", "le cache", PURPLE, PURPLE_L, 420),
        ("postgresql", "la base", BLUE, BLUE_L, 700),
    ]
    for name, role, c, cl, x in subs:
        b += arrow(490, 170, x+80, 245, HELM, 2.5)
        b += box(x, 250, 160, 90, cl, c, 12)
        b += text(x+80, 282, name, 14, c, "bold")
        b += text(x+80, 304, role, 11, MUTED)
        b += text(x+80, 324, "sous-chart", 9.5, MUTED)

    b += text(W/2, 380, "On installe le parent, Helm déploie tout l'ensemble cohérent en une seule Release.",
              11, MUTED)
    return svg(W, H, b)


def main():
    illus = {
        "01-overview.svg":      illu_overview(),
        "02-structure.svg":     illu_structure(),
        "03-templating.svg":    illu_templating(),
        "04-release.svg":       illu_release(),
        "05-dependencies.svg":  illu_dependencies(),
    }
    for name, content in illus.items():
        (IMG / name).write_text(content, encoding="utf-8")
        print(f"  + img/{name}")
    print(f"\n{len(illus)} illustrations générées dans {IMG}")


if __name__ == "__main__":
    main()
