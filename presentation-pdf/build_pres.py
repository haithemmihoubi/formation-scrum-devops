#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Présentation PDF 16:9 « explique tout petit à petit », avec images.
Markdown-libre : on écrit directement le HTML des slides puis weasyprint -> PDF."""
import os
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "Presentation-Cours-Illustree.pdf")
CSS = os.path.join(HERE, "slides.css")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

TITLE = "Agilité, DevOps &amp; Sécurité"
SUB = "Le cours expliqué pas à pas, en images"
AUTHOR = "Haithem Mihoubi"

D = "img/diagrams/"   # schémas dessinés
L = "img/"            # logos


def bullets_html(items):
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append(f'<li class="sub">{it[0]}</li>')
        else:
            out.append(f'<li>{it}</li>')
    return "<ul>" + "".join(out) + "</ul>"


# Chaque slide : dict décrivant le type
SLIDES = [
    {"t": "title"},

    {"t": "content", "title": "Comment lire cette présentation", "img": D + "feedback-loop.svg",
     "intro": "On avance <strong>pas à pas</strong> : pour chaque notion, le problème, l'explication, et un schéma.",
     "bullets": [
        "3 modules : <strong>Agilité</strong>, <strong>DevOps</strong>, <strong>Spring Security</strong>",
        "Un fil rouge unique : l'application <strong>QuickBite</strong>",
        ("Chaque slide = une seule idée, illustrée",),
     ]},

    # ================= MODULE 1 =================
    {"t": "section", "num": "MODULE 1", "title": "Agilité", "sub": "Scrum &amp; Kanban"},

    {"t": "content", "title": "Le problème de départ", "img": D + "waterfall-vs-agile.svg",
     "intro": "Avant l'Agilité, on faisait tout en <strong>cascade</strong> : spécifier, développer, puis livrer 12 à 18 mois plus tard.",
     "bullets": [
        "Effet tunnel : le client ne voit rien avant la fin",
        "Les besoins ont changé entre-temps → produit périmé",
        "Le coût du changement explose avec le temps",
     ]},
    {"t": "content", "title": "L'idée de l'Agilité", "img": D + "waterfall-vs-agile.svg",
     "intro": "Si on ne peut pas tout prévoir, organisons-nous pour <strong>apprendre et corriger vite</strong>.",
     "bullets": [
        "Livrer un <strong>petit morceau utilisable</strong> toutes les 2-3 semaines",
        "Montrer à de vrais utilisateurs, recueillir leur avis, ajuster",
        ("Un grand pari risqué devient une série de petits paris corrigeables",),
     ]},
    {"t": "content", "title": "Le Manifeste Agile (2001)", "img": D + "feedback-loop.svg",
     "intro": "Quatre <strong>valeurs</strong> : « A plutôt que B » — B garde de la valeur, mais on privilégie A.",
     "bullets": [
        "Les individus et interactions &gt; les processus et outils",
        "Un logiciel qui marche &gt; une documentation exhaustive",
        "La collaboration client &gt; la négociation de contrat",
        "L'adaptation au changement &gt; le suivi d'un plan",
     ]},
    {"t": "content", "title": "La boucle de feedback", "img": D + "feedback-loop.svg",
     "intro": "Le cœur de l'Agilité : <strong>construire → mesurer → apprendre</strong>, en boucle.",
     "bullets": [
        "Plus la boucle est courte, plus on corrige tôt",
        "Corriger tôt coûte beaucoup moins cher",
        ("MVP : la plus petite version qui permet déjà d'apprendre",),
     ]},
    {"t": "content", "title": "Scrum : le cadre", "img": L + "scrum.svg",
     "intro": "Scrum organise le travail en <strong>sprints</strong> (itérations de durée fixe, 1 à 4 semaines).",
     "bullets": [
        "3 piliers : transparence, inspection, adaptation",
        "Événements : Planning, Daily, Review, Rétrospective",
        "Artefacts : Product Backlog, Sprint Backlog, Increment",
     ]},
    {"t": "content", "title": "Scrum : les 3 rôles", "img": L + "scrum.svg",
     "intro": "Une seule équipe, sans hiérarchie, avec trois responsabilités.",
     "bullets": [
        "<strong>Product Owner</strong> : le quoi et le pourquoi (priorise la valeur)",
        "<strong>Scrum Master</strong> : facilite, lève les obstacles (≠ chef de projet)",
        "<strong>Développeurs</strong> : auto-organisés, le comment",
     ]},
    {"t": "content", "title": "User stories & estimation", "img": D + "feedback-loop.svg",
     "intro": "On décrit le besoin côté utilisateur : « En tant que… je veux… afin de… ».",
     "bullets": [
        "Critères <strong>INVEST</strong> pour une bonne story",
        "Estimation en <strong>points</strong> (Fibonacci), pas en heures",
        "Priorisation <strong>MoSCoW</strong> : Must / Should / Could / Won't",
     ]},
    {"t": "full", "title": "Kanban : visualiser & limiter le travail", "img": L + "kanban.svg",
     "intro": "On visualise le flux sur un tableau et on <strong>limite le travail en cours (WIP)</strong> — « stop starting, start finishing ». Loi de Little : Lead time ≈ WIP ÷ Throughput."},

    # ================= MODULE 2 =================
    {"t": "section", "num": "MODULE 2", "title": "DevOps", "sub": "CI/CD · Docker · Kubernetes"},

    {"t": "content", "title": "DevOps : briser le mur", "img": D + "devops-loop.svg",
     "intro": "Réunir <strong>Dev</strong> (le changement) et <strong>Ops</strong> (la stabilité) par la culture et l'automatisation.",
     "bullets": [
        "<strong>CAMS</strong> : Culture, Automation, Measurement, Sharing",
        "But : raccourcir le délai idée → production, de façon fiable",
        ("Métriques DORA : fréquence, délai, taux d'échec, MTTR",),
     ]},
    {"t": "content", "title": "Intégration & livraison continues", "img": D + "cicd-pipeline.svg",
     "intro": "À chaque commit, un <strong>pipeline</strong> teste, construit et prépare le déploiement.",
     "bullets": [
        "<strong>CI</strong> : tester à chaque changement",
        "<strong>CD</strong> : toujours déployable (puis déploiement auto)",
        "Règle d'or : on ne fusionne jamais un pipeline rouge",
     ]},
    {"t": "content", "title": "Git : le travail collaboratif", "img": L + "git.svg", "logo": True,
     "intro": "Tout part du code, géré avec <strong>Git</strong> : branches courtes + Pull Requests + revue.",
     "bullets": [
        "Conventional Commits : feat, fix, docs, refactor…",
        "GitHub / GitLab : pipelines intégrés",
        ("Branches courtes = fusions faciles",),
     ]},
    {"t": "content", "title": "Docker : la conteneurisation", "img": L + "docker.svg", "logo": True,
     "intro": "Empaqueter l'application <strong>avec son environnement</strong> → « ça marche partout ».",
     "bullets": [
        "Image (le modèle) vs Conteneur (l'instance)",
        "Dockerfile multi-stage → image légère",
        "Docker Compose : plusieurs services en une commande",
     ]},
    {"t": "full", "title": "Conteneur vs machine virtuelle", "img": D + "container-vs-vm.svg",
     "intro": "Le conteneur <strong>partage le noyau</strong> de l'hôte : léger, démarre en millisecondes. La VM embarque un OS complet : lourde, démarre en minutes."},
    {"t": "content", "title": "Kubernetes : l'orchestration", "img": L + "kubernetes.svg", "logo": True,
     "intro": "En production : redémarrage auto, mise à l'échelle, déploiement <strong>sans coupure</strong>.",
     "bullets": [
        "<strong>Pod</strong> (unité), <strong>Deployment</strong> (réplicas), <strong>Service</strong> (adresse stable)",
        "<strong>Ingress</strong> (accès externe), ConfigMap / Secret",
        "Déclaratif : on décrit l'état souhaité, K8s converge",
     ]},
    {"t": "full", "title": "Architecture Kubernetes", "img": D + "k8s-arch.svg",
     "intro": "Un <strong>Control Plane</strong> (le cerveau) pilote des <strong>Nodes</strong> (machines) qui exécutent les Pods."},
    {"t": "content", "title": "Observabilité", "img": L + "grafana.svg", "logo": True,
     "intro": "Voir ce qui se passe en production : logs, <strong>métriques</strong>, traces.",
     "bullets": [
        "<strong>Prometheus</strong> collecte les métriques",
        "<strong>Grafana</strong> affiche les tableaux de bord",
        "4 signaux dorés : latence, trafic, erreurs, saturation",
     ]},

    # ================= MODULE 3 =================
    {"t": "section", "num": "MODULE 3", "title": "Spring Security", "sub": "JWT · OAuth2 · Keycloak"},

    {"t": "full", "title": "Authentification vs Autorisation", "img": D + "authn-authz.svg",
     "intro": "<strong>AuthN</strong> = « qui es-tu ? » (vient en premier). <strong>AuthZ</strong> = « as-tu le droit ? ». 401 = non authentifié · 403 = authentifié mais sans droit."},
    {"t": "content", "title": "Spring Security 6", "img": L + "spring.svg", "logo": True,
     "intro": "La sécurité s'insère comme une <strong>chaîne de filtres</strong> devant l'application.",
     "bullets": [
        "Bean <strong>SecurityFilterChain</strong> (WebSecurityConfigurerAdapter supprimé)",
        "Mots de passe : <strong>BCrypt</strong> / Argon2 (jamais en clair)",
        "RBAC : @PreAuthorize(\"hasRole('ADMIN')\")",
     ]},
    {"t": "full", "title": "JWT : un jeton auto-porteur", "img": D + "jwt-structure.svg",
     "intro": "Le JWT contient l'identité, est <strong>signé</strong> (donc vérifiable sans base) mais <strong>pas chiffré</strong> : son contenu est lisible. Access token court + refresh token long avec rotation."},
    {"t": "full", "title": "OAuth2 / OpenID Connect", "img": D + "oauth-flow.svg",
     "intro": "<strong>OAuth2</strong> délègue l'autorisation ; <strong>OIDC</strong> ajoute l'authentification (qui est l'utilisateur). Flow recommandé : Authorization Code + PKCE."},
    {"t": "content", "title": "Keycloak", "img": L + "keycloak.png", "logo": True,
     "intro": "Serveur d'identité (IAM) : l'API devient un <strong>resource server</strong> qui valide les tokens.",
     "bullets": [
        "Realm (espace isolé), Client, Roles, Mappers",
        "SSO : « se connecter avec… »",
        ("Mapper realm_access.roles → ROLE_* (cause n°1 des 403)",),
     ]},
    {"t": "content", "title": "Durcissement & OWASP", "img": L + "oauth.svg", "logo": True,
     "intro": "Sécuriser pour de vrai : on applique une <strong>check-list</strong>.",
     "bullets": [
        "CORS (permission) ≠ CSRF (attaque)",
        "Rate limiting, exceptions neutres, audit",
        "Risque n°1 OWASP : <strong>Broken Access Control</strong>",
     ]},

    # ================= PROJET & FIN =================
    {"t": "section", "num": "PROJET FIL ROUGE", "title": "QuickBite", "sub": "On construit, déploie et sécurise une vraie API"},
    {"t": "content", "title": "QuickBite : atelier après atelier", "img": L + "postman.png", "logo": True,
     "intro": "Une API Spring Boot qui grandit en appliquant chaque notion du cours.",
     "bullets": [
        "Sécurité de base → RBAC → JWT → Keycloak → durcissement",
        "DevOps : Docker → CI → Kubernetes",
        "Tests fournis : collection <strong>Postman</strong>",
     ]},
    {"t": "content", "title": "Synthèse du cursus", "img": D + "devops-loop.svg",
     "intro": "Trois disciplines, un seul objectif : <strong>livrer de la valeur, en confiance</strong>.",
     "bullets": [
        "<strong>Agile</strong> : construire le bon produit",
        "<strong>DevOps</strong> : le livrer vite et sûrement",
        "<strong>Sécurité</strong> : protéger ce qui est livré",
     ]},
    {"t": "endsection", "num": "", "title": "Merci !", "sub": "Questions / Réponses — Haithem Mihoubi"},
]


def render():
    parts = []
    n_content = 0
    total = len(SLIDES)
    for idx, s in enumerate(SLIDES):
        t = s["t"]
        if t == "title":
            parts.append(f"""<section class="slide title-slide">
