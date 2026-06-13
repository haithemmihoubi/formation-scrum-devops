#!/usr/bin/env python3
"""Assemble les modules Markdown du cours Docker en un seul PDF stylé."""
import re
import markdown
from pathlib import Path
from weasyprint import HTML, CSS as WCSS

BASE = Path(__file__).parent

# Ordre des modules dans le PDF
FILES = [
    "00-introduction-docker.md",
    "01-spring-boot-multistage.md",
    "02-multi-environnement.md",
    "03-angular.md",
    "04-react.md",
    "05-python.md",
    "06-bonnes-pratiques.md",
]

CSS = """
@page {
    size: A4;
    margin: 2.2cm 1.8cm 2cm 1.8cm;
    @top-left { content: "Dockeriser ses applications — Spring Boot, Angular, React, Python"; font-size: 8pt; color: #888; }
    @top-right { content: "Formateur : Haithem Mihoubi"; font-size: 8pt; color: #0b6bcb; font-weight: bold; }
    @bottom-center { content: "Page " counter(page) " / " counter(pages); font-size: 8pt; color: #888; }
}
@page cover {
    @top-left { content: ""; }
    @top-right { content: ""; }
    @bottom-center { content: ""; }
}
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.5; color: #222; }
h1 { color: #0b6bcb; font-size: 22pt; border-bottom: 3px solid #0b6bcb; padding-bottom: 6px; page-break-before: always; }
h2 { color: #0d7ec0; font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #cdd; padding-bottom: 3px; }
h3 { color: #1aa179; font-size: 12.5pt; margin-top: 1.1em; }
a { color: #0d7ec0; text-decoration: none; }
code { font-family: "DejaVu Sans Mono", monospace; background: #f2f4f7; padding: 1px 4px; border-radius: 3px; font-size: 9pt; color: #b00050; }
pre { background: #1e2330; color: #e6e6e6; padding: 10px 12px; border-radius: 6px; overflow-x: auto; font-size: 8.4pt; line-height: 1.35; page-break-inside: avoid; }
pre code { background: transparent; color: #e6e6e6; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9pt; page-break-inside: avoid; }
th { background: #0b6bcb; color: white; padding: 5px 8px; text-align: left; }
td { border: 1px solid #cdd; padding: 4px 8px; }
tr:nth-child(even) { background: #f4f7fa; }
blockquote { border-left: 4px solid #1aa179; background: #f0faf4; margin: 0.6em 0; padding: 6px 12px; color: #355; }
ul, ol { margin: 0.5em 0; }
li { margin: 2px 0; }
hr { border: none; border-top: 1px solid #ccd; margin: 1.2em 0; }
.cover { page: cover; page-break-after: always; text-align: center; padding-top: 24%; }
.cover h1 { border: none; font-size: 30pt; page-break-before: avoid; color: #0b6bcb; }
.cover .sub { font-size: 14pt; color: #555; margin-top: 10px; }
.cover .formateur { font-size: 13pt; color: #0b6bcb; font-weight: bold; margin-top: 50px; }
.cover .meta { font-size: 10pt; color: #888; margin-top: 14px; }
.toc { page-break-after: always; }
.toc h1 { page-break-before: avoid; }
.toc ul { list-style: none; padding: 0; margin-top: 1em; }
.toc li { margin: 7px 0; font-size: 11pt; border-bottom: 1px dotted #dde; padding-bottom: 4px; }
.toc a { color: #0b6bcb; text-decoration: none; display: flex; }
.toc a::after { content: target-counter(attr(href), page); color: #888; margin-left: auto; padding-left: 8px; font-size: 10pt; }
.toc .num { color: #1aa179; font-weight: bold; margin-right: 8px; min-width: 34px; }
"""


def fix_links(html: str) -> str:
    return re.sub(r'href="[0-9A-Za-z\-]+\.md(#[^"]*)?"', 'href="#"', html)


def preprocess(text: str) -> str:
    """Insère une ligne vide avant un tableau collé à du texte (hors blocs de code)."""
    lines = text.split("\n")
    out = []
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        if (not in_fence and stripped.startswith("|") and out
                and out[-1].strip() != "" and not out[-1].lstrip().startswith("|")
                and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: ")
                and "-" in lines[i + 1]):
            out.append("")
        out.append(line)
    return "\n".join(out)


md = markdown.Markdown(extensions=["extra", "fenced_code", "tables", "sane_lists", "toc"])

cover = """
<div class="cover">
  <h1>Dockeriser ses<br>applications</h1>
  <div class="sub">Multi-stage &amp; multi-environnement &mdash; Spring Boot, Angular, React, Python</div>
  <div class="formateur">Formateur : Haithem Mihoubi</div>
  <div class="meta">Formation DevOps &bull; 7 modules &bull; 2026</div>
</div>
"""


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


modules = []
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

toc_items = "".join(
    f'<li><a href="#{hid}"><span class="num">{i:02d}</span>{title}</a></li>'
    for i, (hid, title, _) in enumerate(modules)
)
toc = f'<div class="toc"><h1>Table des matières</h1><ul>{toc_items}</ul></div>'

parts = [cover, toc] + [html for _, _, html in modules]
html_doc = f"<html><head><meta charset='utf-8'></head><body>{''.join(parts)}</body></html>"

out = BASE / "Cours-Docker-Multistage.pdf"
HTML(string=html_doc, base_url=str(BASE)).write_pdf(str(out), stylesheets=[WCSS(string=CSS)])
print(f"\nPDF généré : {out}")
