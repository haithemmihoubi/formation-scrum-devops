#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère des schémas SVG (concepts du cours) dans img/diagrams/.
Charte : bleu #0B3D62, jaune #F5B301, accents."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "diagrams")
os.makedirs(OUT, exist_ok=True)

BLUE = "#0B3D62"; YEL = "#F5B301"; D2 = "#14507A"; GREY = "#5B6770"
GREEN = "#1E9E5A"; RED = "#C0392B"; PURPLE = "#6C3FB5"; LIGHT = "#F4F7FA"

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, Arial, sans-serif">'

def box(x, y, w, h, fill, text, tcolor="#fff", fs=15, rx=8, sub=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2-4}" fill="{tcolor}" font-size="{fs}" font-weight="bold" text-anchor="middle">{text}</text>'
        s += f'<text x="{x+w/2}" y="{y+h/2+14}" fill="{tcolor}" font-size="{fs-3}" text-anchor="middle">{sub}</text>'
    else:
        s += f'<text x="{x+w/2}" y="{y+h/2+5}" fill="{tcolor}" font-size="{fs}" font-weight="bold" text-anchor="middle">{text}</text>'
    return s

def arrow(x1, y1, x2, y2, color=YEL, w=3):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#a)"/>')

DEFS = f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 Z" fill="{YEL}"/></marker></defs>'

def save(name, w, h, body):
    svg = HEAD.format(w=w, h=h) + DEFS + body + "</svg>"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ->", name)


# 1. Cascade vs Agile
def waterfall_vs_agile():
    b = f'<text x="20" y="24" font-size="16" font-weight="bold" fill="{BLUE}">Cascade : la valeur arrive à la fin</text>'
    phases = ["Besoins", "Concept.", "Code", "Tests", "Livraison"]
    x = 20
    for i, p in enumerate(phases):
        b += box(x, 40, 110, 46, BLUE if i < 4 else GREEN, p, fs=13)
        if i < 4:
            b += arrow(x+110, 63, x+135, 63)
        x += 135
    b += f'<text x="20" y="150" font-size="16" font-weight="bold" fill="{BLUE}">Agile : de la valeur à chaque itération</text>'
    x = 20
    for i in range(5):
        b += box(x, 166, 110, 46, GREEN, f"Itér. {i+1}", sub="valeur ✓", fs=13)
        if i < 4:
            b += arrow(x+110, 189, x+135, 189)
        x += 135
    save("waterfall-vs-agile.svg", 720, 230, b)


# 2. Boucle DevOps
def devops_loop():
    steps = ["PLAN", "CODE", "BUILD", "TEST", "RELEASE", "DEPLOY", "OPERATE", "MONITOR"]
    b = ""
    x = 20
    for i, s in enumerate(steps):
        col = BLUE if i < 4 else D2
        b += box(x, 70, 78, 46, col, s, fs=12)
        if i < len(steps)-1:
            b += arrow(x+78, 93, x+86, 93)
        x += 86
    b += f'<path d="M60,70 C60,30 {20+86*7+39},30 {20+86*7+39},70" fill="none" stroke="{YEL}" stroke-width="3" marker-end="url(#a)"/>'
    b += f'<text x="{(720)/2}" y="22" font-size="13" fill="{GREY}" text-anchor="middle">boucle de feedback continue</text>'
    save("devops-loop.svg", 760, 140, b)


# 3. Conteneur vs VM
def container_vs_vm():
    b = f'<text x="20" y="22" font-size="15" font-weight="bold" fill="{BLUE}">Machines virtuelles</text>'
    b += box(20, 35, 150, 40, "#9aa6b2", "App A", fs=13) + box(180, 35, 150, 40, "#9aa6b2", "App B", fs=13)
    b += box(20, 78, 150, 34, "#c3cdd8", "OS invité", "#1f2329", 12) + box(180, 78, 150, 34, "#c3cdd8", "OS invité", "#1f2329", 12)
    b += box(20, 115, 310, 32, D2, "Hyperviseur", fs=13)
    b += box(20, 150, 310, 30, BLUE, "OS hôte + Matériel", fs=12)
    b += f'<text x="175" y="205" font-size="12" fill="{GREY}" text-anchor="middle">lourd · démarre en minutes</text>'

    ox = 390
    b += f'<text x="{ox}" y="22" font-size="15" font-weight="bold" fill="{BLUE}">Conteneurs</text>'
    b += box(ox, 35, 150, 40, GREEN, "App A", fs=13) + box(ox+160, 35, 150, 40, GREEN, "App B", fs=13)
    b += box(ox, 82, 310, 30, D2, "Moteur Docker", fs=13)
    b += box(ox, 117, 310, 30, BLUE, "OS hôte (noyau partagé)", fs=12)
    b += box(ox, 150, 310, 30, BLUE, "Matériel", fs=12)
    b += f'<text x="{ox+155}" y="205" font-size="12" fill="{GREY}" text-anchor="middle">léger · démarre en millisecondes</text>'
    save("container-vs-vm.svg", 720, 220, b)


# 4. Pipeline CI/CD
def cicd():
    steps = [("Commit", BLUE), ("Build", D2), ("Tests", D2), ("Image", D2), ("Deploy", GREEN)]
    b = ""
    x = 20
    for i, (s, c) in enumerate(steps):
        b += box(x, 50, 120, 56, c, s, fs=14)
        if i < len(steps)-1:
            b += arrow(x+120, 78, x+148, 78)
        x += 148
    b += f'<text x="20" y="30" font-size="14" font-weight="bold" fill="{BLUE}">À chaque push : tout est automatisé</text>'
    b += f'<text x="20" y="135" font-size="12" fill="{RED}">✗ tests rouges → fusion bloquée</text>'
    save("cicd-pipeline.svg", 770, 150, b)


