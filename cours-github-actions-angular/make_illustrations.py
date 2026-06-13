#!/usr/bin/env python3
"""Génère les illustrations SVG du cours GitHub Actions (vectoriel, net à l'impression)."""
from pathlib import Path

IMG = Path(__file__).parent / "img"
IMG.mkdir(exist_ok=True)

# ---- Palette ----
INK     = "#1f2328"   # texte foncé
MUTED   = "#57606a"   # texte secondaire
LINE    = "#d0d7de"   # bordures claires
GHA     = "#2088ff"   # bleu GitHub Actions
GHA_DK  = "#0969da"
GREEN   = "#1a7f37"
GREEN_L = "#dafbe1"
PURPLE  = "#8250df"
PURPLE_L= "#fbefff"
ORANGE  = "#bc4c00"
ORANGE_L= "#fff1e5"
BLUE_L  = "#ddf4ff"
GREY_L  = "#f6f8fa"
DARK    = "#24292e"
YELLOW_L= "#fff8c5"

FONT = "font-family='DejaVu Sans, Segoe UI, sans-serif'"


def svg(w, h, body, bg="#ffffff"):
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
        f"viewBox='0 0 {w} {h}'>"
        f"<rect width='{w}' height='{h}' rx='10' fill='{bg}'/>"
        f"{body}</svg>"
    )


def box(x, y, w, h, fill, stroke, r=10, sw=2):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' "
            f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, fill=INK, weight="normal", anchor="middle"):
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill}' "
            f"font-weight='{weight}' text-anchor='{anchor}' {FONT}>{esc(s)}</text>")


