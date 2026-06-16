#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Présentation PDF 16:9 — « Les bénéfices du CI/CD & GitHub Actions ».
Pédagogie pas à pas : problème → solution → bénéfice → exemple.
Génère les schémas puis assemble le PDF avec weasyprint."""
import os
import subprocess
import sys
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "Presentation-CICD-GitHub-Actions.pdf")
PDFS = os.path.abspath(os.path.join(HERE, "..", "pdfs", "Presentation-CICD-GitHub-Actions.pdf"))
CSS = os.path.join(HERE, "slides.css")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

TITLE = "CI/CD : livrer plus vite,<br>avec confiance"
SUB = "Les bénéfices business de l'agilité technique — illustré avec GitHub Actions"
AUTHOR = "Haithem Mihoubi"

D = "img/diagrams/"
L = "img/"


def bullets_html(items):
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append(f'<li class="sub">{it[0]}</li>')
        else:
            out.append(f'<li>{it}</li>')
    return "<ul>" + "".join(out) + "</ul>"


def benef_html(cards):
    out = '<div class="benef">'
    for kind, h, d in cards:
        out += f'<div class="card {kind}"><div class="h">{h}</div><div class="d">{d}</div></div>'
    return out + "</div>"


SLIDES = [
    {"t": "title"},

    {"t": "content", "title": "Comment lire cette présentation", "img": D + "feedback-loop.svg",
     "intro": "On avance <strong>pas à pas</strong> : pour chaque idée — le problème, la solution, le <strong>bénéfice métier</strong>, puis un exemple.",
     "bullets": [
        "1) Pourquoi le CI/CD ? (le problème du métier)",
        "2) Ce que CI/CD apporte : qualité + <strong>agilité business</strong>",
        "3) GitHub Actions, composant par composant",
        ("Fil rouge : l'application QuickBite, du commit à la prod",),
     ]},

    # ============== PARTIE 1 : LE PROBLÈME ==============
    {"t": "section", "num": "PARTIE 1", "title": "Pourquoi le CI/CD ?", "sub": "Le problème côté métier"},

    {"t": "content", "title": "Livrer du logiciel, c'est risqué", "img": D + "sans-vs-avec.svg",
     "intro": "Sans automatisation, chacun code dans son coin et l'<strong>intégration arrive à la fin</strong> : c'est là que tout casse.",
     "bullets": [
        "« Ça marche chez moi » → mais pas en production",
        "Fusions géantes = conflits et bugs en cascade",
        "Mises en prod rares, manuelles et <strong>stressantes</strong>",
        ("Conséquence métier : on livre lentement et on perd des clients",),
     ]},

    {"t": "full", "title": "Le coût d'un bug grandit avec le temps", "img": D + "cout-du-bug.svg",
     "intro": "Un bug attrapé <strong>au commit</strong> coûte presque rien ; le même bug <strong>en production</strong> peut coûter 100×. Le CI/CD déplace la détection le plus tôt possible — « shift left »."},

    {"t": "content", "title": "Ce que veut le métier", "img": D + "value-loop.svg",
     "intro": "Le métier ne veut pas « des pipelines ». Il veut <strong>livrer de la valeur vite et sans casser</strong>.",
     "bullets": [
        "Mettre une fonctionnalité entre les mains des clients <strong>rapidement</strong>",
        "Réagir à un concurrent ou à un bug en heures, pas en semaines",
        "Tenir la promesse de l'<strong>agilité</strong> : apprendre et corriger en boucle courte",
        ("CI/CD = le moteur technique qui rend l'agilité réelle",),
     ]},

    # ============== PARTIE 2 : LA SOLUTION & LES BÉNÉFICES ==============
    {"t": "section", "num": "PARTIE 2", "title": "CI/CD & ses bénéfices", "sub": "De la qualité technique à la valeur business"},

    {"t": "content", "title": "CI — Intégration continue", "img": D + "pipeline-vertical.svg",
     "intro": "<strong>À chaque commit</strong>, un pipeline automatique récupère le code, le teste et le construit.",
     "bullets": [
        "On intègre <strong>en petits lots, plusieurs fois par jour</strong>",
        "Lint + tests automatisés à chaque changement",
        "Règle d'or : <strong>on ne fusionne jamais un pipeline rouge</strong>",
        ("Résultat : les bugs sont bloqués avant d'atteindre les autres",),
     ]},

    {"t": "content", "title": "CD — Livraison / Déploiement continu", "img": D + "cicd-pipeline.svg",
     "intro": "Le code qui passe la CI est <strong>toujours déployable</strong> ; le CD pousse ensuite en production de façon automatique.",
     "bullets": [
        "<strong>Livraison continue</strong> : prêt à déployer à tout moment (1 clic)",
        "<strong>Déploiement continu</strong> : la prod se met à jour toute seule",
        "Rollback automatique si quelque chose tourne mal",
        ("La mise en prod devient une routine, pas un événement",),
     ]},

    {"t": "content", "title": "Bénéfices techniques", "img": D + "pipeline-vertical.svg",
     "intro": "Le pipeline est un <strong>filet de sécurité</strong> qui tourne pour vous, jour et nuit.",
     "benef": [
        ("g", "Qualité constante", "tests + lint + scan sécu à chaque commit"),
        ("g", "Feedback rapide", "on sait en minutes si on a cassé quelque chose"),
        ("g", "Moins de bugs en prod", "ils sont attrapés tôt, au plus bas coût"),
        ("g", "Process reproductible", "fini le « ça marche chez moi »"),
     ]},

    {"t": "content", "title": "Bénéfices business & agilité", "img": D + "value-loop.svg",
     "intro": "Ces gains techniques se traduisent directement en <strong>valeur pour l'entreprise</strong>.",
     "benef": [
        ("b", "Time-to-market réduit", "la valeur arrive aux clients en jours, pas en mois"),
        ("b", "Boucle d'apprentissage courte", "tester une idée, mesurer, ajuster — vite"),
        ("b", "Confiance & moins de stress", "des équipes qui livrent sereinement"),
        ("b", "Coûts maîtrisés", "moins d'incidents, moins de travail refait"),
     ]},

    {"t": "full", "title": "Mesurer l'impact : les 4 métriques DORA", "img": D + "dora.svg",
     "intro": "On ne pilote bien que ce qu'on mesure. Les métriques <strong>DORA</strong> relient la performance technique à la performance business : les organisations « élite » déploient plus souvent ET sont plus stables."},

    {"t": "full", "title": "Exemple chiffré : avant / après", "img": D + "avant-apres.svg",
     "intro": "Le même produit, la même équipe — avant et après l'adoption du CI/CD. Livrer <strong>plus souvent</strong> et <strong>plus sûrement</strong> ne sont pas opposés : ils vont ensemble."},

    # ============== PARTIE 3 : GITHUB ACTIONS ==============
    {"t": "section", "num": "PARTIE 3", "title": "GitHub Actions", "sub": "Le CI/CD intégré à votre dépôt"},

    {"t": "content", "title": "Pourquoi GitHub Actions ?", "img": L + "github.svg", "logo": True,
     "intro": "Le CI/CD <strong>natif dans GitHub</strong> : pas de serveur séparé à installer, tout vit avec le code.",
     "bullets": [
        "Configuré en <strong>YAML</strong>, versionné avec le projet",
        "Runners hébergés (Linux/Windows/macOS) — gratuit pour le public",
        "<strong>Marketplace</strong> : des milliers d'actions réutilisables",
        ("Déclenché par un push, une PR, un planning, un bouton…",),
     ]},

    {"t": "full", "title": "Anatomie : Workflow ▸ Job ▸ Step", "img": D + "gha-anatomy.svg",
     "intro": "Un <strong>Workflow</strong> contient des <strong>Jobs</strong> (qui tournent en parallèle par défaut), chaque Job contient des <strong>Steps</strong> exécutés dans l'ordre. <code>needs:</code> permet d'enchaîner les jobs."},

    {"t": "full", "title": "Les composants à connaître", "img": D + "gha-components.svg",
     "intro": "Huit briques suffisent à tout comprendre. On les retrouve dans chaque workflow."},

    {"t": "full", "title": "Les événements déclencheurs", "img": D + "gha-events.svg",
     "intro": "Le mot-clé <code>on:</code> définit <strong>quand</strong> le workflow se lance. <code>push</code> et <code>pull_request</code> couvrent l'essentiel du CI ; <code>workflow_dispatch</code> ajoute un déclenchement manuel."},

    {"t": "code", "title": "Un workflow complet, expliqué", "pill": ".github/workflows/ci.yml",
     "code": (
        '<span class="k">name:</span> <span class="s">CI</span>\n'
        '<span class="k">on:</span>\n'
        '  <span class="k">push:</span>\n'
        '    <span class="k">branches:</span> <span class="s">[ main ]</span>\n'
        '  <span class="k">pull_request:</span>\n'
        '<span class="k">jobs:</span>\n'
        '  <span class="k">build:</span>\n'
        '    <span class="k">runs-on:</span> <span class="s">ubuntu-latest</span>\n'
        '    <span class="k">steps:</span>\n'
        '      - <span class="k">uses:</span> <span class="s">actions/checkout@v4</span>\n'
        '      - <span class="k">uses:</span> <span class="s">actions/setup-node@v4</span>\n'
        '        <span class="k">with:</span> { <span class="k">node-version:</span> <span class="s">20</span> }\n'
        '      - <span class="k">run:</span> <span class="s">npm ci</span>\n'
        '      - <span class="k">run:</span> <span class="s">npm test</span>\n'
        '      - <span class="k">run:</span> <span class="s">npm run build</span>'
     ),
     "notes": [
        "<strong>on</strong> : déclenché par push sur main et par toute PR",
        "<strong>jobs.build</strong> : 1 job, sur un runner Ubuntu",
        "<strong>uses</strong> : on réutilise des actions du Marketplace",
        "<strong>run</strong> : on exécute nos commandes shell",
        ("Si un step échoue → le job est rouge → la PR est bloquée",),
     ]},

    {"t": "content", "title": "Secrets & sécurité", "img": L + "github.svg", "logo": True,
     "intro": "Jamais de mot de passe en clair dans le YAML : on utilise des <strong>Secrets</strong> chiffrés.",
     "bullets": [
        "Stockés dans <strong>Settings ▸ Secrets</strong>, masqués dans les logs",
        "Lus via <code>${{ secrets.SSH_KEY }}</code>",
        "Permissions minimales du <code>GITHUB_TOKEN</code> (least privilege)",
        ("Un scan de sécurité dans le pipeline = bénéfice sécu en plus",),
     ]},

    # ============== PARTIE 4 : CAS PRATIQUE & SYNTHÈSE ==============
    {"t": "section", "num": "PARTIE 4", "title": "Cas pratique", "sub": "QuickBite : du commit à la production"},

    {"t": "content", "title": "QuickBite : le pipeline en action", "img": D + "cicd-pipeline.svg",
     "intro": "Un développeur pousse une fonctionnalité. Voici ce qui se passe <strong>sans intervention humaine</strong>.",
     "bullets": [
        "1. Push → GitHub Actions démarre le workflow",
        "2. Tests + lint + build → ✅ vert",
        "3. Image Docker construite et poussée au registry",
        "4. Déploiement automatique → clients servis en <strong>minutes</strong>",
     ]},

    {"t": "content", "title": "Synthèse : CI/CD = agilité concrète", "img": D + "value-loop.svg",
     "intro": "La technique au service du métier : <strong>livrer de la valeur, vite et en confiance</strong>.",
     "benef": [
        ("b", "Agilité", "boucle idée → prod → feedback raccourcie"),
        ("g", "Qualité", "le pipeline protège chaque livraison"),
        ("b", "Valeur business", "time-to-market et satisfaction client"),
        ("g", "GitHub Actions", "le moteur, intégré et simple à adopter"),
     ]},

    {"t": "endsection", "num": "", "title": "Merci !", "sub": "Questions / Réponses — Haithem Mihoubi"},
]


def render():
    parts = []
    total = len(SLIDES)
    for idx, s in enumerate(SLIDES):
        t = s["t"]
        if t == "title":
            parts.append(f"""<section class="slide title-slide">
