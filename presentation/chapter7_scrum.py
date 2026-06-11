# -*- coding: utf-8 -*-
"""
Chapitre 7 - Introduction a Scrum.
Inseree au debut du Module 1 (Agilite / Scrum) de la presentation.

Format identique a slides_content.py :
  - {"type": "section", "title", "subtitle", ["note"]}
  - {"type": "content", "title", "bullets", ["image"]}
Les images (cle "image") sont des fichiers de presentation/img/.
"""

CH7_SLIDES = [
    # ----- Couverture du chapitre -----
    {"type": "section",
     "title": "Chapitre 7 - Introduction a Scrum",
     "subtitle": "Scrum.org  -  International Scrum Institute  -  Scrum Alliance",
     "note": "Improving the Profession of Software Development   |   18/12/2015   -   Copyright ISETR 2014 ©"},

    # Diapo 2 - Plan general
    {"type": "content", "title": "Plan general", "bullets": [
        "I.   Generalites sur Scrum",
        "II.  La theorie de Scrum",
        "III. Les roles Scrum",
        "IV.  Le fonctionnement de Scrum",
        "V.   Les evenements Scrum",
        "VI.  Les artefacts Scrum",
        "Conclusion",
    ]},

    # ===================== I. GENERALITES =====================
    {"type": "section", "title": "I. Generalites sur Scrum",
     "subtitle": "Definitions, historique, theorie et composition"},

    # Diapo 3 - Definitions fondamentales
    {"type": "content", "title": "I. Generalites - Definitions fondamentales", "bullets": [
        "Scrum EST :",
        ("Un cadre de travail (framework) pour repondre a des problemes complexes et changeants", 1),
        ("tout en livrant de maniere productive et creative des produits de la plus grande valeur", 1),
        "Scrum N'EST PAS :",
        ("Un processus ni une methode de developpement de produit logiciel", 1),
    ]},

    # Diapo 4 - Historique, Theorie, Composition
    {"type": "content", "title": "I. Generalites - Historique, theorie & composition", "bullets": [
        "Historique : le mot Scrum vient du Rugby (la melee)",
        ("Utilise dans le developpement logiciel depuis le debut des annees 90", 1),
        "Theorie : Transparence - Inspection - Adaptation",
        "Composition du cadre Scrum :",
        ("Equipes et roles  |  Evenements  |  Artefacts  |  Regles", 1),
    ]},

    # Diapo 5 - Metaphore de la melee (IMAGE)
    {"type": "content", "title": "I. Generalites - Metaphore de la melee", "bullets": [
        "Definition sportive : en Rugby, une melee est une reprise du jeu ordonnee apres une infraction mineure",
        "Symbolise la cohesion d'equipe necessaire pour affronter collectivement les obstacles de production",
        "L'effort est commun, oriente vers un meme objectif",
    ], "image": "melee.png"},

    # ===================== II. THEORIE =====================
    {"type": "section", "title": "II. La theorie de Scrum",
     "subtitle": "L'empirisme et ses trois piliers"},

    # Diapo 6 - L'empirisme (IMAGE)
    {"type": "content", "title": "II. La theorie - L'empirisme", "bullets": [
        "Principe de base : Scrum se base sur l'empirisme",
        "Processus empirique : Transparence, Inspection et Adaptation interconnectees",
        "Empirisme (Larousse) : la connaissance des choses derive de l'experience",
    ], "image": "empirisme.png"},

    # Diapo 7 - Les 3 piliers
    {"type": "content", "title": "II. La theorie - Les 3 piliers operationnels", "bullets": [
        "Transparence : les aspects importants du processus sont visibles des responsables des retombees",
        "Inspection : surveiller en permanence l'avancement vers l'objectif de l'iteration",
        ("Sans que la frequence des inspections gene le travail en cours", 1),
        "Adaptation : si un aspect derive hors des limites acceptables, ajuster des que possible",
        ("Objectif : minimiser le risque de derives supplementaires", 1),
    ]},

    # ===================== III. LES ROLES =====================
    {"type": "section", "title": "III. Les roles Scrum",
     "subtitle": "Product Owner - Scrum Master - Equipe de developpement"},

    # Diapo 8 - Vue d'ensemble
    {"type": "content", "title": "III. Les roles - Vue d'ensemble", "bullets": [
        "L'Equipe Scrum (Scrum Team) est constituee de trois entites indissociables :",
        ("Product Owner (PO)", 1),
        ("Development Team (Equipe de developpement)", 1),
        ("Scrum Master (SM)", 1),
        "Aucun sous-groupe, une seule equipe orientee vers un meme objectif",
    ]},

    # Diapo 9 - Product Owner
    {"type": "content", "title": "III.1 Le Product Owner (PO)", "bullets": [
        "Responsabilite : maximiser la valeur du produit et du travail de l'Equipe de Developpement",
        "Positionnement : represente le client et defend le produit",
        "Ecosysteme relationnel : interface constante entre :",
        ("l'Utilisateur, le Client, le Consultant et les autres parties prenantes", 1),
    ]},

    # Diapo 10 - PO taches cles
    {"type": "content", "title": "III.1 Le Product Owner - Taches cles", "bullets": [
        "Definir les besoins du produit et rediger les specifications",
        "Ordonner les besoins pour mieux realiser les missions",
        "Optimiser la valeur du travail effectue par l'Equipe de Developpement",
        "S'assurer que le besoin est visible, transparent et clair pour tous",
        ("Montrer ce sur quoi l'equipe travaillera prochainement", 1),
    ]},

    # Diapo 11 - Scrum Master
    {"type": "content", "title": "III.2 Le Scrum Master (SM)", "bullets": [
        "Definition : la personne chargee de lever tout obstacle freinant le travail de l'equipe",
        ("C'est un facilitateur, au service de l'equipe", 1),
        "Image : le chef d'orchestre, ou le gardien qui protege l'equipe des perturbations externes",
    ]},

    # Diapo 12 - SM taches cles
    {"type": "content", "title": "III.2 Le Scrum Master - Taches cles", "bullets": [
        "S'assurer de la bonne application de la methode",
        "Degager la voie devant l'Equipe de Developpement",
        "Optimiser la valeur du travail effectue par l'Equipe de Developpement",
    ]},

    # Diapo 13 - Equipe de developpement
    {"type": "content", "title": "III.3 L'Equipe de Developpement", "bullets": [
        "Definition : les personnes chargees de la realisation du sprint",
        ("et d'un produit utilisable en fin de sprint", 1),
        "Composition : developpeurs, architectes, testeurs fonctionnels, etc.",
        "Auto-organisee et pluridisciplinaire",
    ]},

    # ===================== IV. FONCTIONNEMENT =====================
    {"type": "section", "title": "IV. Le fonctionnement de Scrum",
     "subtitle": "Sprints, releases, regles et automatisation"},

    # Diapo 14 - Le concept de Sprint
    {"type": "content", "title": "IV. Fonctionnement - Le concept de Sprint", "bullets": [
        "Scrum decoupe le projet en iterations appelees sprints",
        "Cadence : un sprint dure entre 1 semaine et 1 mois",
        "Melee quotidienne (stand-up) : chaque jour les collaborateurs font le point sur :",
        ("Ce qui a ete fait  |  ce qui reste a faire  |  les difficultes rencontrees", 1),
        "Les fonctionnalites (user stories) sont triees dans le Product Backlog puis le Sprint Backlog",
    ]},

    # Diapo 15 - Cartographie du flux (IMAGE scrum_process)
    {"type": "content", "title": "IV. Fonctionnement - Cartographie du flux", "bullets": [
        "Entrees : executives, equipe, parties prenantes, clients, utilisateurs",
        "Le PO priorise la liste des besoins -> Product Backlog",
        "Sprint Planning : l'equipe selectionne le haut de la liste -> Sprint Backlog (Task Breakout)",
        "Sprint (1-4 sem) encadre par le SM : Burndown chart + Daily Scrum (toutes les 24 h)",
        "La date de fin et le livrable ne changent pas",
        "Sprint Review -> produit fini (Finished Work) -> Sprint Retrospective",
    ], "image": "scrum_process.png"},

    # Diapo 16 - Regles du Sprint et Release
    {"type": "content", "title": "IV. Fonctionnement - Sprint & livrable (Release)", "bullets": [
        "Chaque sprint cree une version potentiellement livrable du produit (release)",
        "Duree fixe ; chaque fin de sprint enchaine sur un nouveau",
        "Le contenu ne doit pas changer durant l'iteration",
        ("Les fonctionnalites reportees retournent dans le Product Backlog", 1),
        "Un release est heterogene : modules, configuration, doc, manuel, tests, user stories...",
    ]},

    # Diapo 17 - Cycle iteratif des versions (IMAGE release_cycle)
    {"type": "content", "title": "IV. Fonctionnement - Le cycle iteratif des versions", "bullets": [
        "Enchainement continu des increments produit :",
        ("Release 0  ->  Release 1  ->  ...  ->  Release N", 1),
        "Chaque release ajoute de la valeur livrable a la precedente",
    ], "image": "release_cycle.png"},

    # Diapo 18 - Release 0
    {"type": "content", "title": "IV. Fonctionnement - Le cas du Release 0", "bullets": [
        "Configurer l'environnement de developpement",
        "Choisir le socle technique",
        "Implementer les taches a automatiser",
        "Initialiser le developpement",
        "Mettre en place une infrastructure initiale",
    ]},

    # Diapo 19 - Pendant le Sprint
    {"type": "content", "title": "IV. Fonctionnement - Pendant le Sprint", "bullets": [
        "L'objectif du sprint est fixe : les changements qui le remettent en cause sont interdits",
        "Les objectifs de qualite sont maintenus : jamais revus a la baisse",
        "Le perimetre peut etre clarifie et renegocie entre le PO et l'equipe",
        ("au fur et a mesure de ce que l'equipe apprend", 1),
    ]},

    # Diapo 20 - Duree des sprints
    {"type": "content", "title": "IV. Fonctionnement - Duree des sprints", "bullets": [
        "Regle generale : duree fixe pour toutes les iterations",
        "Donnee cle pour la planification",
        "Best practice : l'equipe reste fidele aux delais (vacances, absences...)",
        "Gestion de crise : ne jamais etendre la duree ; en cas extreme, reduire le perimetre rendu",
    ]},

    # Diapo 21 - Short vs Long Sprint
    {"type": "content", "title": "IV. Fonctionnement - Short Sprint vs Long Sprint", "bullets": [
        "Short Sprint (court) :",
        ("Retour rapide des clients", 1),
        ("Risque de death sprints -> mauvaise qualite logicielle", 1),
        "Long Sprint (long) :",
        ("Difficile a planifier ; risque de changement de besoins chez le PO", 1),
        ("Tendance a deriver vers un modele classique en cascade", 1),
    ]},

    # Diapo 22 - Automatisation (IMAGE pipeline)
    {"type": "content", "title": "IV. Fonctionnement - Automatisation dans les sprints", "bullets": [
        "Automatiser les taches repetitives et consommatrices de ressources est essentiel",
        "Chaine d'automatisation continue (pipeline) :",
        ("Integration  ->  Build  ->  Packaging  ->  Deployment", 1),
    ], "image": "pipeline.png"},

    # ===================== V. EVENEMENTS =====================
    {"type": "section", "title": "V. Les evenements Scrum",
     "subtitle": "Sprint Planning - Daily Scrum - Sprint Review - Retrospective"},

    # Diapo 23 - Les 4 ceremonies
    {"type": "content", "title": "V. Les evenements - Les 4 ceremonies", "bullets": [
        "Les etapes cles du rythme Scrum :",
        ("Sprint Planning", 1),
        ("Daily Scrum", 1),
        ("Sprint Review", 1),
        ("Sprint Retrospective", 1),
    ]},

    # Diapo 24 - Sprint Planning
    {"type": "content", "title": "V. Les evenements - Le Sprint Planning", "bullets": [
        "Reunion determinante pour la reussite du sprint",
        "Inputs : les items prioritaires du Product Backlog",
        "Identifie les items a inclure dans le sprint",
        "Permet de definir l'objectif global du sprint (Sprint Goal)",
    ]},

    # Diapo 25 - Structure type
    {"type": "content", "title": "V. Les evenements - Structure d'un Sprint Planning", "bullets": [
        "Introduction et rappel des principes : 5 mn",
        "Definition du but du sprint : 10 mn",
        "Description des stories candidates : 30 mn",
        "Estimation des stories et decoupage si necessaire : 60 mn",
        "Decoupage technique en taches unitaires : 30 mn",
        "Definition des criteres d'acceptation precis : 40 mn",
        "Conclusion de la seance : 5 mn",
    ]},

    # Diapo 26 - Daily Scrum
    {"type": "content", "title": "V. Les evenements - Le Daily Scrum", "bullets": [
        "Aussi appele : daily stand-up, stand-up meeting, daily meeting",
        "Format : 15 minutes maximum pour synchroniser l'equipe et planifier les 24 h",
        "Contenu : ce qui a ete fait, ce qui reste a faire, les obstacles rencontres",
        "Gouvernance : le SM s'assure qu'il a lieu ; l'equipe en est responsable",
    ]},

    # Diapo 27 - Apports du Daily Scrum
    {"type": "content", "title": "V. Les evenements - Les apports du Daily Scrum", "bullets": [
        "Ameliore la communication et elimine les reunions superflues",
        "Revele les obstacles pour les supprimer rapidement",
        "Encourage la prise de decision rapide",
        "Ameliore le niveau de connaissance globale de l'equipe",
        "Point cle d'inspection et d'adaptation",
    ]},

    # Diapo 28 - Sprint Review
    {"type": "content", "title": "V. Les evenements - Le Sprint Review", "bullets": [
        "Reunion tenue a la fin de chaque sprint",
        "Objectif : inspecter le sprint ecoule et adapter le Product Backlog",
        "Duree : au maximum 4 heures pour un sprint d'1 mois",
        "Participants : toute l'equipe Scrum + les parties prenantes (stakeholders)",
    ]},

    # Diapo 29 - Deroulement du Sprint Review
    {"type": "content", "title": "V. Les evenements - Deroulement du Sprint Review", "bullets": [
        "Revue des pratiques du sprint et propositions d'amelioration",
        "L'equipe discute de ce qui a bien marche, des problemes et de leur resolution",
        "Le groupe convient de la suite -> contribue aux planifications suivantes",
        "Revue des delais, du budget, des fonctionnalites et du marche pour la prochaine livraison",
    ]},

    # Diapo 30 - Sprint Retrospective
    {"type": "content", "title": "V. Les evenements - Le Sprint Retrospective", "bullets": [
        "Occasion pour l'equipe de s'inspecter et de creer un plan d'amelioration",
        ("applique des le sprint suivant", 1),
        "Trois objectifs majeurs :",
        ("Inspecter le dernier sprint : personnes, relations, processus, outils", 1),
        ("Identifier et ordonner ce qui a bien marche et les ameliorations possibles", 1),
        ("Creer un plan pour ameliorer concretement le travail de l'equipe", 1),
    ]},

    # ===================== VI. ARTEFACTS =====================
    {"type": "section", "title": "VI. Les artefacts Scrum",
     "subtitle": "Product Backlog - Sprint Backlog - Burn-down chart"},

    # Diapo 31 - Documents de suivi
    {"type": "content", "title": "VI. Les artefacts - Les documents de suivi", "bullets": [
        "Les trois artefacts indispensables de Scrum :",
        ("Product Backlog", 1),
        ("Sprint Backlog (parfois appele release backlog)", 1),
        ("Burn-down chart", 1),
    ]},

    # Diapo 32 - Product Backlog
    {"type": "content", "title": "VI. Les artefacts - Le Product Backlog", "bullets": [
        "Une liste unique, triee par ordre de priorite absolue, de taches et de besoins",
        "Les besoins sont exprimes sous forme de user stories",
        "Bugs, ameliorations et changements techniques y sont traites de maniere unifiee",
        ("pas uniquement les besoins fonctionnels", 1),
    ]},

    # Diapo 33 - Affinage du Backlog
    {"type": "content", "title": "VI. Les artefacts - Affinage du Backlog", "bullets": [
        "Transition temporelle du besoin vers le livrable :",
        ("Product Backlog (vision macro)", 1),
        ("-> selection pour 30 jours maximum", 1),
        ("-> affinement dans le Release / Sprint Backlog", 1),
        ("-> decoupage a la journee (24 h)", 1),
        ("-> version exploitable (working increment)", 1),
    ]},

    # Diapo 34 - Sprint Backlog
    {"type": "content", "title": "VI. Les artefacts - Le Sprint Backlog", "bullets": [
        "Chaque sprint cree une version potentiellement livrable du produit",
        "Duree fixe ; chaque fin de sprint enchaine sur un nouveau",
        "Rassemble les elements selectionnes du Product Backlog",
        ("associes au plan technique detaille de realisation etabli par l'equipe", 1),
    ]},

    # Diapo 35 - Burn-down chart (IMAGE burndown)
    {"type": "content", "title": "VI. Les artefacts - Le Burn-down chart", "bullets": [
        "Exemple : Project XYZ - Iteration 1 Burn Down",
        "Axe Y : Sum of Task Estimates (days) - de 0 a 30 jours",
        "Axe X : Iteration Timeline (days) - de 0 a 20 jours",
        "Ligne bleue : Ideal Tasks Remaining (decroissance ideale)",
        "Ligne rouge : Actual Tasks Remaining (reste a faire reel)",
    ], "image": "burndown.png"},

    # Diapo 36 - Utilite du Burn-down
    {"type": "content", "title": "VI. Les artefacts - Utilite du Burn-down chart", "bullets": [
        "Mesurer precisement l'avancement du projet",
        ("Quantite de travail deja realise", 1),
        ("Quantite de travail restant a faire", 1),
        "Regle d'efficacite : privilegier de petites taches",
        ("pour que l'avancement de l'equipe soit fidelement mesurable", 1),
    ]},

    # ===================== CONCLUSION =====================
    {"type": "content", "title": "VII. Conclusion generale", "bullets": [
        "Scrum : approche moderne centree sur la livraison optimale et iterative de logiciels",
        "Roles stricts, evenements cadences, etat d'esprit collaboratif",
        "Ne fige pas les outils ni les techniques d'ingenierie : dicte une maniere agile de faire",
        "Favorise l'automatisation systematique des taches repetitives (productivite & stabilite)",
    ]},

    # Diapo 38 - References
    {"type": "content", "title": "References bibliographiques", "bullets": [
        "The Scrum Guide - Ken Schwaber & Jeff Sutherland (Scrum.org)",
        "Scrum Alliance - scrumalliance.org",
        "International Scrum Institute - scrum-institute.org",
        "K. Schwaber, M. Beedle - Agile Software Development with Scrum",
    ]},
]