def arrow(x1, y1, x2, y2, color=MUTED, sw=2.5, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' marker-end='url(#arr-{color.lstrip('#')})' {d}/>")


def marker(color):
    return (f"<marker id='arr-{color.lstrip('#')}' viewBox='0 0 10 10' refX='9' refY='5' "
            f"markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0 L10 5 L0 10 z' fill='{color}'/></marker>")


DEFS = ("<defs>" + marker(MUTED) + marker(GHA) + marker(GREEN) + marker(PURPLE)
        + marker(ORANGE) + marker(GHA_DK) + "</defs>")


def card(x, y, w, h, title, sub, fill, stroke, icon=""):
    """Carte avec titre + sous-titre."""
    s = box(x, y, w, h, fill, stroke)
    s += text(x + w/2, y + (h/2 - 4 if sub else h/2 + 5), title, 15, INK, "bold")
    if sub:
        s += text(x + w/2, y + h/2 + 16, sub, 11, MUTED)
    if icon:
        s += text(x + 22, y + h/2 + 7, icon, 20)
    return s


# ============================================================
# 1. Vue d'ensemble CI/CD
# ============================================================
def illu_overview():
    W, H = 1080, 360
    b = DEFS
    b += text(W/2, 34, "Le pipeline CI/CD : du commit au serveur en production", 19, INK, "bold")

    y = 110
    steps = [
        ("Développeur", "git push", BLUE_L, GHA),
        ("Dépôt GitHub", "événement", GREY_L, LINE),
        ("GitHub Actions", "runner Ubuntu", BLUE_L, GHA),
        ("Registry GHCR", "image Docker", PURPLE_L, PURPLE),
        ("Serveur", "conteneur en prod", GREEN_L, GREEN),
    ]
    bw, bh, gap = 180, 90, 30
    x = (W - (len(steps)*bw + (len(steps)-1)*gap)) / 2
    for i, (t, s, f, st) in enumerate(steps):
        cx = x + i*(bw+gap)
        b += box(cx, y, bw, bh, f, st)
        b += text(cx+bw/2, y+38, t, 14, INK, "bold")
        b += text(cx+bw/2, y+62, s, 11, MUTED)
        if i < len(steps)-1:
            ax = cx+bw+4
            b += arrow(ax, y+bh/2, ax+gap-8, y+bh/2, GHA, 3)

    # bande étapes internes
    yy = 255
    b += text(W/2, yy-8, "Ce que GitHub Actions exécute automatiquement", 13, MUTED, "bold")
    inner = ["Checkout", "npm ci", "ng build", "docker build", "smoke test", "docker push", "ssh deploy"]
    iw, ig = 128, 14
    ix = (W - (len(inner)*iw + (len(inner)-1)*ig)) / 2
    for i, t in enumerate(inner):
        cx = ix + i*(iw+ig)
        b += box(cx, yy, iw, 44, DARK, DARK, 8)
        b += text(cx+iw/2, yy+28, t, 12, "#ffffff", "bold")
        if i < len(inner)-1:
            b += arrow(cx+iw+1, yy+22, cx+iw+ig-3, yy+22, "#8b949e", 2)
    return svg(W, H, b)


# ============================================================
# 2. Anatomie d'un workflow (Workflow > Job > Step > Runner)
# ============================================================
def illu_anatomy():
    W, H = 1080, 470
    b = DEFS
    b += text(W/2, 34, "Anatomie d'un workflow GitHub Actions", 19, INK, "bold")
    b += text(W/2, 56, "Workflow  ⊃  Jobs  ⊃  Steps  —  chaque job tourne sur un runner isolé", 12, MUTED)

    # Workflow (cadre externe)
    b += box(40, 80, W-80, H-120, GREY_L, GHA, 14, 2.5)
    b += text(64, 108, "Workflow — .github/workflows/deploy.yml", 15, GHA_DK, "bold", "start")
    b += text(W-64, 108, "on: push", 12, MUTED, "normal", "end")

    # Job 1
    jx, jy, jw, jh = 70, 130, 440, 290
    b += box(jx, jy, jw, jh, "#ffffff", PURPLE, 12)
    b += text(jx+18, jy+28, "Job : build", 14, PURPLE, "bold", "start")
    b += text(jx+jw-14, jy+28, "runs-on: ubuntu-latest", 10, MUTED, "normal", "end")
    steps1 = ["uses: actions/checkout@v4", "uses: actions/setup-node@v4",
              "run: npm ci", "run: npm run build", "run: docker build ..."]
    for i, s in enumerate(steps1):
        sy = jy+48 + i*44
        b += box(jx+18, sy, jw-36, 34, GREY_L, LINE, 7)
        b += text(jx+30, sy+22, f"Step {i+1}", 10, PURPLE, "bold", "start")
        b += text(jx+96, sy+22, s, 11.5, INK, "normal", "start")

    # Job 2
    j2x = 570
    b += box(j2x, jy, jw, jh, "#ffffff", GREEN, 12)
    b += text(j2x+18, jy+28, "Job : deploy", 14, GREEN, "bold", "start")
    b += text(j2x+jw-14, jy+28, "needs: build", 10, MUTED, "normal", "end")
    steps2 = ["if: github.ref == 'refs/heads/main'", "uses: appleboy/ssh-action",
              "ssh → docker login", "ssh → docker pull", "ssh → docker run"]
    for i, s in enumerate(steps2):
        sy = jy+48 + i*44
        b += box(j2x+18, sy, jw-36, 34, GREY_L, LINE, 7)
        b += text(j2x+30, sy+22, f"Step {i+1}", 10, GREEN, "bold", "start")
        b += text(j2x+96, sy+22, s, 11.5, INK, "normal", "start")

    # flèche needs entre jobs
    b += arrow(jx+jw+2, jy+jh/2, j2x-4, jy+jh/2, MUTED, 3)
    b += text((jx+jw+j2x)/2, jy+jh/2-10, "needs", 11, MUTED, "bold")
    return svg(W, H, b)


# ============================================================
# 3. Les événements déclencheurs
# ============================================================
def illu_events():
    W, H = 1000, 380
    b = DEFS
    b += text(W/2, 34, "Qu'est-ce qui déclenche un workflow ?  ( on: )", 19, INK, "bold")

    events = [
        ("push", "un commit poussé\nsur main / develop", ORANGE_L, ORANGE),
        ("pull_request", "une PR ouverte\nou mise à jour", BLUE_L, GHA),
        ("schedule", "cron — ex. tous\nles jours à 2h", PURPLE_L, PURPLE),
        ("workflow_dispatch", "bouton manuel\ndans l'onglet Actions", GREEN_L, GREEN),
    ]
    bw, bh = 230, 64
    x0, y0, gap = 60, 90, 18
    for i, (name, desc, f, st) in enumerate(events):
        cy = y0 + i*(bh+gap)
        b += box(x0, cy, bw, bh, f, st)
        b += text(x0+18, cy+28, name, 14, INK, "bold", "start")
        for k, ln in enumerate(desc.split("\n")):
            b += text(x0+18, cy+45+k*14, ln, 10.5, MUTED, "normal", "start")
        b += arrow(x0+bw+2, cy+bh/2, 560, 200, st, 2.5)

    # Workflow cible
    b += box(560, 150, 360, 110, DARK, DARK, 14)
    b += text(740, 188, "Workflow exécuté", 17, "#ffffff", "bold")
    b += text(740, 214, "GitHub provisionne un runner,", 12, "#c9d1d9")
    b += text(740, 232, "clone le repo et lance les jobs", 12, "#c9d1d9")

    b += text(W/2, 348, "On peut aussi filtrer par chemin (paths:) — ex. ne builder que si quickbite-frontend/ change",
              11.5, MUTED)
    return svg(W, H, b)


# ============================================================
# 4. Flux des 3 jobs (build -> push -> deploy)
# ============================================================
def illu_jobs_flow():
    W, H = 1080, 430
    b = DEFS
    b += text(W/2, 34, "Le pipeline en 3 jobs enchaînés (needs)", 19, INK, "bold")

    jobs = [
        ("build", "Build Angular + Docker",
         ["checkout", "setup-node", "npm ci", "npm run build", "docker build (load)", "smoke test HTTP 200"],
         GHA, BLUE_L, "sur chaque push & PR"),
        ("push-image", "Publier l'image",
         ["docker login ghcr.io", "metadata-action (tags)", "docker build --push", "tags: sha · branch · latest"],
         PURPLE, PURPLE_L, "if: main ou develop"),
        ("deploy", "Déployer sur le serveur",
         ["ssh-action → serveur", "docker login + pull", "docker rm -f ancien", "docker run nouveau", "vérifier State.Running"],
         GREEN, GREEN_L, "if: main uniquement"),
    ]
    jw, gap = 320, 40
    x0 = (W - (3*jw + 2*gap)) / 2
    y0, jh = 80, 290
    for i, (title, sub, steps, c, fl, cond) in enumerate(jobs):
        x = x0 + i*(jw+gap)
        b += box(x, y0, jw, jh, "#ffffff", c, 12, 2.5)
        b += box(x, y0, jw, 50, fl, fl, 12)
        b += text(x+jw/2, y0+24, title, 15, INK, "bold")
        b += text(x+jw/2, y0+42, sub, 11, MUTED)
        for k, s in enumerate(steps):
            sy = y0+68 + k*36
            b += box(x+16, sy, jw-32, 28, GREY_L, LINE, 6)
            b += text(x+26, sy+19, f"› {s}", 11, INK, "normal", "start")
        # bandeau condition
        b += box(x+16, y0+jh+12, jw-32, 30, YELLOW_L, "#d4a72c", 7)
        b += text(x+jw/2, y0+jh+31, cond, 11, ORANGE, "bold")
        if i < 2:
            ax = x+jw+4
            b += arrow(ax, y0+jh/2, ax+gap-8, y0+jh/2, c, 3.5)
            b += text(ax+gap/2-2, y0+jh/2-10, "needs", 10.5, MUTED, "bold")
    return svg(W, H, b)


# ============================================================
# 5. Déploiement SSH sur le serveur
# ============================================================
def illu_ssh_deploy():
    W, H = 1040, 380
    b = DEFS
    b += text(W/2, 34, "Le déploiement SSH : du runner GitHub au serveur", 19, INK, "bold")

    # Runner
    b += box(60, 90, 300, 220, BLUE_L, GHA, 14)
    b += text(210, 120, "Runner GitHub Actions", 15, GHA_DK, "bold")
    runner = ["appleboy/ssh-action@v1", "host  = secrets.DEPLOY_HOST",
              "user  = secrets.DEPLOY_USER", "key   = secrets.DEPLOY_SSH_KEY"]
    for i, s in enumerate(runner):
        b += box(80, 140+i*40, 260, 30, "#ffffff", LINE, 7)
        b += text(94, 160+i*40, s, 11, INK, "normal", "start")

    # Tunnel SSH
    b += arrow(370, 200, 660, 200, GREEN, 4)
    b += box(440, 168, 150, 40, GREEN_L, GREEN, 8)
    b += text(515, 193, "SSH (clé)", 13, GREEN, "bold")

    # Serveur
    b += box(680, 90, 300, 220, GREEN_L, GREEN, 14)
    b += text(830, 120, "Serveur de prod", 15, GREEN, "bold")
    srv = ["docker login ghcr.io", "docker pull ...:latest",
           "docker rm -f ancien", "docker run -p 80:80 ...", "OK — State.Running == true"]
    for i, s in enumerate(srv):
        b += box(700, 138+i*32, 260, 26, "#ffffff", LINE, 7)
        b += text(714, 156+i*32, s, 11, INK, "normal", "start")

    b += text(W/2, 352, "La clé privée vit dans les Secrets GitHub, jamais dans le code. "
              "Le runner s'auto-détruit après le job.", 11.5, MUTED)
    return svg(W, H, b)


# ============================================================
# 6. Secrets & sécurité
# ============================================================
def illu_secrets():
    W, H = 1000, 360
    b = DEFS
    b += text(W/2, 34, "Les secrets : injectés au runtime, jamais exposés", 19, INK, "bold")

    # Coffre
    b += box(70, 90, 300, 220, "#fff8f0", ORANGE, 14)
    b += text(220, 120, "Settings › Secrets", 15, ORANGE, "bold")
    secrets = ["DEPLOY_HOST", "DEPLOY_USER", "DEPLOY_SSH_KEY", "GITHUB_TOKEN (auto)"]
    for i, s in enumerate(secrets):
        b += box(92, 142+i*38, 256, 28, "#ffffff", "#f0c0a0", 7)
        b += text(106, 161+i*38, "•••  " + s, 11.5, INK, "normal", "start")

    b += arrow(370, 200, 620, 200, ORANGE, 3.5)
    b += text(495, 188, "${{ secrets.X }}", 12, ORANGE, "bold")

    # Workflow
    b += box(640, 90, 300, 220, DARK, DARK, 14)
    b += text(790, 120, "Workflow", 15, "#ffffff", "bold")
    code = ['with:', '  host: ${{ secrets.DEPLOY_HOST }}',
            '  key:  ${{ secrets.DEPLOY_SSH_KEY }}', '', 'logs › valeur masquée : ***']
    for i, s in enumerate(code):
        col = "#7ee787" if s.startswith("logs") else "#c9d1d9"
        b += text(660, 158+i*30, s, 11.5, col, "normal", "start")

    b += text(W/2, 344, "Dans les logs, GitHub remplace automatiquement toute valeur de secret par ***",
              11.5, MUTED)
    return svg(W, H, b)


def main():
    illus = {
        "01-overview.svg":   illu_overview(),
        "02-anatomy.svg":    illu_anatomy(),
        "03-events.svg":     illu_events(),
        "04-jobs-flow.svg":  illu_jobs_flow(),
        "05-ssh-deploy.svg": illu_ssh_deploy(),
        "06-secrets.svg":    illu_secrets(),
    }
    for name, content in illus.items():
        (IMG / name).write_text(content, encoding="utf-8")
        print(f"  + img/{name}")
    print(f"\n{len(illus)} illustrations générées dans {IMG}")


if __name__ == "__main__":
    main()