<div class="band top"></div>
<div class="brand">FORMATION DEVOPS</div>
<h1>{TITLE}</h1>
<div class="sub">{SUB}</div>
<div class="author">Formateur : {AUTHOR}</div>
<div class="band bottom"></div>
</section>""")
        elif t in ("section", "endsection"):
            parts.append(f"""<section class="slide section-slide">
<div class="modnum">{s.get('num','')}</div>
<div class="accent"></div>
<h1>{s['title']}</h1>
<div class="sub">{s.get('sub','')}</div>
</section>""")
        elif t == "full":
            parts.append(f"""<section class="slide content-slide">
<h2>{s['title']}</h2>
<p class="intro">{s.get('intro','')}</p>
<div class="full"><img src="{s['img']}"/></div>
<div class="foot"><span>Formation DevOps — H. Mihoubi</span><span>{idx+1} / {total}</span></div>
</section>""")
        elif t == "code":
            notes = bullets_html(s.get("notes", []))
            pill = f'<div class="pill">{s["pill"]}</div>' if s.get("pill") else ""
            parts.append(f"""<section class="slide content-slide">
<h2>{s['title']}</h2>
<div class="row">
<div class="codecol">{pill}<pre>{s['code']}</pre></div>
<div class="codenote">{notes}</div>
</div>
<div class="foot"><span>Formation DevOps — H. Mihoubi</span><span>{idx+1} / {total}</span></div>
</section>""")
        else:  # content
            logo = " logo" if s.get("logo") else ""
            body = f'<p class="intro">{s.get("intro","")}</p>'
            if s.get("benef"):
                body += benef_html(s["benef"])
            else:
                body += bullets_html(s.get("bullets", []))
            parts.append(f"""<section class="slide content-slide">
<h2>{s['title']}</h2>
<div class="row">
<div class="txt">{body}</div>
<div class="pic{logo}"><img src="{s['img']}"/></div>
</div>
<div class="foot"><span>Formation DevOps — H. Mihoubi</span><span>{idx+1} / {total}</span></div>
</section>""")
    return "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body>" + "".join(parts) + "</body></html>"


def main():
    illu = os.path.join(HERE, "make_diagrams.py")
    if os.path.exists(illu):
        subprocess.run([sys.executable, illu], check=True)
    html = render()
    HTML(string=html, base_url=HERE).write_pdf(OUT, stylesheets=[CSS])
    # copie dans le dossier pdfs/ central
    import shutil
    shutil.copy(OUT, PDFS)
    print(f"OK -> {OUT}  ({os.path.getsize(OUT)//1024} KB, {len(SLIDES)} slides)")
    print(f"OK -> {PDFS}")


if __name__ == "__main__":
    main()
