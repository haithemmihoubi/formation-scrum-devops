# -*- coding: utf-8 -*-
"""Contenu de la presentation. Modifiable librement puis regenerer avec make_pptx.py."""

TITLE = "Agilite, DevOps & Securite"
SUBTITLE = "Scrum & Kanban - CI/CD, Docker, Kubernetes - Spring Security"
AUTHOR = "Haithem Mihoubi"

# Chaque slide : {"type": "section"|"content", ...}
#  - section : title, subtitle
#  - content : title, bullets (str ou (str, niveau))
SLIDES = [
    # ===== Agenda =====
    {"type": "content", "title": "Programme de la formation", "bullets": [
        "Module 1 - Gestion de projet Agile : Scrum & Kanban (3 jours)",
        "Module 2 - Culture & outils DevOps : CI/CD, Docker, Kubernetes (4 jours)",
        "Module 3 - Spring Security : JWT, OAuth2, Keycloak (5 jours)",
        ("Fil rouge : application QuickBite (commande de repas)", 1),
        ("Pedagogie : theorie courte -> demonstration -> atelier -> corrige", 1),
    ]},

    # ===================== MODULE 1 =====================
    {"type": "section", "title": "Module 1 - Agilite", "subtitle": "Scrum & Kanban, roles PO / Scrum Master"},

    # Jour 1
    {"type": "content", "title": "Pourquoi l'Agilite ?", "bullets": [
        "Avant : cycle en cascade - tout specifier, puis livrer 12-18 mois plus tard",
        "Consequences : effet tunnel, besoins perimes, fonctions inutilisees",
        "Le cout du changement explose avec le temps",
        "Reponse : livrer par petits increments et apprendre vite",
        ("Idee cle : raccourcir la boucle entre une idee et sa validation utilisateur", 1),
    ]},
    {"type": "content", "title": "Le Manifeste Agile (2001) - 4 valeurs", "bullets": [
        "Les individus et leurs interactions  plutot que  les processus et outils",
        "Un logiciel qui fonctionne  plutot que  une documentation exhaustive",
        "La collaboration avec le client  plutot que  la negociation contractuelle",
        "L'adaptation au changement  plutot que  le suivi d'un plan",
        ("Les elements de droite gardent de la valeur - on deplace le curseur", 1),
    ]},
    {"type": "content", "title": "Les 12 principes (regroupes)", "bullets": [
        "Livrer de la valeur tot et souvent, accueillir le changement meme tardif",
        "Collaboration quotidienne metier <-> developpeurs, dialogue en face a face",
        "Mesure d'avancement = logiciel qui marche, a un rythme soutenable",
        "Excellence technique, simplicite, equipes auto-organisees",
        "S'ameliorer regulierement : retrospective a intervalles reguliers",
    ]},
    {"type": "content", "title": "Predictif vs Adaptatif", "bullets": [
        "Predictif (cycle en V) : besoin stable, valeur a la fin, changement couteux",
        "Adaptatif (Agile) : besoin evolutif, valeur a chaque iteration",
        "Iteratif ≠ incremental - l'Agile combine les deux",
        ("Metaphore : skateboard -> trottinette -> velo -> voiture", 1),
    ]},
    {"type": "content", "title": "Concepts cles", "bullets": [
        "MVP : plus petite version livrable qui permet d'apprendre aupres d'utilisateurs reels",
        "Valeur metier : on priorise par la valeur, pas par la facilite technique",
        "Boucle de feedback : construire -> mesurer -> apprendre",
        "Definition of Ready (DoR) : story prete a etre developpee",
        "Definition of Done (DoD) : reellement termine - checklist non negociable",
    ]},

    # Jour 2
    {"type": "content", "title": "Scrum - les fondations", "bullets": [
        "Cadre leger fonde sur l'empirisme : transparence, inspection, adaptation",
        "5 valeurs Scrum : Engagement - Focus - Ouverture - Respect - Courage",
        ("Engagement : l'equipe s'engage sur l'objectif du sprint, pas une simple liste de taches", 1),
        ("Focus : rien ne prime sur l'objectif du sprint pendant sa duree", 1),
        "Sprint = iteration de duree fixe (1 a 4 semaines), sans interruption",
    ]},
    {"type": "content", "title": "Scrum - les 3 roles", "bullets": [
        "Product Owner : le QUOI et le POURQUOI - possede et ordonne le Product Backlog",
        ("Outils PO : story mapping, MoSCoW, WSJF, roadmap produit, criteres d'acceptation", 1),
        "Scrum Master : leader serviteur - facilite, leve les obstacles, protege l'equipe",
        ("≠ chef de projet : influence et coaching, pas autorite hierarchique", 1),
        "Developpeurs : auto-organises, pluridisciplinaires - decident du COMMENT",
    ]},
    {"type": "content", "title": "Story Mapping - outil cle du PO", "bullets": [
        "Visualise le parcours utilisateur de gauche a droite (activites -> taches utilisateur)",
        "Decoupe verticalement les priorites en tranches horizontales (releases / sprints)",
        "Permet de definir le MVP : la premiere tranche bout-en-bout fonctionnelle",
        "Revele les dependances et les risques avant de planifier",
        ("Format : post-it sur un mur ou outil dedie - toujours realise en equipe", 1),
    ]},
    {"type": "content", "title": "Scrum - artefacts & evenements", "bullets": [
        "Artefacts : Product Backlog (Product Goal) | Sprint Backlog (Sprint Goal) | Increment (DoD)",
        "Sprint Planning (≤ 4 h) : Pourquoi ce sprint a de la valeur ? Quoi ? Comment ?",
        "Daily Scrum (15 min) : synchronisation entre developpeurs, pas un reporting",
        "Sprint Review (≤ 2 h) : inspecter le PRODUIT avec les parties prenantes",
        "Sprint Retrospective (≤ 1 h 30) : inspecter le PROCESSUS de travail",
    ]},
    {"type": "content", "title": "Ecrire & estimer le travail", "bullets": [
        "Epic -> User Story -> Task",
        "Story : En tant que [role], je veux [action] afin de [benefice]",
        "INVEST : Independent, Negotiable, Valuable, Estimable, Small, Testable",
        "Estimation en points (Fibonacci) + Planning Poker, pas en heures",
        "Priorisation MoSCoW : Must / Should / Could / Won't",
    ]},

    # Jour 3
    {"type": "content", "title": "Kanban - principes & pratiques", "bullets": [
        "Visualiser le travail sur un tableau (colonnes = etapes du flux)",
        "Limiter le WIP (Work In Progress) : 'stop starting, start finishing'",
        "Gerer le flux : rendre les regles explicites, boucles de feedback cadencees",
        "Metriques : lead time (vu client), cycle time (temps d'execution), throughput",
        "Loi de Little : Lead time ≈ WIP / Throughput - reduire le WIP reduit les delais",
    ]},
    {"type": "content", "title": "Kanban avance - CFD & classes de service", "bullets": [
        "Diagramme de flux cumule (CFD) : courbes empilees par etat dans le temps",
        ("Bande qui s'elargit = accumulation / goulot d'etranglement visible", 1),
        ("Bandes paralleles et fines = flux sain et previsible", 1),
        "Classes de service : Standard | Urgent (expedite, WIP=1) | Date fixe | Intangible",
        "Optimiser le TOUT, pas chaque poste isolement (theorie des contraintes)",
    ]},
    {"type": "content", "title": "Scrum vs Kanban vs ScrumBan", "bullets": [
        "Scrum : iterations fixes, roles imposes, Sprint Goal - developpement produit",
        "Kanban : flux continu, pas de roles imposes - support, ops, flux imprevisible",
        "ScrumBan : hybride - equipe Scrum noyee d'urgences, ou equipe en transition",
        ("Pas de meilleur cadre : on choisit selon la nature du travail", 1),
    ]},
    {"type": "content", "title": "Outils de gestion Agile", "bullets": [
        "Jira : puissant, reporting avance, Agile a l'echelle - grandes equipes produit",
        "Trello : simplicite, prise en main immediate - petites equipes, Kanban leger",
        "ClickUp : polyvalent (docs, objectifs, vues multiples) - equipes multi-usages",
        "GitHub Projects : couple au code et aux issues, automatisation - equipes dev",
        ("Asana : gestion de taches et de flux, echeances - coordination transverse", 1),
    ]},
    {"type": "content", "title": "Module 1 - Ateliers pratiques", "bullets": [
        "Atelier 1 (Jour 1) : Diagnostic d'un projet cascade -> proposition de transition Agile",
        "Atelier 2 (Jour 2) : Creer un Product Backlog QuickBite + Sprint Planning (Planning Poker)",
        "Atelier 3 (Jour 3) : Mettre en place un tableau Kanban + simuler 5 jours de flux",
        ("Mini-atelier outil : creer le board QuickBite sur Trello ou GitHub Projects", 1),
        ("Chaque atelier se clot par une restitution et un corrige commente", 1),
    ]},

    # ===================== MODULE 2 =====================
    {"type": "section", "title": "Module 2 - DevOps", "subtitle": "CI/CD, Docker, Kubernetes"},

    # Jour 1
    {"type": "content", "title": "DevOps, c'est quoi ?", "bullets": [
        "Briser le mur entre Dev (changement) et Ops (stabilite)",
        "Une culture + des pratiques, pas un metier ni un outil",
        "CAMS : Culture, Automation, Measurement, Sharing",
        "But : raccourcir le delai idee -> production, de facon fiable et repetable",
    ]},
    {"type": "content", "title": "Mesurer : les metriques DORA", "bullets": [
        "Deployment Frequency : a quelle frequence on deploie en production",
        "Lead Time for Changes : du commit au deploiement en prod",
        "Change Failure Rate : % de deploiements provoquant un incident",
        "MTTR (Mean Time To Restore) : delai de remise en service apres incident",
        ("Vitesse et stabilite ne s'opposent pas - les equipes elite excellent sur les 4", 1),
    ]},
    {"type": "content", "title": "CI / CD / CD", "bullets": [
        "CI - Integration Continue : tester a chaque commit, feedback en minutes",
        "CD - Livraison Continue : artefact toujours deployable (deploiement manuel)",
        "CD - Deploiement Continu : deploiement automatique en prod a chaque merge",
        "Cycle DevOps : Plan->Code->Build->Test->Release->Deploy->Operate->Monitor",
    ]},
    {"type": "content", "title": "Git Flow & strategies de branches", "bullets": [
        "Git Flow : branches main / develop / feature / release / hotfix - releases planifiees",
        "GitHub Flow : main + branches courtes + PR + deploiement continu - SaaS web",
        "Trunk-Based : commits frequents sur main + feature flags - equipes matures",
        "Conventional Commits : feat / fix / docs / refactor / test / chore",
        ("Regle d'or : branches courtes, integrations frequentes, CI toujours verte", 1),
    ]},
    {"type": "content", "title": "Pipeline CI - outils & anatomie", "bullets": [
        "Etapes typiques : checkout -> install -> lint -> build -> tests -> artefact",
        "GitHub Actions : YAML dans .github/workflows/ - integre a GitHub, gratuit",
        "GitLab CI : .gitlab-ci.yml, runners integres, tout-en-un (DevSecOps)",
        "Jenkins : serveur CI open source, tres configurable, Groovy pipelines, plugins",
        ("On ne fusionne jamais une branche avec un pipeline rouge", 1),
    ]},

    # Jour 2
    {"type": "content", "title": "Docker - conteneurisation", "bullets": [
        "Empaqueter l'app + son environnement -> marche partout",
        "Conteneur : partage le noyau de l'hote -> leger, demarre en millisecondes",
        "VM : embarque un OS complet -> lourd, demarre en minutes",
        "Image (modele) vs Conteneur (instance) ; volumes, reseaux, registres",
    ]},
    {"type": "content", "title": "Docker - Dockerfile & Compose", "bullets": [
        "Dockerfile multi-stage : build separe du runtime -> image finale legere",
        "Ordonner du moins au plus changeant (exploiter le cache des couches)",
        "Ne pas tourner en root ; jamais de secret dans une couche d'image",
        "Docker Compose : plusieurs services (app + base de donnees) en une commande",
        ("Registres d'images : Docker Hub, GitHub Container Registry (GHCR)", 1),
    ]},

    # Jour 3
    {"type": "content", "title": "Kubernetes - orchestration", "bullets": [
        "Redemarrage auto, mise a l'echelle, deploiement sans coupure (rolling update)",
        "Pod (unite), Deployment (replicas + rollback), Service (adresse reseau stable)",
        "Ingress (acces HTTP externe), ConfigMap / Secret, Namespace (isolation)",
        "Approche declarative : on decrit l'etat souhaite, K8s converge en continu",
    ]},
    {"type": "content", "title": "Kubernetes - RBAC & securite", "bullets": [
        "RBAC : Role -> RoleBinding -> qui peut faire quoi sur quelles ressources",
        "Bonnes pratiques : moindre privilege, conteneurs non-root, resources.limits",
        "readinessProbe : Pod pret a recevoir du trafic ? Sinon retire du load balancer",
        "livenessProbe : Pod vivant ? Sinon redemarrage automatique par K8s",
        ("Namespace + Secrets + NetworkPolicies : isoler les environnements (dev/prod)", 1),
    ]},

    # Jour 4
    {"type": "content", "title": "Aller plus loin : Helm, observabilite, GitOps", "bullets": [
        "Helm : packager et parametrer les manifestes K8s (templates + values.yaml)",
        "Observabilite - 3 piliers : logs, metriques (Prometheus), traces distribuees",
        "4 signaux dores (Google SRE) : latence, trafic, erreurs, saturation",
        "Grafana : dashboards sur les metriques Prometheus (requetes PromQL)",
        "GitOps (Argo CD) : Git = source de verite, synchro automatique avec le cluster",
    ]},
    {"type": "content", "title": "Module 2 - Ateliers pratiques", "bullets": [
        "Atelier 1 (Jour 1) : Pipeline CI sur GitHub Actions ou GitLab CI - bloquer la fusion si rouge",
        "Atelier 2 (Jour 2) : Conteneuriser QuickBite API + PostgreSQL via Docker Compose",
        "Atelier 3 (Jour 3) : Deployer sur Minikube/K3s - Ingress, ConfigMap, scale, rollback",
        "Atelier 4 (Jour 4) : Chaine complete CI/CD -> Docker -> Kubernetes -> Helm -> Grafana",
        ("Bonus : brancher Argo CD - un commit Git declenche le deploiement automatique", 1),
    ]},

    # ===================== MODULE 3 =====================
    {"type": "section", "title": "Module 3 - Spring Security", "subtitle": "Authentification, JWT, OAuth2, Keycloak"},

    # Jour 1
    {"type": "content", "title": "Authentification vs Autorisation", "bullets": [
        "AuthN : Qui es-tu ? (identite) - vient en premier",
        "AuthZ : As-tu le droit ? (permissions) - vient apres l'authentification",
        "Authentifie ≠ autorise : les deux controles sont distincts et obligatoires",
        ("401 = non authentifie | 403 = authentifie mais sans droit", 1),
    ]},
    {"type": "content", "title": "Stateful vs Stateless & mots de passe", "bullets": [
        "Stateful : session cote serveur (JSESSIONID) - scalabilite difficile",
        "Stateless : token (JWT) - ideal API REST / microservices, scale horizontal",
        "Mots de passe : jamais en clair -> hachage lent + sale (sel integre)",
        "BCrypt (work factor 12+) / Argon2 - MD5 et SHA seuls sont interdits",
    ]},
    {"type": "content", "title": "Attaques courantes & parades", "bullets": [
        "Brute force -> hachage lent, rate limiting, lockout, MFA",
        "MITM -> HTTPS/TLS partout, HSTS",
        "XSS -> echapper les sorties, CSP, cookies HttpOnly",
        "CSRF -> token anti-CSRF, SameSite, ou API stateless",
        "Injection SQL -> requetes parametrees / ORM",
        ("Credential stuffing -> MFA, detection d'anomalies, alertes sur fuites connues", 1),
    ]},
    {"type": "content", "title": "Architecture Spring Security 6", "bullets": [
        "Chaine de filtres (SecurityFilterChain) devant l'application",
        "AuthenticationManager -> AuthenticationProvider -> UserDetailsService",
        "SecurityContext : porte l'utilisateur authentifie pour toute la requete",
        ("WebSecurityConfigurerAdapter supprime -> bean SecurityFilterChain + lambdas", 1),
    ]},

    # Jour 2
    {"type": "content", "title": "Authentification avancee", "bullets": [
        "Form login & Basic Auth : pour applications web classiques (HTTPS obligatoire)",
        "Custom UserDetailsService : charger les utilisateurs depuis la base de donnees",
        "PasswordEncoder : BCrypt recommande ; DelegatingPasswordEncoder pour migrer",
        "Authentification multi-layer : combiner Basic/Token + MFA pour les zones sensibles",
        ("Toujours renvoyer un message generique a l'echec - ne pas reveler login vs mdp", 1),
    ]},
    {"type": "content", "title": "Autorisation RBAC", "bullets": [
        "Role (grossier : ADMIN) vs Permission (fin : order:read)",
        "Modele mature : Utilisateur -> Roles -> Permissions",
        "@EnableMethodSecurity + @PreAuthorize(\"hasRole('ADMIN')\")",
        "@PostAuthorize : filtrer selon l'objet retourne | @Secured : annotation legacy",
        ("Piege : hasRole('ADMIN') attend l'autorite ROLE_ADMIN en base", 1),
    ]},

    # Jour 3
    {"type": "content", "title": "JWT - JSON Web Token", "bullets": [
        "Auto-porteur et SIGNE -> verifiable sans appeler la base (stateless)",
        "3 parties : header (algo) . payload (claims) . signature (integrite)",
        "Signe ≠ chiffre : le payload est LISIBLE -> aucune donnee sensible dedans",
        "Access token court (15 min) + refresh token long (7 j, rotation obligatoire)",
        ("JWTAuthenticationFilter + JWTAuthorizationFilter dans la SecurityFilterChain", 1),
    ]},

    # Jour 4
    {"type": "content", "title": "OAuth2 - les flows", "bullets": [
        "Authorization Code + PKCE : RECOMMANDE - web, mobile, SPA (securise)",
        "Client Credentials : machine a machine, pas d'utilisateur implique",
        "Device Code : appareils sans clavier (TV, IoT)",
        ("Implicit Flow : DECONSEILLE - remplace par Authorization Code + PKCE", 1),
        ("Password (ROPC) : DECONSEILLE - expose les identifiants a l'application", 1),
    ]},
    {"type": "content", "title": "OAuth2 & OpenID Connect", "bullets": [
        "OAuth2 : autorisation deleguee (acces a des ressources en mon nom)",
        "OIDC : couche d'authentification au-dessus d'OAuth2 + ID token",
        "ID token (pour le client, qui est l'utilisateur) ≠ Access token (pour l'API)",
        "PKCE : code_verifier secret + code_challenge - protege les clients publics",
        ("Spring : oauth2Login() pour le client | oauth2ResourceServer() pour l'API", 1),
    ]},
    {"type": "content", "title": "Keycloak", "bullets": [
        "Serveur d'identite open source (IAM) : authentification, SSO, federation",
        "Realm (espace isole), Client (application), Roles (realm ou client), Mappers",
        "API Spring = resource server qui valide les tokens via issuer-uri (JWKS)",
        ("Mapper realm_access.roles -> ROLE_* : cause n°1 des 403 avec Keycloak", 1),
        ("Alternative : Spring Authorization Server - serveur OAuth2/OIDC natif Spring", 1),
    ]},

    # Jour 5
    {"type": "content", "title": "Securite avancee - WebSocket & microservices", "bullets": [
        "WebSocket : desactiver CSRF pour le endpoint WS | SockJS necessite config CORS",
        "Intercepteurs de messages : @MessageMapping protege par @PreAuthorize",
        "Microservices : API Gateway centralise AuthN, rate limiting, terminaison TLS",
        "Rotation des cles JWT (JWKS + kid) - limiter l'impact d'une compromission",
        ("Zero-trust : chaque service re-valide le token, meme en interne au cluster", 1),
    ]},
    {"type": "content", "title": "Durcissement & OWASP", "bullets": [
        "CORS (permission cross-domaine) ≠ CSRF (attaque contre les sessions)",
        "Rate limiting (Bucket4j / API Gateway), exceptions neutres, audit des acces",
        "Headers de securite : CSP, X-Frame-Options, X-Content-Type-Options, HSTS",
        "OWASP Top 1 : Broken Access Control -> verifier CHAQUE endpoint",
        ("Actuator : proteger les endpoints de monitoring, ne jamais tout exposer", 1),
    ]},
    {"type": "content", "title": "Module 3 - Ateliers pratiques", "bullets": [
        "Atelier 1 (Jour 1) : Premier projet Spring Boot 3 securise - SecurityFilterChain",
        "Atelier 2 (Jour 2) : UserDetailsService JPA + modele Role/Permission + Postman",
        "Atelier 3 (Jour 3) : API REST securisee JWT - login, refresh, rotation, 401/403",
        "Atelier 4 (Jour 4) : Keycloak Docker + resource server + front OAuth2/OIDC",
        "Atelier 5 (Jour 5) : Grand TP final - API JWT + RBAC + Keycloak + durcissement",
    ]},

    # ===================== PROJET & CONCLUSION =====================
    {"type": "section", "title": "Projet fil rouge", "subtitle": "QuickBite - une API qu'on construit, deploie et securise"},
    {"type": "content", "title": "QuickBite - atelier progressif", "bullets": [
        "A0-A1 : squelette Spring Boot + SecurityFilterChain + securite de base",
        "A2 : utilisateurs en base + RBAC (BCrypt, @PreAuthorize, roles/permissions)",
        "A3 : authentification JWT (login / refresh / rotation des tokens)",
        "A4 : OAuth2 / Keycloak (SSO, resource server, front protege en OIDC)",
        "A5 : durcissement (CORS, rate limit, exceptions, audit, OWASP checklist)",
        "DevOps : Docker -> CI GitHub Actions/GitLab/Jenkins -> Kubernetes -> Helm",
    ]},
    {"type": "content", "title": "Synthese du cursus", "bullets": [
        "Agile : construire LE BON produit, dans le bon ordre, avec les bonnes personnes",
        "DevOps : le livrer VITE et SUREMENT, de facon automatisee et tracable",
        "Securite : PROTEGER ce qui est livre, a chaque couche de la stack",
        ("Trois facettes d'un meme metier : livrer de la valeur, en confiance", 1),
    ]},
    {"type": "section", "title": "Merci !", "subtitle": "Questions / Reponses - Haithem Mihoubi"},
]
