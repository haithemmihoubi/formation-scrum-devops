#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les schémas SVG de la présentation « CI/CD & GitHub Actions ».
Charte : bleu #0B3D62, jaune #F5B301, vert succès, rouge alerte."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

BLUE = "#0B3D62"; YEL = "#F5B301"; D2 = "#14507A"; GREY = "#5B6770"
GREEN = "#1E9E5A"; RED = "#C0392B"; PURPLE = "#6C3FB5"; LIGHT = "#F4F7FA"
GHBLUE = "#2088ff"

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, Arial, sans-serif">'


def box(x, y, w, h, fill, text, tcolor="#fff", fs=15, rx=8, sub=None, sfs=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2-4}" fill="{tcolor}" font-size="{fs}" font-weight="bold" text-anchor="middle">{text}</text>'
        s += f'<text x="{x+w/2}" y="{y+h/2+15}" fill="{tcolor}" font-size="{sfs or fs-3}" text-anchor="middle">{sub}</text>'
    else:
        s += f'<text x="{x+w/2}" y="{y+h/2+5}" fill="{tcolor}" font-size="{fs}" font-weight="bold" text-anchor="middle">{text}</text>'
    return s


def txt(x, y, s, fill=BLUE, fs=15, bold=False, anchor="start"):
    fw = ' font-weight="bold"' if bold else ''
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{fs}"{fw} text-anchor="{anchor}">{s}</text>'


