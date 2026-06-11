#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build des manuels de formation : Markdown -> HTML -> PDF (weasyprint).

Usage:
    python3 build.py module1.md "Manuel ..." "out/Module1.pdf"
    python3 build.py --all
"""
import sys
import os
import re
import markdown
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(HERE, "style.css")
OUT = os.path.join(HERE, "out")

MD_EXTENSIONS = [
    "extra",          # tables, fenced_code, footnotes, attr_list, def_list...
    "codehilite",
    "toc",
    "sane_lists",
    "admonition",
]
MD_CONFIG = {
    "codehilite": {"guess_lang": False, "noclasses": False, "css_class": "codehilite"},
    # Sommaire auto : seulement les niveaux 1-2 (modules/jours + chapitres),
    # avec un titre "Sommaire". Les liens sont cliquables ; les numéros de
    # page sont ajoutés par la CSS (target-counter).
    "toc": {"title": "Sommaire", "toc_depth": "1-2"},
}


def _fix_tight_lists(md_text: str) -> str:
    """Insère une ligne vide entre une ligne entièrement en gras (titre de
    sommaire) et la liste qui la suit immédiatement, sinon la liste est
    absorbée dans le paragraphe. On ne touche jamais aux blocs de code ```."""
    parts = re.split(r"(```.*?```)", md_text, flags=re.DOTALL)
    for i in range(0, len(parts), 2):  # 0,2,4… = hors blocs de code
        parts[i] = re.sub(
            r"(?m)^(\*\*[^\n]+\*\*[ \t]*)\n([-*] )",
            r"\1\n\n\2",
            parts[i],
        )
    return "".join(parts)


def md_to_html(md_text: str) -> str:
    md_text = _fix_tight_lists(md_text)
    # Le contenu markdown placé dans un <div class="toc"> doit être interprété :
    # on ajoute l'attribut markdown="1" (extension md_in_html) si absent.
    md_text = re.sub(
        r'<div class="toc">(?!\s*markdown)',
        '<div class="toc" markdown="1">',
        md_text,
    )
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    return md.convert(md_text)


def wrap(title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
{body_html}
</body>
</html>"""


def build(md_path: str, title: str, out_pdf: str):
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    body = md_to_html(md_text)
    html = wrap(title, body)
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    HTML(string=html, base_url=HERE).write_pdf(out_pdf, stylesheets=[CSS])
    size = os.path.getsize(out_pdf) / 1024
    print(f"  OK -> {out_pdf}  ({size:.0f} KB)")


JOBS = [
    ("module1.md", "Module 1 — Agile, Scrum & Kanban", "out/Module1-Agile-Scrum-Kanban.pdf"),
    ("module2.md", "Module 2 — DevOps CI/CD, Docker, Kubernetes", "out/Module2-DevOps-CICD-Docker-Kubernetes.pdf"),
    ("module3.md", "Module 3 — Spring Security", "out/Module3-Spring-Security.pdf"),
]


def main():
    if len(sys.argv) >= 4:
        build(sys.argv[1], sys.argv[2], sys.argv[3])
        return
    # --all (par défaut) : ne construit que les fichiers présents
    for md, title, out in JOBS:
        path = os.path.join(HERE, md)
        if os.path.exists(path):
            print(f"Build {md} ...")
            build(path, title, os.path.join(HERE, out))
        else:
            print(f"  (skip {md} — absent)")


if __name__ == "__main__":
    main()