<div class="band top"></div>
<div class="brand">SOLID WALL CONSULTING</div>
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
            n_content += 1
            parts.append(f"""<section class="slide content-slide">
<h2>{s['title']}</h2>
<p class="intro">{s.get('intro','')}</p>
<div class="full"><img src="{s['img']}"/></div>
<div class="foot"><span>Solid Wall — H. Mihoubi</span><span>{idx+1} / {total}</span></div>
</section>""")
        else:  # content
            n_content += 1
            logo = " logo" if s.get("logo") else ""
            parts.append(f"""<section class="slide content-slide">
<h2>{s['title']}</h2>
<div class="row">
<div class="txt"><p class="intro">{s.get('intro','')}</p>{bullets_html(s.get('bullets', []))}</div>
<div class="pic{logo}"><img src="{s['img']}"/></div>
</div>
<div class="foot"><span>Solid Wall — H. Mihoubi</span><span>{idx+1} / {total}</span></div>
</section>""")
    return "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body>" + "".join(parts) + "</body></html>"


def main():
    html = render()
    HTML(string=html, base_url=HERE).write_pdf(OUT, stylesheets=[CSS])
    print(f"OK -> {OUT}  ({os.path.getsize(OUT)//1024} KB, {len(SLIDES)} slides)")


if __name__ == "__main__":
    main()