def arrow(x1, y1, x2, y2, color=YEL, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#a)"/>'


DEFS = (f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" '
        f'markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 Z" fill="{YEL}"/></marker>'
        f'<marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" '
        f'markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 Z" fill="{GREEN}"/></marker></defs>')


def save(name, w, h, body):
    svg = HEAD.format(w=w, h=h) + DEFS + body + "</svg>"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ->", name)


# 1. Sans CI/CD vs Avec CI/CD ------------------------------------------------
def sans_vs_avec():
    b = txt(20, 26, "SANS CI/CD — intégration tardive, douloureuse", RED, 16, True)
    # plusieurs devs travaillent isolés, big bang merge
    for i, p in enumerate(["Dev A", "Dev B", "Dev C"]):
        b += box(20, 44 + i * 40, 110, 32, GREY, p, fs=12)
    b += arrow(130, 100, 230, 100, RED)
    b += box(230, 70, 150, 60, RED, "MERGE GÉANT", sub="conflits, bugs", fs=13)
    b += arrow(380, 100, 470, 100, RED)
    b += box(470, 70, 230, 60, "#7B241C", "Déploiement rare & stressant",
             sub="manuel · « ça marche chez moi »", fs=12, sfs=10)

    b += txt(20, 196, "AVEC CI/CD — petits lots, intégrés en continu", GREEN, 16, True)
    x = 20
    for i in range(4):
        b += box(x, 214, 92, 40, GREEN, f"commit {i+1}", sub="testé auto", fs=11, sfs=9)
        if i < 3:
            b += arrow(x + 92, 234, x + 120, 234, GREEN)
        x += 120
    b += arrow(x, 234, x + 26, 234, GREEN)
    b += box(x + 26, 210, 174, 48, BLUE, "Prod, plusieurs fois/jour",
             sub="auto · fiable · sans stress", fs=12, sfs=10)
    save("sans-vs-avec.svg", 720, 270, b)


# 2. Coût d'un bug selon le moment de détection -----------------------------
def cout_du_bug():
    b = txt(360, 24, "Plus un bug est détecté tard, plus il coûte cher", BLUE, 16, True, "middle")
    # axes
    b += f'<line x1="70" y1="240" x2="690" y2="240" stroke="{GREY}" stroke-width="2"/>'
    b += f'<line x1="70" y1="40" x2="70" y2="240" stroke="{GREY}" stroke-width="2"/>'
    b += txt(70, 262, "Code", GREY, 12, False, "middle")
    stages = [("Code", 1, 50), ("CI / Tests", 5, 100), ("Recette", 25, 160), ("Production", 100, 200)]
    x = 130
    for name, cost, h in stages:
        col = GREEN if cost <= 5 else (YEL if cost <= 25 else RED)
        b += f'<rect x="{x}" y="{240-h}" width="90" height="{h}" rx="6" fill="{col}"/>'
        b += txt(x + 45, 240 - h - 8, f"x{cost}", BLUE, 14, True, "middle")
        b += txt(x + 45, 258, name, GREY, 12, False, "middle")
        x += 150
    b += txt(690, 230, "coût", GREY, 11, False, "end")
    b += txt(95, 50, "↑", GREY, 14)
    save("cout-du-bug.svg", 720, 280, b)


# 3. Boucle de valeur business ----------------------------------------------
def value_loop():
    cx, cy, r = 360, 150, 96
    b = ""
    pts = [("Idée", -90), ("Build", -18), ("Livré", 54), ("Mesuré", 126), ("Appris", 198)]
    import math
    coords = []
    for label, ang in pts:
        a = math.radians(ang)
        x = cx + r * math.cos(a); y = cy + r * math.sin(a)
        coords.append((x, y, label))
    for i, (x, y, label) in enumerate(coords):
        col = YEL if label == "Livré" else BLUE
        tc = BLUE if label == "Livré" else "#fff"
        b += f'<circle cx="{x}" cy="{y}" r="34" fill="{col}"/>'
        b += txt(x, y + 5, label, tc, 13, True, "middle")
    # arcs between
    for i in range(len(coords)):
        x1, y1, _ = coords[i]
        x2, y2, _ = coords[(i + 1) % len(coords)]
        b += arrow(x1 + (x2 - x1) * 0.28, y1 + (y2 - y1) * 0.28,
                   x1 + (x2 - x1) * 0.72, y1 + (y2 - y1) * 0.72, YEL, 3)
    b += txt(cx, cy - 6, "Boucle", BLUE, 15, True, "middle")
    b += txt(cx, cy + 14, "de valeur", BLUE, 15, True, "middle")
    b += txt(cx, 290, "CI/CD raccourcit le tour de boucle → on apprend et on gagne plus vite",
             GREY, 12, False, "middle")
    save("value-loop.svg", 720, 305, b)


# 4. Anatomie GitHub Actions : Workflow > Job > Step ------------------------
def gha_anatomy():
    b = txt(20, 24, "Workflow = 1 fichier .yml dans .github/workflows/", GHBLUE, 15, True)
    # cadre du workflow
    b += f'<rect x="20" y="36" width="680" height="258" rx="12" fill="none" stroke="{GHBLUE}" stroke-width="2.5"/>'
    b += txt(34, 58, "WORKFLOW  « CI/CD »", GHBLUE, 14, True)
    # déclencheur
    b += box(540, 44, 150, 30, YEL, "on: push", tcolor=BLUE, fs=12)
    # JOB build
    b += f'<rect x="34" y="80" width="316" height="200" rx="10" fill="{LIGHT}" stroke="{D2}" stroke-width="1.6"/>'
    b += txt(48, 102, "JOB  build", BLUE, 13, True)
    b += txt(48, 120, "runs-on: ubuntu-latest", GREY, 10)
    sy = 132
    for st in ["step: checkout", "step: setup-node", "step: npm test", "step: npm build"]:
        b += box(48, sy, 286, 30, BLUE, st, fs=11)
        sy += 36
    # JOB deploy
    b += f'<rect x="370" y="80" width="316" height="200" rx="10" fill="{LIGHT}" stroke="{D2}" stroke-width="1.6"/>'
    b += txt(384, 102, "JOB  deploy", BLUE, 13, True)
    b += txt(384, 120, "needs: build", GREY, 10)
    sy = 132
    for st in ["step: build image", "step: push registry", "step: deploy SSH"]:
        b += box(384, sy, 286, 30, GREEN, st, fs=11)
        sy += 36
    # flèche build -> deploy
    b += arrow(350, 180, 370, 180, YEL)
    save("gha-anatomy.svg", 720, 305, b)


# 5. Flux d'événements GitHub Actions ---------------------------------------
def gha_events():
    b = txt(360, 26, "Un événement déclenche un workflow sur un runner", BLUE, 15, True, "middle")
    events = [("push", "un commit poussé"), ("pull_request", "une PR ouverte/maj"),
              ("schedule", "cron (ex: nuit)"), ("workflow_dispatch", "manuel (bouton)")]
    y = 56
    cy = 56 + (len(events) - 1) * 58 / 2 + 20  # centre vertical des events
    for ev, desc in events:
        b += box(30, y, 190, 44, YEL, ev, tcolor=BLUE, fs=14, sub=desc, sfs=10)
        b += arrow(222, y + 22, 296, cy, YEL)
        y += 58
    b += box(300, cy - 40, 150, 80, GHBLUE, "GitHub Actions", sub="orchestrateur", fs=14, sfs=11)
    b += arrow(452, cy, 528, cy, YEL)
    b += box(530, cy - 40, 160, 80, BLUE, "Runner", sub="machine qui exécute", fs=14, sfs=11)
    b += txt(610, cy + 64, "ubuntu · windows · macos · self-hosted", GREY, 11, False, "middle")
    save("gha-events.svg", 720, y + 24, b)


# 6. Les briques (composants) GitHub Actions --------------------------------
def gha_components():
    comps = [
        ("Workflow", "le pipeline (1 fichier .yml)", BLUE),
        ("Event", "ce qui déclenche (push, PR…)", YEL),
        ("Job", "un groupe d'étapes, sur 1 runner", D2),
        ("Step", "une commande ou une action", GREEN),
        ("Action", "brique réutilisable (Marketplace)", PURPLE),
        ("Runner", "la machine d'exécution", GREY),
        ("Secret", "valeur chiffrée (token, clé SSH)", RED),
        ("Artifact", "fichier produit & partagé", "#B8860B"),
    ]
    b = ""
    x, y = 24, 24
    for i, (name, desc, col) in enumerate(comps):
        tc = BLUE if col == YEL else "#fff"
        b += box(x, y, 326, 56, col, name, tcolor=tc, fs=16, sub=desc, sfs=11)
        if i % 2 == 0:
            x += 346
        else:
            x = 24
            y += 70
    save("gha-components.svg", 720, 305, b)


# 7. Étapes d'un pipeline type ----------------------------------------------
def pipeline_stages():
    stages = [("Commit", GREY), ("Lint", BLUE), ("Test", BLUE), ("Build", D2),
              ("Scan sécu", PURPLE), ("Image", D2), ("Deploy", GREEN)]
    b = txt(360, 24, "Du commit à la prod — chaque étape garde la qualité", BLUE, 15, True, "middle")
    x = 16
    w = 90
    for i, (name, col) in enumerate(stages):
        b += box(x, 80, w, 56, col, name, fs=13)
        if i < len(stages) - 1:
            b += arrow(x + w, 108, x + w + 12, 108)
        x += w + 12
    b += txt(360, 175, "❌ pipeline rouge → on ne fusionne pas · ✅ vert → déployable",
             GREY, 12, False, "middle")
    save("pipeline-stages.svg", 720, 200, b)


# 7b. Pipeline vertical (pour slides de contenu, colonne étroite) ------------
def pipeline_vertical():
    stages = [("Commit", GREY, "le dev pousse"), ("Lint", BLUE, "style du code"),
              ("Test", BLUE, "tests auto"), ("Build", D2, "compilation"),
              ("Scan sécu", PURPLE, "vulnérabilités"), ("Image", D2, "Docker"),
              ("Deploy", GREEN, "→ production")]
    b = ""
    y = 14
    for i, (name, col, desc) in enumerate(stages):
        b += box(70, y, 220, 50, col, name, fs=16, sub=desc, sfs=11)
        if i < len(stages) - 1:
            b += arrow(180, y + 50, 180, y + 64, YEL if col != GREEN else GREEN)
        y += 64
    save("pipeline-vertical.svg", 360, y + 4, b)


# 8. Métriques DORA ---------------------------------------------------------
def dora():
    metrics = [
        ("Fréquence de déploiement", "à quelle vitesse on livre", GREEN, "↑"),
        ("Délai de livraison (Lead Time)", "commit → production", BLUE, "↓"),
        ("Taux d'échec de changement", "% de déploiements ratés", YEL, "↓"),
        ("MTTR", "temps de rétablissement", PURPLE, "↓"),
    ]
    b = txt(360, 26, "4 métriques DORA : mesurer l'impact business du CI/CD", BLUE, 15, True, "middle")
    y = 48
    for name, desc, col, arr in metrics:
        tc = BLUE if col == YEL else "#fff"
        b += box(40, y, 560, 50, col, "", fs=14)
        b += txt(60, y + 24, name, tc, 15, True)
        b += txt(60, y + 42, desc, tc, 11)
        b += txt(635, y + 33, arr, col, 30, True, "middle")
        y += 62
    save("dora.svg", 720, 305, b)


# 9. Exemple chiffré avant/après --------------------------------------------
def avant_apres():
    rows = [
        ("Fréquence de livraison", "1× / trimestre", "10× / jour"),
        ("Délai commit → prod", "3 semaines", "15 minutes"),
        ("Bugs détectés en prod", "fréquents", "rares (bloqués en CI)"),
        ("Retour arrière (rollback)", "heures, manuel", "1 clic, auto"),
        ("Stress des mises en prod", "élevé", "routine"),
    ]
    b = txt(360, 26, "Effet concret sur une équipe produit", BLUE, 16, True, "middle")
    b += box(40, 44, 280, 38, GREY, "Indicateur", fs=14)
    b += box(324, 44, 178, 38, RED, "Avant CI/CD", fs=14)
    b += box(506, 44, 178, 38, GREEN, "Avec CI/CD", fs=14)
    y = 86
    for ind, av, ap in rows:
        b += f'<rect x="40" y="{y}" width="280" height="38" fill="{LIGHT}" stroke="#d0d7de"/>'
        b += txt(54, y + 24, ind, BLUE, 12, True)
        b += f'<rect x="324" y="{y}" width="178" height="38" fill="#fdecea" stroke="#d0d7de"/>'
        b += txt(413, y + 24, av, "#7B241C", 12, False, "middle")
        b += f'<rect x="506" y="{y}" width="178" height="38" fill="#e8f6ee" stroke="#d0d7de"/>'
        b += txt(595, y + 24, ap, "#14633a", 12, False, "middle")
        y += 42
    save("avant-apres.svg", 720, 300, b)


if __name__ == "__main__":
    print("Génération des schémas CI/CD...")
    sans_vs_avec()
    cout_du_bug()
    value_loop()
    gha_anatomy()
    gha_events()
    gha_components()
    pipeline_stages()
    pipeline_vertical()
    dora()
    avant_apres()
    print("Terminé.")
