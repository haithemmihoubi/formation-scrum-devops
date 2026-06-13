#!/usr/bin/env python3
"""Génère les illustrations SVG du cours GitOps avec Argo CD.

Fil rouge : on déploie nginx via GitOps.
"""
from pathlib import Path

IMG = Path(__file__).parent / "img"
IMG.mkdir(exist_ok=True)

# ---- Palette ----
INK     = "#1f2328"
MUTED   = "#57606a"
LINE    = "#d0d7de"
ARGO    = "#ef7b4d"   # orange Argo
ARGO_L  = "#fdeee6"
BLUE    = "#326ce5"
BLUE_L  = "#e8f0fe"
GIT     = "#f05133"   # rouge Git
GIT_L   = "#fde8e4"
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


COLORS = [MUTED, ARGO, BLUE, GIT, GREEN, PURPLE, TEAL, RED, DARK]
DEFS = "<defs>" + "".join(marker(c) for c in COLORS) + "</defs>"


# ============================================================
# 1. Push vs Pull (CI/CD classique vs GitOps)
# ============================================================
def illu_push_pull():
    W, H = 1080, 420
    b = DEFS
    b += text(W/2, 32, "CI/CD classique (push) vs GitOps (pull)", 20, INK, "bold")

    # PUSH (haut)
    b += text(80, 78, "Push : le pipeline POUSSE dans le cluster", 13, MUTED, "bold", "start")
    b += box(60, 92, 200, 70, GREY_L, DARK, 10)
    b += text(160, 124, "Pipeline CI/CD", 13, DARK, "bold")
    b += text(160, 144, "(kubectl apply)", 10, MUTED)
    b += arrow(260, 127, 470, 127, RED, 3)
    b += text(365, 112, "a les droits d'écriture", 10, RED, "bold")
    b += box(470, 92, 200, 70, BLUE_L, BLUE, 10)
    b += text(570, 124, "Cluster K8s", 13, BLUE, "bold")
    b += text(570, 144, "subit les ordres", 10, MUTED)
    b += text(820, 120, "✗ identifiants du cluster", 11, RED, "normal", "start")
    b += text(820, 140, "  exposés au pipeline", 11, RED, "normal", "start")

    # séparateur
    b += line(60, 195, W-60, 195, LINE, 1.5, "6 5")

    # PULL (bas)
    b += text(80, 232, "Pull (GitOps) : un agent DANS le cluster tire depuis Git", 13, ARGO, "bold", "start")
    b += box(60, 250, 190, 80, GIT_L, GIT, 10)
    b += text(155, 282, "Dépôt Git", 13, GIT, "bold")
    b += text(155, 304, "état désiré (YAML)", 10, MUTED)

    b += box(360, 250, 190, 80, ARGO_L, ARGO, 10)
    b += text(455, 278, "Argo CD", 13, ARGO, "bold")
    b += text(455, 300, "(dans le cluster)", 10, MUTED)
    b += arrow(360, 290, 255, 290, ARGO, 3)
    b += text(307, 274, "tire (pull)", 9.5, ARGO, "bold")

    b += box(660, 250, 190, 80, BLUE_L, BLUE, 10)
    b += text(755, 282, "Cluster K8s", 13, BLUE, "bold")
    b += text(755, 304, "= reflet de Git", 10, GREEN)
    b += arrow(550, 290, 655, 290, ARGO, 3)
    b += text(602, 274, "applique", 9.5, ARGO, "bold")

    b += text(905, 282, "✓ aucun secret", 11, GREEN, "normal", "start")
    b += text(905, 302, "  ne sort du cluster", 11, GREEN, "normal", "start")

    b += text(W/2, 384, "En GitOps, on ne pousse plus vers le cluster : on écrit dans Git, et l'agent réconcilie le cluster avec Git.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 2. La boucle de réconciliation GitOps
# ============================================================
def illu_loop():
    W, H = 1000, 475
    b = DEFS
    b += text(W/2, 34, "La boucle de réconciliation GitOps", 20, INK, "bold")

    # 4 noeuds en cercle
    nodes = [
        ("1. Git", "l'état désiré\n(manifests / Helm)", GIT, GIT_L, 500, 100),
        ("2. Argo CD", "compare Git\net le cluster", ARGO, ARGO_L, 820, 250),
        ("3. Cluster", "état réel\nappliqué", BLUE, BLUE_L, 500, 400),
        ("4. Diff", "synced ?\nsinon → sync", PURPLE, PURPLE_L, 180, 250),
    ]
    cx, cy = 500, 250
    for title, desc, c, cl, x, y in nodes:
        b += box(x-110, y-46, 220, 92, cl, c, 12)
        b += text(x, y-18, title, 15, c, "bold")
        for k, ln in enumerate(desc.split("\n")):
            b += text(x, y+4+k*18, ln, 10.5, INK)

    # flèches circulaires
    b += arrow(640, 130, 760, 210, ARGO, 3)
    b += arrow(820, 305, 610, 380, BLUE, 3)
    b += arrow(390, 380, 230, 305, PURPLE, 3)
    b += arrow(240, 200, 400, 120, GIT, 3)

    b += text(cx, cy-6, "git push", 14, GIT, "bold")
    b += text(cx, cy+16, "= la seule action", 11, MUTED)
    b += text(cx, cy+36, "humaine", 11, MUTED)

    b += text(W/2, 462, "Argo CD compare en continu Git (désiré) et le cluster (réel), et corrige tout écart.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 3. L'objet Application d'Argo CD
# ============================================================
def illu_application():
    W, H = 1020, 400
    b = DEFS
    b += text(W/2, 34, "L'objet Application : le lien Git → Cluster", 20, INK, "bold")

    # Application (centre)
    b += box(380, 120, 260, 200, ARGO_L, ARGO, 14, 2.5)
    b += text(510, 148, "Application", 16, ARGO, "bold")
    b += text(510, 168, "(objet Argo CD)", 10, MUTED)
    b += box(398, 180, 224, 60, "#ffffff", GIT, 8)
    b += text(510, 200, "source", 11, GIT, "bold")
    b += mono(412, 220, "repo + path + revision", 10, MUTED)
    b += box(398, 248, 224, 60, "#ffffff", BLUE, 8)
    b += text(510, 268, "destination", 11, BLUE, "bold")
    b += mono(412, 288, "cluster + namespace", 10, MUTED)

    # Git source
    b += box(60, 150, 240, 130, GIT_L, GIT, 12)
    b += text(180, 176, "source : Git", 13, GIT, "bold")
    b += mono(78, 202, "repoURL: .../infra", 10, INK)
    b += mono(78, 222, "path: apps/nginx", 10, INK)
    b += mono(78, 242, "targetRevision: main", 10, INK)
    b += mono(78, 262, "(manifests / Helm / Kustomize)", 9, MUTED)
    b += arrow(300, 215, 378, 210, GIT, 3)

    # Cluster destination
    b += box(720, 150, 240, 130, BLUE_L, BLUE, 12)
    b += text(840, 176, "destination : cluster", 12, BLUE, "bold")
    b += mono(738, 202, "server: in-cluster", 10, INK)
    b += mono(738, 222, "namespace: prod", 10, INK)
    b += text(840, 250, "nginx déployé", 12, GREEN, "bold")
    b += text(840, 270, "= reflet exact de Git", 9.5, MUTED)
    b += arrow(640, 230, 718, 230, BLUE, 3)

    b += text(W/2, 380, "Une Application dit : « prends CE chemin de CE dépôt et applique-le sur CE cluster ».", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 4. Sync, états et self-heal
# ============================================================
def illu_sync():
    W, H = 1040, 400
    b = DEFS
    b += text(W/2, 34, "États de synchronisation & auto-réparation", 20, INK, "bold")

    # états
    states = [
        ("Synced", "cluster = Git", GREEN, GREEN_L),
        ("OutOfSync", "Git a changé\n(ou dérive manuelle)", ORANGEish := "#bc4c00", "#fff1e5"),
        ("Healthy", "ressources OK", GREEN, GREEN_L),
        ("Degraded", "un Pod plante", RED, RED_L),
    ]
    bw, gap = 230, 18
    x0 = (W - (4*bw + 3*gap)) / 2
    for i, (name, desc, c, cl) in enumerate(states):
        x = x0 + i*(bw+gap)
        b += box(x, 80, bw, 90, cl, c, 12)
        b += text(x+bw/2, 110, name, 15, c, "bold")
        for k, ln in enumerate(desc.split("\n")):
            b += text(x+bw/2, 132+k*17, ln, 10.5, INK)

    # scénario self-heal
    b += text(W/2, 218, "Scénario : quelqu'un modifie le cluster à la main (kubectl edit)", 12, INK, "bold")
    flow = [
        ("Dérive", "le cluster ≠ Git", RED, RED_L),
        ("Argo détecte", "OutOfSync", "#bc4c00", "#fff1e5"),
        ("Self-heal", "réapplique Git", ARGO, ARGO_L),
        ("Synced", "dérive annulée", GREEN, GREEN_L),
    ]
    fw, fgap = 220, 30
    fx0 = (W - (4*fw + 3*fgap)) / 2
    for i, (title, desc, c, cl) in enumerate(flow):
        x = fx0 + i*(fw+fgap)
        b += box(x, 250, fw, 80, cl, c, 12)
        b += text(x+fw/2, 282, title, 14, c, "bold")
        b += text(x+fw/2, 304, desc, 10.5, INK)
        if i < 3:
            b += arrow(x+fw+2, 290, x+fw+fgap-4, 290, MUTED, 3)

    b += text(W/2, 376, "Avec selfHeal activé, toute modification hors Git est automatiquement annulée : Git fait foi.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 5. App of Apps / multi-environnements
# ============================================================
def illu_app_of_apps():
    W, H = 980, 400
    b = DEFS
    b += text(W/2, 34, "Organiser à l'échelle : le motif App of Apps", 20, INK, "bold")
    b += text(W/2, 58, "Une Application racine qui référence d'autres Applications", 12, MUTED)

    # root
    b += box(380, 84, 220, 70, ARGO_L, ARGO, 12)
    b += text(490, 112, "App racine", 14, ARGO, "bold")
    b += text(490, 134, "root-app (dans Git)", 10, MUTED)

    children = [
        ("nginx", "frontend", GREEN, GREEN_L, 90),
        ("backend", "API", BLUE, BLUE_L, 350),
        ("monitoring", "Prometheus", PURPLE, PURPLE_L, 610),
        ("infra", "ingress, cert", TEAL, TEAL_L, 830),
    ]
    for name, role, c, cl, x in children:
        b += arrow(490, 154, x+75, 235, ARGO, 2.5)
        b += box(x, 240, 150, 90, cl, c, 12)
        b += text(x+75, 270, name, 14, c, "bold")
        b += text(x+75, 292, role, 11, MUTED)
        b += text(x+75, 314, "Application", 9.5, MUTED)

    b += text(W/2, 376, "On gère des dizaines d'apps et plusieurs environnements (dev/staging/prod) de façon déclarative, depuis Git.",
              11, MUTED)
    return svg(W, H, b)


def main():
    illus = {
        "01-push-pull.svg":    illu_push_pull(),
        "02-loop.svg":         illu_loop(),
        "03-application.svg":  illu_application(),
        "04-sync.svg":         illu_sync(),
        "05-app-of-apps.svg":  illu_app_of_apps(),
    }
    for name, content in illus.items():
        (IMG / name).write_text(content, encoding="utf-8")
        print(f"  + img/{name}")
    print(f"\n{len(illus)} illustrations générées dans {IMG}")


if __name__ == "__main__":
    main()