# 5. Architecture Kubernetes
def k8s():
    b = f'<text x="20" y="22" font-size="15" font-weight="bold" fill="{BLUE}">Architecture Kubernetes</text>'
    b += box(20, 35, 680, 44, BLUE, "Control Plane : API Server · Scheduler · Controllers · etcd", fs=13)
    b += arrow(360, 79, 360, 100, color=YEL)
    nx = 40
    for i in range(3):
        b += box(nx, 105, 200, 90, LIGHT, "", rx=8)
        b += f'<text x="{nx+100}" y="125" font-size="13" font-weight="bold" fill="{BLUE}" text-anchor="middle">Node {i+1}</text>'
        b += box(nx+18, 135, 75, 46, GREEN, "Pod", fs=12) + box(nx+105, 135, 75, 46, GREEN, "Pod", fs=12)
        nx += 230
    save("k8s-arch.svg", 720, 210, b)


# 6. Structure d'un JWT
def jwt():
    b = f'<text x="20" y="24" font-size="15" font-weight="bold" fill="{BLUE}">Un JWT = 3 parties (signé, pas chiffré)</text>'
    parts = [("HEADER", "algorithme", "#e06d2f"), ("PAYLOAD", "claims : sub, roles, exp", PURPLE), ("SIGNATURE", "intégrité", GREEN)]
    x = 20
    widths = [150, 320, 170]
    for (t, s, c), w in zip(parts, widths):
        b += box(x, 45, w, 60, c, t, sub=s, fs=14)
        if w != widths[-1]:
            b += f'<text x="{x+w+4}" y="82" font-size="22" fill="{GREY}">.</text>'
        x += w + 18
    b += f'<text x="20" y="135" font-size="12" fill="{RED}">⚠ le payload est lisible : aucune donnée sensible dedans</text>'
    save("jwt-structure.svg", 720, 150, b)


# 7. Flow OAuth2 / OIDC
def oauth():
    b = f'<text x="20" y="22" font-size="15" font-weight="bold" fill="{BLUE}">OAuth2 / OIDC — Authorization Code + PKCE</text>'
    actors = [("Utilisateur", 20), ("Client", 200), ("Auth Server", 380), ("API", 560)]
    for name, x in actors:
        b += box(x, 40, 140, 40, BLUE, name, fs=13)
    y = 110
    flows = [
        ("Utilisateur → Client : je veux me connecter", BLUE),
        ("Client → Auth Server : redirige vers login", D2),
        ("Auth Server → Client : code d'autorisation", GREEN),
        ("Client → Auth Server : code + PKCE → tokens", GREEN),
        ("Client → API : appel avec access token", PURPLE),
    ]
    for i, (t, c) in enumerate(flows):
        b += f'<circle cx="34" cy="{y+i*26-4}" r="9" fill="{c}"/><text x="34" y="{y+i*26}" font-size="11" fill="#fff" text-anchor="middle">{i+1}</text>'
        b += f'<text x="52" y="{y+i*26}" font-size="13" fill="#1f2329">{t}</text>'
    save("oauth-flow.svg", 720, 260, b)


# 8. AuthN vs AuthZ
def authn_authz():
    b = box(20, 30, 330, 110, LIGHT, "", rx=10)
    b += f'<text x="185" y="58" font-size="16" font-weight="bold" fill="{BLUE}" text-anchor="middle">Authentification</text>'
    b += f'<text x="185" y="84" font-size="13" fill="#1f2329" text-anchor="middle">« Qui es-tu ? »</text>'
    b += f'<text x="185" y="110" font-size="12" fill="{GREY}" text-anchor="middle">identité · mot de passe, token</text>'
    b += arrow(355, 85, 385, 85)
    b += box(390, 30, 330, 110, LIGHT, "", rx=10)
    b += f'<text x="555" y="58" font-size="16" font-weight="bold" fill="{BLUE}" text-anchor="middle">Autorisation</text>'
    b += f'<text x="555" y="84" font-size="13" fill="#1f2329" text-anchor="middle">« As-tu le droit ? »</text>'
    b += f'<text x="555" y="110" font-size="12" fill="{GREY}" text-anchor="middle">permissions · rôles</text>'
    save("authn-authz.svg", 740, 160, b)


# 9. Boucle de feedback Agile
def feedback():
    cx = [120, 360, 600]; labels = ["Construire", "Mesurer", "Apprendre"]; cols = [BLUE, D2, GREEN]
    b = ""
    for x, l, c in zip(cx, labels, cols):
        b += box(x-90, 50, 180, 56, c, l, fs=16)
    b += arrow(210, 78, 268, 78) + arrow(450, 78, 508, 78)
    b += f'<path d="M600,106 C600,160 120,160 120,108" fill="none" stroke="{YEL}" stroke-width="3" marker-end="url(#a)"/>'
    b += f'<text x="360" y="150" font-size="13" fill="{GREY}" text-anchor="middle">plus la boucle est courte, moins l\'erreur coûte cher</text>'
    save("feedback-loop.svg", 720, 175, b)


for fn in [waterfall_vs_agile, devops_loop, container_vs_vm, cicd, k8s, jwt, oauth, authn_authz, feedback]:
    fn()
print("Schémas générés.")
