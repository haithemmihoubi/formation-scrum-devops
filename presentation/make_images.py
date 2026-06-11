#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les illustrations PNG du Chapitre 7 (Scrum) dans presentation/img/.
Schémas dessinés avec Pillow (pas de réseau). La charte reprend les couleurs
Solid Wall : bleu #0B3D62, jaune #F5B301.

Le diagramme du processus Scrum est rasterisé depuis presentation-pdf/img/scrum.svg
via ImageMagick (`convert`) s'il est disponible.
"""
import os
import math
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)

BLUE = (11, 61, 98)
YELLOW = (245, 179, 1)
D2 = (20, 80, 122)
GREY = (91, 103, 112)
GREEN = (30, 158, 90)
RED = (192, 57, 43)
LIGHT = (244, 247, 250)
WHITE = (255, 255, 255)
INK = (31, 35, 41)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_PATH, size)


def text_center(d, cx, cy, s, fnt, fill):
    bb = d.textbbox((0, 0), s, font=fnt)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1]), s, font=fnt, fill=fill)


def rounded(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, p1, p2, color, width=6, head=16):
    d.line([p1, p2], fill=color, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for s in (-1, 1):
        a = ang + s * math.radians(28)
        d.line([p2, (p2[0] - head * math.cos(a), p2[1] - head * math.sin(a))],
               fill=color, width=width)


def canvas(w, h, bg=WHITE):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def save(img, name):
    path = os.path.join(IMG, name)
    img.save(path, "PNG")
    print("  ->", name, img.size)


# ---------------------------------------------------------------------------
# 1. Processus empirique : Transparence / Inspection / Adaptation (cycle)
# ---------------------------------------------------------------------------
def empirisme():
    W, H = 1200, 780
    img, d = canvas(W, H, WHITE)
    text_center(d, W // 2, 40, "L'EMPIRISME EN SCRUM", font(34, True), BLUE)
    cx, cy, R = W // 2, 430, 215
    nodes = [
        ("TRANSPARENCE", "Rendre visible", -90, BLUE),
        ("INSPECTION", "Surveiller l'avancement", 30, D2),
        ("ADAPTATION", "Ajuster au plus tot", 150, GREEN),
    ]
    pts = []
    for _, _, ang, _ in nodes:
        a = math.radians(ang)
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    # fleches circulaires entre les noeuds
    for i in range(3):
        p1, p2 = pts[i], pts[(i + 1) % 3]
        v = (p2[0] - p1[0], p2[1] - p1[1])
        ln = math.hypot(*v)
        ux, uy = v[0] / ln, v[1] / ln
        arrow(d, (p1[0] + ux * 122, p1[1] + uy * 122),
              (p2[0] - ux * 122, p2[1] - uy * 122), YELLOW, width=8, head=22)
    for (title, sub, _, col), (x, y) in zip(nodes, pts):
        r = 118
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        text_center(d, x, y - 12, title, font(22, True), WHITE)
        text_center(d, x, y + 18, sub, font(15), (235, 240, 245))
    save(img, "empirisme.png")


# ---------------------------------------------------------------------------
# 2. Metaphore de la melee (rugby) - illustration stylisee
# ---------------------------------------------------------------------------
def melee():
    W, H = 1200, 720
    img, d = canvas(W, H, (224, 236, 226))
    # terrain
    d.rectangle([0, H - 150, W, H], fill=GREEN)
    for x in range(60, W, 160):
        d.line([(x, H - 150), (x, H)], fill=(255, 255, 255), width=3)
    # deux packs qui se font face (cercles = joueurs)
    def pack(cx, color):
        rows = [(-1, 0, 1), (-0.5, 0.5), (0,)]
        for ri, row in enumerate(rows):
            for off in row:
                x = cx + off * 92 + (ri * (1 if cx < W / 2 else -1)) * 64
                y = 330 + ri * 14 + abs(off) * 26
                r = 46
                d.ellipse([x - r, y - r, x + r, y + r], fill=color,
                          outline=WHITE, width=5)
        return
    pack(360, BLUE)
    pack(840, RED)
    # ballon au centre
    d.ellipse([W // 2 - 34, 440, W // 2 + 34, 500], fill=(120, 72, 40),
              outline=WHITE, width=4)
    text_center(d, W // 2, 70, "LA MELEE (SCRUM)", font(40, True), BLUE)
    text_center(d, W // 2, 120, "Cohesion et effort collectif pour avancer ensemble",
                font(23), GREY)
    save(img, "melee.png")


# ---------------------------------------------------------------------------
# 3. Cycle des releases : Release 0 -> 1 -> ... -> N
# ---------------------------------------------------------------------------
def release_cycle():
    W, H = 1200, 420
    img, d = canvas(W, H, WHITE)
    labels = [("Release 0", "Socle technique", GREY),
              ("Release 1", "1er increment", D2),
              ("Release 2", "increment", BLUE),
              ("...", "", GREEN),
              ("Release N", "Produit complet", GREEN)]
    n = len(labels)
    bw, bh, gap = 180, 150, 50
    total = n * bw + (n - 1) * gap
    x = (W - total) // 2
    y = 150
    for i, (t, s, col) in enumerate(labels):
        rounded(d, [x, y, x + bw, y + bh], 18, col)
        text_center(d, x + bw / 2, y + bh / 2 - 16, t, font(26, True), WHITE)
        if s:
            text_center(d, x + bw / 2, y + bh / 2 + 22, s, font(18), (235, 240, 245))
        if i < n - 1:
            arrow(d, (x + bw + 6, y + bh / 2), (x + bw + gap - 6, y + bh / 2),
                  YELLOW, width=8, head=20)
        x += bw + gap
    text_center(d, W // 2, 60, "ENCHAINEMENT CONTINU DES INCREMENTS", font(30, True), BLUE)
    save(img, "release_cycle.png")


# ---------------------------------------------------------------------------
# 4. Pipeline d'automatisation : Integration -> Build -> Packaging -> Deploy
# ---------------------------------------------------------------------------
def pipeline():
    W, H = 1200, 380
    img, d = canvas(W, H, WHITE)
    steps = [("Integration", D2), ("Build", BLUE), ("Packaging", GREEN), ("Deployment", YELLOW)]
    n = len(steps)
    bw, bh, gap = 230, 140, 60
    total = n * bw + (n - 1) * gap
    x = (W - total) // 2
    y = 150
    for i, (t, col) in enumerate(steps):
        tc = INK if col == YELLOW else WHITE
        rounded(d, [x, y, x + bw, y + bh], 18, col)
        text_center(d, x + bw / 2, y + bh / 2, t, font(28, True), tc)
        if i < n - 1:
            arrow(d, (x + bw + 6, y + bh / 2), (x + bw + gap - 6, y + bh / 2),
                  GREY, width=8, head=22)
        x += bw + gap
    text_center(d, W // 2, 60, "CHAINE D'AUTOMATISATION CONTINUE", font(30, True), BLUE)
    save(img, "pipeline.png")


# ---------------------------------------------------------------------------
# 5. Burn-down chart
# ---------------------------------------------------------------------------
def burndown():
    W, H = 1100, 720
    img, d = canvas(W, H, WHITE)
    ox, oy = 130, 600          # origine des axes
    ax_w, ax_h = 820, 470
    # axes
    d.line([(ox, oy), (ox, oy - ax_h)], fill=INK, width=4)
    d.line([(ox, oy), (ox + ax_w, oy)], fill=INK, width=4)
    # grille + graduations Y (0..30)
    for i in range(0, 31, 5):
        y = oy - (i / 30) * ax_h
        d.line([(ox, y), (ox + ax_w, y)], fill=(225, 230, 235), width=1)
        text_center(d, ox - 35, y, str(i), font(20), GREY)
    for j in range(0, 21, 5):
        x = ox + (j / 20) * ax_w
        text_center(d, x, oy + 28, str(j), font(20), GREY)
    # ligne ideale (bleue)
    p_ideal = [(ox, oy - ax_h), (ox + ax_w, oy)]
    d.line(p_ideal, fill=BLUE, width=5)
    # ligne reelle (rouge) - en escalier
    real = [30, 30, 27, 24, 24, 20, 18, 15, 14, 11, 7, 0]
    pts = []
    for k, v in enumerate(real):
        x = ox + (k / (len(real) - 1)) * ax_w
        y = oy - (v / 30) * ax_h
        pts.append((x, y))
    d.line(pts, fill=RED, width=5, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=RED)
    # titres / legende
    text_center(d, W // 2, 46, "PROJECT XYZ - ITERATION 1 BURN DOWN", font(28, True), BLUE)
    # label Y vertical (image pivotee pour eviter le chevauchement avec la grille)
    ylab = Image.new("RGBA", (320, 32), (255, 255, 255, 0))
    ImageDraw.Draw(ylab).text((0, 0), "Sum of Task Estimates (days)",
                              font=font(18, True), fill=GREY)
    ylab = ylab.rotate(90, expand=True)
    img.paste(ylab, (12, int(oy - ax_h / 2 - 160)), ylab)
    text_center(d, ox + ax_w / 2, oy + 70, "Iteration Timeline (days)", font(20, True), GREY)
    # legende
    lx, ly = ox + 470, oy - ax_h + 20
    d.line([(lx, ly), (lx + 50, ly)], fill=BLUE, width=5)
    d.text((lx + 60, ly - 12), "Ideal Tasks Remaining", font=font(19), fill=INK)
    d.line([(lx, ly + 40), (lx + 50, ly + 40)], fill=RED, width=5)
    d.text((lx + 60, ly + 28), "Actual Tasks Remaining", font=font(19), fill=INK)
    save(img, "burndown.png")


# ---------------------------------------------------------------------------
# 6. Diagramme du processus Scrum (rasterise depuis scrum.svg)
# ---------------------------------------------------------------------------
def scrum_process():
    svg = os.path.join(HERE, "..", "presentation-pdf", "img", "scrum.svg")
    out = os.path.join(IMG, "scrum_process.png")
    if not os.path.exists(svg):
        print("  (scrum.svg introuvable, ignore)")
        return
    try:
        subprocess.run(["convert", "-density", "200", "-background", "white",
                        "-flatten", svg, out], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  -> scrum_process.png (depuis scrum.svg)")
    except Exception as e:
        print("  (convert indisponible:", e, ")")


def main():
    empirisme()
    melee()
    release_cycle()
    pipeline()
    burndown()
    scrum_process()
    print("Images ->", IMG)


if __name__ == "__main__":
    main()
