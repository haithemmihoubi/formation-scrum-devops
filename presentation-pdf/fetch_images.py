#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Télécharge des logos officiels depuis Wikimedia Commons (Special:FilePath)
et valide chaque fichier (SVG bien formé ou PNG/JPG valide, taille minimale,
pas une page d'erreur HTML). Les images valides sont placées dans img/.
"""
import os
import subprocess
import xml.dom.minidom

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)

BASE = "https://commons.wikimedia.org/wiki/Special:FilePath/"

# nom_local : nom_de_fichier_Wikimedia
LOGOS = {
    "docker.svg": "Docker_(container_engine)_logo.svg",
    "kubernetes.svg": "Kubernetes_logo_without_workmark.svg",
    "git.svg": "Git-logo.svg",
    "github.svg": "GitHub_Invertocat_Logo.svg",
    "gitlab.svg": "GitLab_logo.svg",
    "jenkins.svg": "Jenkins_logo.svg",
    "prometheus.svg": "Prometheus_software_logo.svg",
    "grafana.svg": "Grafana_logo.svg",
    "spring.svg": "Spring_Boot.svg",
    "oauth.svg": "Oauth_logo.svg",
    "openid.svg": "Openid_logo.svg",
    "postgresql.svg": "Postgresql_elephant.svg",
    "postman.svg": "Postman_(software).svg",
    "helm.svg": "Helm_(package_manager).svg",
    "scrum.svg": "Scrum_process.svg",
    "kanban.svg": "Simple-kanban-board-.jpg",
}

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPG_MAGIC = b"\xff\xd8\xff"


def valid(path: str) -> bool:
    try:
        if os.path.getsize(path) < 500:
            return False
        with open(path, "rb") as f:
            head = f.read(16)
        if head.startswith(PNG_MAGIC) or head.startswith(JPG_MAGIC):
            return True
        # sinon, on attend du SVG bien formé
        with open(path, "rb") as f:
            data = f.read()
        if b"<svg" not in data[:2000]:
            return False
        xml.dom.minidom.parseString(data)
        return True
    except Exception:
        return False


def fetch(name: str, filename: str) -> bool:
    out = os.path.join(IMG, name)
    url = BASE + filename
    subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", "-A", "Mozilla/5.0", "-o", out, url],
        check=False,
    )
    if valid(out):
        size = os.path.getsize(out)
        print(f"  OK   {name:18s} {size:>7d} o")
        return True
    if os.path.exists(out):
        os.remove(out)
    print(f"  ÉCHEC {name:18s} (invalide/tronqué)")
    return False


def main():
    ok = []
    for name, filename in LOGOS.items():
        if fetch(name, filename):
            ok.append(name)
    print(f"\n{len(ok)}/{len(LOGOS)} images valides : {', '.join(ok)}")


if __name__ == "__main__":
    main()
