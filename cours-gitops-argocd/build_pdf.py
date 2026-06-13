#!/usr/bin/env python3
"""Assemble les modules Markdown du cours GitOps (Argo CD) en un seul PDF stylé."""
import re
import subprocess
import sys
import markdown
from pathlib import Path
from weasyprint import HTML, CSS as WCSS

BASE = Path(__file__).parent

FILES = [
    "00-introduction.md",
    "01-principes-gitops.md",
    "02-argocd-architecture.md",
    "03-application.md",
    "04-sync-rollback.md",
    "05-structure-depot.md",
    "06-bonnes-pratiques.md",
]

CSS = """
@page {
    size: A4;
    margin: 2.2cm 1.8cm 2cm 1.8cm;
    @top-left { content: "GitOps avec Argo CD"; font-size: 8pt; color: #888; }
    @top-right { content: "Formateur : Haithem Mihoubi"; font-size: 8pt; color: #ef7b4d; font-weight: bold; }
    @bottom-center { content: "Page " counter(page) " / " counter(pages); font-size: 8pt; color: #888; }
}
@page cover { @top-left { content: ""; } @top-right { content: ""; } @bottom-center { content: ""; } }
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1f2328; }
h1 { color: #d2602f; font-size: 22pt; border-bottom: 3px solid #ef7b4d; padding-bottom: 6px; page-break-before: always; }
h2 { color: #d2602f; font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #d0d7de; padding-bottom: 3px; }
h3 { color: #1a7f37; font-size: 12.5pt; margin-top: 1.1em; }
a { color: #d2602f; text-decoration: none; }
code { font-family: "DejaVu Sans Mono", monospace; background: #f6f8fa; padding: 1px 4px; border-radius: 3px; font-size: 9pt; color: #8250df; }
pre { background: #1f2328; color: #e6edf3; padding: 10px 12px; border-radius: 6px; overflow-x: auto; font-size: 8.2pt; line-height: 1.4; page-break-inside: avoid; }
pre code { background: transparent; color: #e6edf3; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9pt; page-break-inside: avoid; }
th { background: #ef7b4d; color: white; padding: 5px 8px; text-align: left; }
td { border: 1px solid #d0d7de; padding: 4px 8px; }
tr:nth-child(even) { background: #f6f8fa; }
blockquote { border-left: 4px solid #1a7f37; background: #dafbe1; margin: 0.6em 0; padding: 6px 12px; color: #1a4d2e; }
ul, ol { margin: 0.5em 0; }
li { margin: 2px 0; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 1.2em 0; }
img { max-width: 100%; display: block; margin: 1em auto; page-break-inside: avoid; }
.cover { page: cover; page-break-after: always; text-align: center; padding-top: 20%; }
.cover h1 { border: none; font-size: 30pt; page-break-before: avoid; color: #d2602f; }
.cover .sub { font-size: 14pt; color: #57606a; margin-top: 12px; }
.cover .badge { display:inline-block; background:#ef7b4d; color:#fff; font-size:11pt; padding:5px 16px; border-radius:20px; margin-top:24px; }
.cover .formateur { font-size: 13pt; color: #d2602f; font-weight: bold; margin-top: 44px; }
.cover .meta { font-size: 10pt; color: #888; margin-top: 14px; }
.toc { page-break-after: always; }
.toc h1 { page-break-before: avoid; }
.toc ul { list-style: none; padding: 0; margin-top: 1em; }
.toc li { margin: 7px 0; font-size: 11pt; border-bottom: 1px dotted #d0d7de; padding-bottom: 4px; }
.toc a { color: #d2602f; text-decoration: none; display: flex; }
.toc a::after { content: target-counter(attr(href), page); color: #888; margin-left: auto; padding-left: 8px; font-size: 10pt; }
.toc .num { color: #1a7f37; font-weight: bold; margin-right: 8px; min-width: 34px; }
.caption { text-align: center; font-size: 9pt; color: #57606a; font-style: italic; margin-top: -0.4em; margin-bottom: 1em; }
"""


def fix_links(html):
    return re.sub(r'href="[0-9A-Za-z\-]+\.md(#[^"]*)?"', 'href="#"', html)


def preprocess(text):
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


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def main():
    illu = BASE / "make_illustrations.py"
    if illu.exists():
        subprocess.run([sys.executable, str(illu)], check=True)

    md = markdown.Markdown(extensions=["extra", "fenced_code", "tables", "sane_lists", "toc"])

    cover = """
    <div class="cover">
      <h1>GitOps<br>avec Argo CD</h1>
      <div class="sub">Git comme source de vérité — déploiement déclaratif, sync &amp; rollback automatiques</div>
      <div class="badge">Formation DevOps &bull; avec illustrations</div>
      <div class="formateur">Formateur : Haithem Mihoubi</div>
      <div class="meta">7 modules &bull; fil rouge : déployer nginx en GitOps &bull; 2026</div>
    </div>
    """

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

    out = BASE / "Cours-GitOps-ArgoCD.pdf"
    HTML(string=html_doc, base_url=str(BASE)).write_pdf(str(out), stylesheets=[WCSS(string=CSS)])
    print(f"\nPDF généré : {out}")


if __name__ == "__main__":
    main()
