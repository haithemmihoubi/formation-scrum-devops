#!/usr/bin/env python3
"""Assemble les modules Markdown du cours en un seul PDF stylé."""
import re
import markdown
from pathlib import Path
from weasyprint import HTML

BASE = Path(__file__).parent

# Ordre des modules dans le PDF
FILES = [
    "00-introduction-devops.md",
    "01-linux-fondamentaux.md",
    "02-linux-utilisateurs-permissions.md",
    "03-linux-processus-services.md",
    "04-linux-paquets-stockage.md",
    "05-bash-scripting.md",
    "06-reseau-fondamentaux.md",
    "07-reseau-adressage-ip.md",
    "07b-adressage-ip-approfondi.md",
    "08-reseau-protocoles-services.md",
    "09-reseau-outils-diagnostic.md",
    "10-securite-parefeu.md",
    "11-pratique-devops.md",
    "12-travaux-pratiques.md",
]

CSS = """
@page {
    size: A4;
    margin: 2.2cm 1.8cm 2cm 1.8cm;
    @top-left { content: "Cours Réseau & Linux pour le DevOps"; font-size: 8pt; color: #888; }
    @top-right { content: "Formateur : Haithem Mihoubi"; font-size: 8pt; color: #1a4f8b; font-weight: bold; }
    @bottom-center { content: "Page " counter(page) " / " counter(pages); font-size: 8pt; color: #888; }
}
@page cover {
    @top-left { content: ""; }
    @top-right { content: ""; }
    @bottom-center { content: ""; }
}
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.5; color: #222; }
h1 { color: #1a4f8b; font-size: 22pt; border-bottom: 3px solid #1a4f8b; padding-bottom: 6px; page-break-before: always; }
h2 { color: #1a6b9b; font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #cdd; padding-bottom: 3px; }
h3 { color: #2a7; font-size: 12.5pt; margin-top: 1.1em; }
a { color: #1a6b9b; text-decoration: none; }
code { font-family: "DejaVu Sans Mono", monospace; background: #f2f4f7; padding: 1px 4px; border-radius: 3px; font-size: 9pt; color: #b00050; }
pre { background: #1e2330; color: #e6e6e6; padding: 10px 12px; border-radius: 6px; overflow-x: auto; font-size: 8.6pt; line-height: 1.35; page-break-inside: avoid; }
pre code { background: transparent; color: #e6e6e6; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9pt; page-break-inside: avoid; }
th { background: #1a4f8b; color: white; padding: 5px 8px; text-align: left; }
td { border: 1px solid #cdd; padding: 4px 8px; }
tr:nth-child(even) { background: #f4f7fa; }
blockquote { border-left: 4px solid #2a7; background: #f0faf4; margin: 0.6em 0; padding: 6px 12px; color: #355; }
details { border: 1px solid #d0d7de; border-radius: 6px; padding: 6px 10px; margin: 0.5em 0; background: #fbfcfd; page-break-inside: avoid; }
summary { font-weight: bold; color: #1a6b9b; }
ul, ol { margin: 0.5em 0; }
li { margin: 2px 0; }
hr { border: none; border-top: 1px solid #ccd; margin: 1.2em 0; }
.cover { page: cover; page-break-after: always; text-align: center; padding-top: 26%; }
.cover h1 { border: none; font-size: 30pt; page-break-before: avoid; color: #1a4f8b; }
.cover .sub { font-size: 14pt; color: #555; margin-top: 10px; }
.cover .formateur { font-size: 13pt; color: #1a4f8b; font-weight: bold; margin-top: 50px; }
.cover .meta { font-size: 10pt; color: #888; margin-top: 14px; }
/* Table des matières */
.toc { page-break-after: always; }
.toc h1 { page-break-before: avoid; }
.toc ul { list-style: none; padding: 0; margin-top: 1em; }
.toc li { margin: 7px 0; font-size: 11pt; border-bottom: 1px dotted #dde; padding-bottom: 4px; }
.toc a { color: #1a4f8b; text-decoration: none; display: flex; }
.toc a::after { content: target-counter(attr(href), page); color: #888; margin-left: auto; padding-left: 8px; font-size: 10pt; }
.toc .num { color: #2a7; font-weight: bold; margin-right: 8px; min-width: 34px; }
"""

def fix_links(html: str) -> str:
    """Transforme les liens .md internes en ancres simples (désactivés en PDF)."""
    return re.sub(r'href="[0-9A-Za-z\-]+\.md(#[^"]*)?"', 'href="#"', html)

def preprocess(text: str) -> str:
    """Insère une ligne vide avant un tableau collé à du texte (hors blocs de code)."""
    # active l'interprétation markdown à l'intérieur des balises <details>
    text = text.replace("<details>", '<details markdown="1">')
    lines = text.split("\n")
    out = []
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        # tableau Markdown détecté : ligne | ... | suivie d'une ligne de séparation |---|
        if (not in_fence and stripped.startswith("|") and out
                and out[-1].strip() != "" and not out[-1].lstrip().startswith("|")
                and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: ")
                and "-" in lines[i + 1]):
            out.append("")
        out.append(line)
    return "\n".join(out)

md = markdown.Markdown(extensions=["extra", "fenced_code", "tables", "sane_lists", "toc", "md_in_html"])

cover = """
<div class="cover">
  <h1>Réseau &amp; Linux<br>pour le DevOps</h1>
  <div class="sub">Cours complet &mdash; théorie, commandes, exercices corrigés</div>
  <div class="formateur">Formateur : Haithem Mihoubi</div>
  <div class="meta">Formation DevOps &bull; 14 modules &bull; 2026</div>
</div>
"""

def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()

modules = []          # (id, titre, html) pour chaque module
for fname in FILES:
    path = BASE / fname
    if not path.exists():
        print(f"  ! manquant: {fname}")
        continue
    text = preprocess(path.read_text(encoding="utf-8"))
    md.reset()
    html = fix_links(md.convert(text))
    m = re.search(r'<h1 id="([^"]+)">(.*?)</h1>', html, re.S)
    hid = m.group(1) if m else fname
    title = strip_tags(m.group(2)) if m else fname
    modules.append((hid, title, html))
    print(f"  + {fname}")

# Table des matières cliquable (numéros de page calculés par WeasyPrint)
toc_items = "".join(
    f'<li><a href="#{hid}">{title}</a></li>'
    for (hid, title, _) in modules
)
toc = f'<div class="toc"><h1>Table des matières</h1><ul>{toc_items}</ul></div>'

parts = [cover, toc] + [html for _, _, html in modules]
html_doc = f"<html><head><meta charset='utf-8'></head><body>{''.join(parts)}</body></html>"

out = BASE / "Cours-Reseau-Linux-DevOps.pdf"
HTML(string=html_doc, base_url=str(BASE)).write_pdf(str(out), stylesheets=[__import__('weasyprint').CSS(string=CSS)])
print(f"\nPDF généré : {out}")
