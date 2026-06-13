#!/usr/bin/env python3
"""Génère les illustrations SVG du cours Kubernetes (vectoriel, net à l'impression).

Fil rouge : une image nginx sert d'exemple pour illustrer tous les concepts.
"""
from pathlib import Path

IMG = Path(__file__).parent / "img"
IMG.mkdir(exist_ok=True)

# ---- Palette ----
INK     = "#1f2328"
MUTED   = "#57606a"
LINE    = "#d0d7de"
K8S     = "#326ce5"   # bleu Kubernetes
K8S_DK  = "#1a4fb4"
K8S_L   = "#e8f0fe"
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


def arrow(x1, y1, x2, y2, color=MUTED, sw=2.5, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' marker-end='url(#arr-{color.lstrip('#')})' {d}/>")


def line(x1, y1, x2, y2, color=MUTED, sw=2, dash=""):
    d = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' "
            f"stroke-width='{sw}' {d}/>")


def marker(color):
    return (f"<marker id='arr-{color.lstrip('#')}' viewBox='0 0 10 10' refX='9' refY='5' "
            f"markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0 L10 5 L0 10 z' fill='{color}'/></marker>")


COLORS = [MUTED, K8S, GREEN, PURPLE, ORANGE, TEAL, K8S_DK, RED]
DEFS = "<defs>" + "".join(marker(c) for c in COLORS) + "</defs>"


def pod(x, y, w, h, label="nginx", fill=GREEN_L, stroke=GREEN, sub="Pod", small=False):
    """Dessine un pod contenant un conteneur nginx."""
    s = box(x, y, w, h, "#ffffff", stroke, 10)
    s += text(x + 10, y + 16, sub, 9, stroke, "bold", "start")
    cw, ch = w - 20, h - 30
    s += box(x + 10, y + 22, cw, ch, fill, stroke, 7)
    fs = 10 if small else 12
    s += text(x + w/2, y + 22 + ch/2 + 4, label, fs, INK, "bold")
    return s


# ============================================================
# 1. Architecture d'un cluster Kubernetes
# ============================================================
def illu_architecture():
    W, H = 1100, 540
    b = DEFS
    b += text(W/2, 32, "Architecture d'un cluster Kubernetes", 20, INK, "bold")

    # kubectl
    b += box(40, 250, 130, 70, GREY_L, DARK, 10)
    b += text(105, 282, "kubectl", 14, DARK, "bold")
    b += text(105, 302, "(vous)", 10, MUTED)
    b += arrow(170, 285, 235, 200, K8S, 3)

    # Control plane
    cpx, cpy, cpw, cph = 240, 70, 360, 410
    b += box(cpx, cpy, cpw, cph, K8S_L, K8S, 14, 2.5)
    b += text(cpx + cpw/2, cpy + 26, "Control Plane (le cerveau)", 15, K8S_DK, "bold")
    cp = [
        ("kube-apiserver", "porte d'entrée — toutes les requêtes passent ici"),
        ("etcd", "base clé/valeur — l'état du cluster"),
        ("kube-scheduler", "choisit le node où placer chaque Pod"),
        ("controller-manager", "réconcilie l'état réel avec l'état désiré"),
    ]
    for i, (t, d) in enumerate(cp):
        yy = cpy + 44 + i*88
        b += box(cpx + 20, yy, cpw - 40, 74, "#ffffff", K8S, 9)
        b += text(cpx + cpw/2, yy + 26, t, 13.5, K8S_DK, "bold")
        b += text(cpx + cpw/2, yy + 50, d, 9.5, MUTED)

    # Worker nodes
    for n in range(2):
        nx = 660 + n*220
        ny, nw, nh = 90, 200, 390
        b += box(nx, ny, nw, nh, GREEN_L, GREEN, 14, 2.5)
        b += text(nx + nw/2, ny + 24, f"Worker Node {n+1}", 14, GREEN, "bold")
        # kubelet / kube-proxy
        b += box(nx + 16, ny + 36, nw - 32, 30, "#ffffff", GREEN, 7)
        b += text(nx + nw/2, ny + 56, "kubelet", 11, INK, "bold")
        b += box(nx + 16, ny + 72, nw - 32, 30, "#ffffff", GREEN, 7)
        b += text(nx + nw/2, ny + 92, "kube-proxy", 11, INK, "bold")
        # pods
        b += pod(nx + 16, ny + 112, nw - 32, 60, "nginx", GREEN_L, GREEN, "Pod", True)
        b += pod(nx + 16, ny + 180, nw - 32, 60, "nginx", GREEN_L, GREEN, "Pod", True)
        b += box(nx + 16, ny + 248, nw - 32, 30, GREY_L, LINE, 7)
        b += text(nx + nw/2, ny + 268, "container runtime", 10, MUTED, "bold")
        b += arrow(cpx + cpw + 4, 260, nx - 4, ny + 60, K8S, 2, "5 4")

    b += text(W/2, 520, "Le Control Plane décide ; les Worker Nodes exécutent les conteneurs. "
              "Tout dialogue passe par kube-apiserver.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 2. Anatomie d'un Pod
# ============================================================
def illu_pod():
    W, H = 1000, 420
    b = DEFS
    b += text(W/2, 32, "Le Pod : la plus petite unité déployable", 20, INK, "bold")
    b += text(W/2, 56, "Un Pod enveloppe un (ou plusieurs) conteneurs qui partagent réseau et stockage", 12, MUTED)

    # Node
    b += box(60, 80, W-120, 300, GREEN_L, GREEN, 14, 2.5)
    b += text(90, 106, "Worker Node", 13, GREEN, "bold", "start")

    # Pod
    px, py, pw, ph = 220, 130, 560, 210
    b += box(px, py, pw, ph, "#ffffff", K8S, 14, 2.5)
    b += text(px + 16, py + 26, "Pod", 15, K8S_DK, "bold", "start")
    b += text(px + pw - 16, py + 26, "IP unique : 10.244.1.7", 11, MUTED, "normal", "end")

    # conteneur nginx
    b += box(px + 30, py + 44, 240, 110, GREEN_L, GREEN, 10)
    b += text(px + 150, py + 70, "Conteneur", 11, GREEN, "bold")
    b += text(px + 150, py + 100, "nginx:1.27", 15, INK, "bold")
    b += text(px + 150, py + 128, "port 80", 11, MUTED)

    # ressources partagées
    b += box(px + 300, py + 44, 230, 50, K8S_L, K8S, 9)
    b += text(px + 415, py + 64, "Réseau partagé", 12, K8S_DK, "bold")
    b += text(px + 415, py + 82, "localhost entre conteneurs", 9.5, MUTED)
    b += box(px + 300, py + 104, 230, 50, ORANGE_L, ORANGE, 9)
    b += text(px + 415, py + 124, "Volumes partagés", 12, ORANGE, "bold")
    b += text(px + 415, py + 142, "montés dans le Pod", 9.5, MUTED)

    b += text(W/2, 405, "Règle : on ne lance jamais un conteneur seul — toujours dans un Pod. "
              "En général : 1 Pod = 1 conteneur applicatif.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 3. Deployment -> ReplicaSet -> Pods
# ============================================================
def illu_deployment():
    W, H = 1000, 470
    b = DEFS
    b += text(W/2, 32, "Deployment › ReplicaSet › Pods", 20, INK, "bold")
    b += text(W/2, 56, "Vous déclarez « je veux 3 nginx » ; Kubernetes s'occupe d'y arriver et de le maintenir", 12, MUTED)

    # Deployment
    b += box(330, 80, 340, 70, PURPLE_L, PURPLE, 12)
    b += text(500, 108, "Deployment : nginx", 15, PURPLE, "bold")
    b += text(500, 130, "replicas: 3  •  image: nginx:1.27", 11, MUTED)
    b += arrow(500, 150, 500, 185, PURPLE, 3)

    # ReplicaSet
    b += box(330, 190, 340, 64, K8S_L, K8S, 12)
    b += text(500, 216, "ReplicaSet", 14, K8S_DK, "bold")
    b += text(500, 238, "garantit que 3 Pods tournent", 11, MUTED)

    # Pods
    pods_y = 320
    xs = [180, 430, 680]
    for x in xs:
        b += arrow(500, 254, x + 70, pods_y - 6, K8S, 2.2)
        b += pod(x, pods_y, 140, 100, "nginx", GREEN_L, GREEN, "Pod")
    b += text(W/2, 455, "Si un Pod meurt, le ReplicaSet en recrée un aussitôt : c'est l'auto-réparation (self-healing).",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 4. Rolling update
# ============================================================
def illu_rolling():
    W, H = 1060, 430
    b = DEFS
    b += text(W/2, 32, "La mise à jour progressive (Rolling Update)", 20, INK, "bold")
    b += text(W/2, 56, "kubectl set image ... nginx:1.27 → nginx:1.28  —  zéro coupure", 12, MUTED)

    cols = [
        ("1. Départ", ["v1.27", "v1.27", "v1.27"], [GREEN]*3),
        ("2. En cours", ["v1.28", "v1.27", "v1.27"], [K8S, GREEN, GREEN]),
        ("3. En cours", ["v1.28", "v1.28", "v1.27"], [K8S, K8S, GREEN]),
        ("4. Terminé", ["v1.28", "v1.28", "v1.28"], [K8S]*3),
    ]
    cw = 230
    x0 = 40
    for i, (title, vers, cols_c) in enumerate(cols):
        x = x0 + i*(cw + 16)
        b += box(x, 80, cw, 290, GREY_L, LINE, 12)
        b += text(x + cw/2, 106, title, 13, INK, "bold")
        for k, (v, c) in enumerate(zip(vers, cols_c)):
            cl = K8S_L if c == K8S else GREEN_L
            b += pod(x + 30, 124 + k*78, cw - 60, 66, f"nginx {v}", cl, c, "Pod", True)
        if i < 3:
            b += arrow(x + cw + 1, 225, x + cw + 15, 225, MUTED, 2.5)

    b += text(W/2, 408, "Kubernetes remplace les Pods un par un : il en crée un neuf, attend qu'il soit prêt, "
              "puis supprime un ancien.", 11, MUTED)
    return svg(W, H, b)


# ============================================================
# 5. Services & exposition
# ============================================================
def illu_service():
    W, H = 1040, 470
    b = DEFS
    b += text(W/2, 32, "Le Service : une adresse stable devant des Pods éphémères", 20, INK, "bold")
    b += text(W/2, 56, "Le Service route le trafic vers les Pods qui portent le bon label (selector)", 12, MUTED)

    # Service
    b += box(360, 80, 320, 84, K8S_L, K8S, 12)
    b += text(520, 108, "Service : nginx", 15, K8S_DK, "bold")
    b += text(520, 130, "selector: app=nginx", 11, MUTED)
    b += text(520, 150, "IP stable + DNS : nginx.default", 10.5, MUTED)

    # pods avec label
    pods_y = 250
    xs = [120, 360, 600, 840]
    labels_ok = [True, True, True, False]
    for x, ok in zip(xs, labels_ok):
        c = GREEN if ok else MUTED
        cl = GREEN_L if ok else GREY_L
        b += pod(x, pods_y, 140, 96, "nginx", cl, c, "app=nginx" if ok else "app=autre")
        if ok:
            b += arrow(520, 164, x + 70, pods_y - 6, K8S, 2.2)
    b += text(840 + 70, pods_y + 116, "label différent → ignoré", 9.5, MUTED)

    # types
    types = [
        ("ClusterIP", "interne au cluster (défaut)", TEAL, TEAL_L),
        ("NodePort", "port ouvert sur chaque node", ORANGE, ORANGE_L),
        ("LoadBalancer", "IP publique (cloud)", PURPLE, PURPLE_L),
    ]
    tw = 320
    for i, (t, d, c, cl) in enumerate(types):
        x = 40 + i*(tw + 12)
        b += box(x, 392, tw, 56, cl, c, 10)
        b += text(x + tw/2, 416, t, 13, c, "bold")
        b += text(x + tw/2, 436, d, 10.5, MUTED)
    return svg(W, H, b)


# ============================================================
# 6. ConfigMap & Secret
# ============================================================
def illu_config():
    W, H = 1000, 420
    b = DEFS
    b += text(W/2, 32, "ConfigMap & Secret : séparer la config du conteneur", 20, INK, "bold")
    b += text(W/2, 56, "La même image nginx, configurée différemment selon l'environnement", 12, MUTED)

    # ConfigMap
    b += box(70, 100, 300, 110, TEAL_L, TEAL, 12)
    b += text(220, 126, "ConfigMap : nginx-conf", 13, TEAL, "bold")
    b += text(85, 152, "default.conf: |", 10.5, INK, "normal", "start")
    b += text(85, 172, "  server { listen 80; ... }", 10.5, MUTED, "normal", "start")
    b += text(85, 192, "index.html, variables...", 10.5, MUTED, "normal", "start")

    # Secret
    b += box(70, 240, 300, 110, ORANGE_L, ORANGE, 12)
    b += text(220, 266, "Secret : nginx-tls", 13, ORANGE, "bold")
    b += text(85, 292, "tls.crt: •••••• (base64)", 10.5, INK, "normal", "start")
    b += text(85, 312, "tls.key: •••••• (base64)", 10.5, INK, "normal", "start")
    b += text(85, 332, "chiffré au repos dans etcd", 10, MUTED, "normal", "start")

    b += arrow(370, 175, 600, 200, TEAL, 3)
    b += arrow(370, 295, 600, 245, ORANGE, 3)
    b += text(490, 150, "monté en volume", 10.5, MUTED, "bold")
    b += text(490, 330, "ou injecté en variable", 10.5, MUTED, "bold")

    # Pod nginx
    b += box(600, 150, 320, 140, "#ffffff", K8S, 14, 2.5)
    b += text(616, 176, "Pod nginx", 14, K8S_DK, "bold", "start")
    b += box(630, 190, 260, 80, GREEN_L, GREEN, 10)
    b += text(760, 222, "nginx:1.27", 15, INK, "bold")
    b += text(760, 248, "/etc/nginx/conf.d/", 10, MUTED)

    b += text(W/2, 400, "On change la config sans rebuilder l'image : il suffit de modifier le ConfigMap et de redémarrer les Pods.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 7. Stockage : PV / PVC / StorageClass
# ============================================================
def illu_storage():
    W, H = 1020, 400
    b = DEFS
    b += text(W/2, 32, "Le stockage persistant : PVC › PV › StorageClass", 20, INK, "bold")
    b += text(W/2, 56, "Les Pods sont éphémères ; le volume persistant survit à leur suppression", 12, MUTED)

    # Pod
    b += box(60, 150, 200, 120, "#ffffff", K8S, 14, 2.5)
    b += text(160, 176, "Pod nginx", 13, K8S_DK, "bold")
    b += box(80, 192, 160, 60, GREEN_L, GREEN, 10)
    b += text(160, 226, "monte /data", 12, INK, "bold")
    b += arrow(260, 210, 350, 210, K8S, 3)

    # PVC
    b += box(350, 150, 200, 120, PURPLE_L, PURPLE, 12)
    b += text(450, 176, "PVC", 14, PURPLE, "bold")
    b += text(450, 200, "« je veux 5 Gi", 11, MUTED)
    b += text(450, 218, "en lecture/écriture »", 11, MUTED)
    b += text(450, 244, "la demande", 10, MUTED)
    b += arrow(550, 210, 640, 210, PURPLE, 3)
    b += text(595, 196, "lie", 10, MUTED, "bold")

    # PV
    b += box(640, 150, 200, 120, ORANGE_L, ORANGE, 12)
    b += text(740, 176, "PV", 14, ORANGE, "bold")
    b += text(740, 200, "5 Gi réels", 11, MUTED)
    b += text(740, 218, "(disque, NFS, cloud)", 11, MUTED)
    b += text(740, 244, "la ressource", 10, MUTED)

    # StorageClass
    b += box(640, 300, 200, 60, TEAL_L, TEAL, 10)
    b += text(740, 326, "StorageClass", 13, TEAL, "bold")
    b += text(740, 346, "provisionne à la demande", 9.5, MUTED)
    b += arrow(740, 300, 740, 272, TEAL, 2.5, "5 4")

    b += text(W/2, 388, "Le Pod demande (PVC), Kubernetes fournit (PV) — automatiquement via la StorageClass.",
              11, MUTED)
    return svg(W, H, b)


# ============================================================
# 8. Ingress
# ============================================================
def illu_ingress():
    W, H = 1020, 430
    b = DEFS
    b += text(W/2, 32, "L'Ingress : un routeur HTTP à l'entrée du cluster", 20, INK, "bold")
    b += text(W/2, 56, "Une seule IP publique route vers plusieurs Services selon l'URL", 12, MUTED)

    # Internet
    b += box(60, 180, 140, 70, GREY_L, DARK, 30)
    b += text(130, 212, "Internet", 14, DARK, "bold")
    b += text(130, 232, "utilisateurs", 9.5, MUTED)
    b += arrow(200, 215, 260, 215, K8S, 3)

    # Ingress
    b += box(260, 150, 240, 130, K8S_L, K8S, 14, 2.5)
    b += text(380, 178, "Ingress Controller", 14, K8S_DK, "bold")
    b += text(380, 204, "host: quickbite.io", 10.5, MUTED)
    b += text(380, 230, "/        → nginx", 10.5, INK)
    b += text(380, 250, "/api  → backend", 10.5, INK)

    # Services + pods
    rows = [("Service nginx", "app=nginx", GREEN, GREEN_L, 110, "/"),
            ("Service backend", "app=api", PURPLE, PURPLE_L, 280, "/api")]
    for name, lab, c, cl, yy, route in rows:
        b += arrow(500, 200 if route == "/" else 230, 600, yy + 30, c, 2.5)
        b += box(600, yy, 200, 60, cl, c, 10)
        b += text(700, yy + 26, name, 13, c, "bold")
        b += text(700, yy + 46, lab, 10, MUTED)
        b += pod(840, yy, 140, 60, "nginx" if route == "/" else "api", cl, c, "Pod", True)
        b += arrow(800, yy + 30, 840, yy + 30, c, 2)

    b += text(W/2, 412, "Sans Ingress, il faudrait un LoadBalancer (et une IP) par Service. "
              "L'Ingress mutualise l'entrée HTTP/HTTPS.", 11, MUTED)
    return svg(W, H, b)


def main():
    illus = {
        "01-architecture.svg": illu_architecture(),
        "02-pod.svg":          illu_pod(),
        "03-deployment.svg":   illu_deployment(),
        "04-rolling.svg":      illu_rolling(),
        "05-service.svg":      illu_service(),
        "06-config.svg":       illu_config(),
        "07-storage.svg":      illu_storage(),
        "08-ingress.svg":      illu_ingress(),
    }
    for name, content in illus.items():
        (IMG / name).write_text(content, encoding="utf-8")
        print(f"  + img/{name}")
    print(f"\n{len(illus)} illustrations générées dans {IMG}")


if __name__ == "__main__":
    main()
