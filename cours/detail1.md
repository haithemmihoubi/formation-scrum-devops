# MODULE 1 — Gestion de projet Agile

## Chapitre 1 — Pourquoi l'Agilité ? Le problème historique

### 1.1 Le contexte : comment on faisait avant

Pour comprendre **pourquoi** l'Agilité existe, il faut comprendre ce qui se passait avant elle. Jusqu'aux années 2000, la quasi-totalité des projets informatiques étaient gérés selon un modèle appelé **cycle en cascade** (en anglais *waterfall*), ou sa variante le **cycle en V**.

L'idée du cycle en cascade est intuitive et rassurante : on traite le projet comme la construction d'un pont. On enchaîne des phases, l'une après l'autre, et on ne passe à la phase suivante que lorsque la précédente est complètement terminée et validée :

1. D'abord, on **recueille tous les besoins** et on rédige un cahier des charges exhaustif.
2. Ensuite, on **conçoit** l'architecture complète du système.
3. Puis on **développe** la totalité du logiciel.
4. Ensuite seulement on **teste** l'ensemble.
5. Enfin, on **livre** au client.

Sur le papier, c'est logique. Le problème, c'est que **le logiciel n'est pas un pont**. Un pont, une fois les besoins exprimés (« relier ces deux rives, supporter tel tonnage »), ne change pas pendant la construction. Un logiciel, lui, évolue constamment : le marché bouge, les concurrents sortent de nouvelles fonctions, les utilisateurs découvrent en s'en servant ce dont ils ont **réellement** besoin — et qui est souvent différent de ce qu'ils avaient demandé au début.

### 1.2 Les symptômes du problème

Quand un projet dure 12 ou 18 mois et qu'on ne montre le résultat au client qu'à la toute fin, plusieurs catastrophes se produisent de façon récurrente. Les études du secteur (notamment les rapports *CHAOS* du Standish Group) les ont documentées depuis les années 1990 :

- **L'effet tunnel.** Pendant des mois, le client ne voit rien de concret. Il signe un cahier des charges, puis attend. Quand il découvre enfin le produit, il est souvent trop tard pour corriger le tir sans exploser le budget.
- **Des besoins périmés à la livraison.** Ce qui était pertinent il y a 18 mois ne l'est plus forcément. On livre donc, parfois parfaitement, un produit qui ne correspond **plus** au besoin réel.
- **Des fonctionnalités jamais utilisées.** Des analyses ont montré qu'une grande partie des fonctionnalités spécifiées en amont sont **rarement ou jamais utilisées**. On a donc investi énormément d'effort pour produire de la valeur… que personne ne consomme.
- **Le coût du changement explose avec le temps.** Plus on découvre tard qu'une décision était mauvaise, plus elle coûte cher à corriger, car tout ce qui a été construit par-dessus doit être défait.

<div class="callout warn"><span class="title">⚠️ Le cœur du problème</span>
Plus l'horizon de livraison est lointain, plus l'écart se creuse entre <b>ce qui a été spécifié</b> et <b>ce dont l'utilisateur a réellement besoin</b>. L'Agilité ne fait pas disparaître l'incertitude — elle la rend gérable en <b>raccourcissant le temps entre une idée et sa validation par un vrai utilisateur</b>.
</div>

### 1.3 La réponse : livrer par petits morceaux et apprendre vite

L'intuition fondatrice de l'Agilité est simple : **si on ne peut pas tout prévoir, alors arrêtons d'essayer de tout prévoir, et organisons-nous plutôt pour apprendre et nous corriger rapidement.**

Concrètement, au lieu de livrer une seule fois après 18 mois, on livre un **petit morceau utilisable** toutes les deux ou trois semaines. À chaque livraison, on montre le résultat à de vrais utilisateurs, on observe leur réaction, et on ajuste la suite. On transforme un grand pari risqué en une série de petits paris peu risqués et corrigeables.

### 1.4 D'où vient le mot « Agile »

En février 2001, dix-sept experts du développement logiciel se sont réunis dans une station de ski à Snowbird, dans l'Utah. Ils venaient de courants différents — *eXtreme Programming* (Kent Beck), *Scrum* (Ken Schwaber et Jeff Sutherland), *DSDM*, *Crystal* — mais partageaient un même constat : les méthodes lourdes et bureaucratiques étouffaient les projets. De cette réunion est né un texte court : le **Manifeste pour le développement Agile de logiciels**.

<div class="callout note"><span class="title">📘 À retenir absolument</span>
L'Agilité n'est <b>pas une méthode</b> avec des étapes à suivre. C'est un <b>état d'esprit</b> (un <i>mindset</i>) décrit par un manifeste. Ce mindset se décline ensuite en <b>cadres de travail</b> (Scrum, Kanban, XP, SAFe…) et en <b>pratiques concrètes</b> (intégration continue, tests automatisés, revues…). Quand quelqu'un dit « on fait de l'Agile », demandez-lui toujours : « avec quel cadre, et quelles pratiques ? »
</div>

### 1.5 Quelques repères dans le temps

| Année | Ce qui se passe |
|------|-----------------|
| 1986 | Takeuchi et Nonaka publient un article comparant le développement produit au rugby ; le terme *scrum* (la mêlée) y apparaît. |
| 1995 | Première présentation formelle de Scrum par Schwaber et Sutherland. |
| 1999 | Kent Beck publie *Extreme Programming Explained*. |
| **2001** | **Rédaction du Manifeste Agile.** |
| 2003 | David J. Anderson commence à appliquer Kanban (issu de l'industrie Toyota) au logiciel. |
| 2010+ | L'Agilité se généralise et se combine avec DevOps ; apparition des cadres de mise à l'échelle (SAFe, LeSS). |

---

## Chapitre 2 — Le Manifeste Agile expliqué en profondeur

Le Manifeste tient en quatre **valeurs** et douze **principes**. Beaucoup de gens les récitent sans les comprendre. Nous allons les expliquer un par un.

### 2.1 Les quatre valeurs, décortiquées

Chaque valeur s'écrit sous la forme « **A plutôt que B** ». Le point le plus important, et le plus souvent mal compris, est ceci : **B n'est pas mauvais. B a de la valeur. Mais quand il faut choisir, on privilégie A.** Le Manifeste le dit lui-même explicitement.

**Valeur 1 — Les individus et leurs interactions, plutôt que les processus et les outils.**
Un processus bien rodé et un outil sophistiqué ne sauveront jamais une équipe dont les membres ne se parlent pas et ne se font pas confiance. À l'inverse, une équipe soudée trouvera toujours une solution, même avec des outils modestes. *Cela ne veut pas dire « pas de processus ni d'outils » : cela veut dire que l'humain passe d'abord.*

**Valeur 2 — Un logiciel qui fonctionne, plutôt qu'une documentation exhaustive.**
La vraie mesure de l'avancement d'un projet, ce n'est pas le nombre de pages de spécifications produites, ni le pourcentage de phases « terminées » sur un planning. C'est **du logiciel qui marche et qu'on peut montrer**. Un document de 200 pages ne rend service à personne s'il ne se traduit pas en produit utilisable. *Cela ne veut pas dire « zéro documentation » : cela veut dire « juste assez de documentation, au bon moment, et un produit qui fonctionne avant tout ».*

**Valeur 3 — La collaboration avec le client, plutôt que la négociation contractuelle.**
Dans l'approche traditionnelle, le client et le fournisseur passent un temps fou à négocier un contrat détaillé, puis à se renvoyer la responsabilité quand quelque chose ne va pas (« ce n'était pas dans le contrat ! »). L'Agilité propose de traiter le client comme un **partenaire continu** : il participe régulièrement, voit le produit grandir, et oriente les priorités. Le contrat existe toujours, mais la relation prime sur le bras de fer.

**Valeur 4 — L'adaptation au changement, plutôt que le suivi d'un plan.**
On planifie toujours — c'est indispensable. Mais le plan est un **outil de décision**, pas une promesse gravée dans le marbre. Dès qu'on apprend quelque chose de nouveau (un retour utilisateur, un problème technique, une opportunité), on ajuste le plan. Dans le monde traditionnel, changer le plan est vu comme un échec ; en Agile, c'est vu comme une **intelligence**.

<div class="callout danger"><span class="title">❗ L'erreur la plus répandue sur l'Agilité</span>
« Être agile, ça veut dire qu'on ne planifie pas et qu'on ne documente pas. » <b>C'est faux, et c'est l'inverse de ce que dit le Manifeste.</b> Le texte précise que les éléments de droite (processus, documentation, contrat, plan) <b>ont de la valeur</b>. L'Agilité déplace simplement le curseur vers l'humain, le produit, la collaboration et l'adaptation — elle ne supprime rien.
</div>

### 2.2 Les douze principes, regroupés pour les comprendre

Réciter douze principes dans le désordre ne sert à rien. Regroupons-les en **quatre grandes idées**.

**Idée A — Livrer de la valeur tôt, souvent, et accueillir le changement.**

> 1. Notre priorité est de satisfaire le client en livrant tôt et régulièrement des fonctionnalités à grande valeur.
> 2. Accueillez positivement les changements de besoins, même tard dans le projet : c'est un avantage compétitif pour le client.
> 3. Livrez fréquemment un logiciel opérationnel, de quelques semaines à quelques mois, la période la plus courte étant préférable.

L'idée centrale : **la valeur se mesure quand elle est entre les mains de l'utilisateur**, pas quand elle est « codée mais pas livrée ». Et puisqu'on livre souvent, accepter un changement coûte peu.

**Idée B — La collaboration humaine est le moteur.**

> 4. Les responsables métier et les développeurs doivent travailler ensemble quotidiennement.
> 5. Réalisez les projets avec des personnes motivées ; donnez-leur l'environnement et le soutien dont elles ont besoin, et faites-leur confiance.
> 6. La méthode la plus efficace de transmettre de l'information est une conversation en face à face.

L'idée centrale : on ne pilote pas un projet à coups de documents qui s'échangent par e-mail. On le pilote par la **conversation directe et continue** entre ceux qui savent ce qu'il faut faire (le métier) et ceux qui savent le faire (les développeurs).

**Idée C — La mesure de la réussite, c'est le produit qui marche, à un rythme tenable.**

> 7. Un logiciel opérationnel est la principale mesure d'avancement.
> 8. Les processus agiles encouragent un rythme de développement soutenable : commanditaires, développeurs et utilisateurs devraient pouvoir maintenir indéfiniment un rythme constant.

L'idée centrale : on ne « brûle » pas les équipes par des sprints d'urgence permanents. Un bon rythme est un rythme qu'on peut tenir **pendant des années**, pas pendant trois semaines.

**Idée D — L'excellence technique et l'amélioration continue.**

> 9. Une attention continue à l'excellence technique et à une bonne conception renforce l'agilité.
> 10. La simplicité — c'est-à-dire l'art de maximiser la quantité de travail qu'on ne fait pas — est essentielle.
> 11. Les meilleures architectures, spécifications et conceptions émergent d'équipes auto-organisées.
> 12. À intervalles réguliers, l'équipe réfléchit aux moyens de devenir plus efficace, puis ajuste son comportement en conséquence.

L'idée centrale : pour pouvoir changer vite et souvent, le code doit rester **propre et simple** (sinon, chaque changement devient un cauchemar). Et l'équipe doit régulièrement **s'arrêter pour réfléchir à comment mieux travailler** — c'est l'origine de la rétrospective qu'on verra plus loin.

Le principe 10 mérite une explication particulière car il est contre-intuitif : « maximiser la quantité de travail qu'on **ne** fait **pas** ». Cela signifie : la meilleure fonctionnalité est souvent celle qu'on décide de **ne pas** développer parce qu'elle n'apporte pas assez de valeur. Chaque ligne de code écrite est une ligne à maintenir, tester et faire évoluer. Moins on en écrit pour un même résultat, mieux c'est.

---

## Chapitre 3 — Prédictif contre adaptatif

Maintenant que l'esprit est posé, comparons concrètement les deux grandes familles d'approches.

### 3.1 L'approche prédictive (cascade / cycle en V)

```
Besoins ─► Spécifications ─► Conception ─► Codage ─► Tests ─► Recette ─► Livraison
   (tout est figé au début ; la valeur n'arrive qu'à la toute fin)
```

Dans cette approche, on cherche à **tout prévoir au début** (d'où le nom « prédictif »). Elle a de vraies qualités, et il serait faux de la diaboliser :

- Elle donne un **cadre rassurant** avec des jalons contractuels nets.
- Elle convient parfaitement quand le besoin est **stable et parfaitement connu** : par exemple un logiciel embarqué dans un dispositif médical certifié, un calcul de paie soumis à une réglementation précise, ou un système qui doit respecter une norme figée.

Ses faiblesses, on les a vues au chapitre 1 : effet tunnel, feedback tardif, coût du changement très élevé en fin de parcours.

### 3.2 L'approche adaptative (itérative et incrémentale)

Ici, on construit le produit par **incréments** : à chaque itération (une période courte et fixe), on produit un morceau de produit **réellement utilisable**, on le montre, on recueille du feedback, et on ajuste le plan.

| Critère | Approche prédictive (V) | Approche adaptative (Agile) |
|---------|-------------------------|-----------------------------|
| Nature du besoin | Stable et connu d'avance | Évolutif, incertain |
| Moment où la valeur est livrée | À la toute fin | À chaque itération |
| Gestion du changement | Coûteuse, encadrée, mal vue | Attendue et intégrée |
| Comment on mesure l'avancement | En pourcentage de phases finies | En logiciel qui fonctionne |
| Quand les risques se révèlent | Tard (souvent trop tard) | Tôt (on peut réagir) |

### 3.3 Une distinction subtile mais essentielle : itératif ≠ incrémental

Ces deux mots sont souvent confondus. L'Agilité combine les deux.

- **Incrémental** veut dire : on ajoute des morceaux les uns après les autres. Image : on construit une maison pièce par pièce — d'abord la cuisine entièrement finie, puis le salon entièrement fini, etc.
- **Itératif** veut dire : on repasse plusieurs fois sur l'ensemble pour l'améliorer. Image : on peint d'abord une esquisse grossière du tableau entier, puis on raffine progressivement les détails.

<div class="callout note"><span class="title">📘 L'illustration du skateboard</span>
La célèbre illustration de Henrik Kniberg résume tout. Pour livrer une voiture, l'approche prédictive construit d'abord une roue (inutilisable), puis deux roues (inutilisable), puis un châssis (inutilisable), et enfin la voiture. L'approche agile livre d'abord un <b>skateboard</b> (le client peut déjà se déplacer !), puis une <b>trottinette</b>, puis un <b>vélo</b>, puis une <b>moto</b>, et enfin la <b>voiture</b>. À chaque étape, le client a quelque chose d'<b>utilisable</b> et peut donner son avis. C'est cela, combiner itératif et incrémental.
</div>

---

## Chapitre 4 — Les concepts clés

Quatre notions reviennent en permanence en Agile. Prenons le temps de bien les comprendre, car tout le reste s'appuie dessus.

### 4.1 Le MVP — Minimum Viable Product (produit minimum viable)

Le MVP est la **plus petite version livrable du produit qui permet déjà d'apprendre quelque chose d'utile auprès de vrais utilisateurs**. Le mot important est « viable » : ce n'est pas un produit bâclé ou cassé, c'est un produit **réduit mais cohérent et fonctionnel**.

Prenons notre fil rouge, l'application QuickBite (commande de repas) :

- ❌ **Mauvais MVP :** « on livre la moitié de l'écran de paiement, sans que ça fonctionne ». Ce n'est pas viable, on n'apprend rien.
- ✅ **Bon MVP :** « on permet de commander **un** plat dans **un** seul restaurant et de payer — du début à la fin ». C'est minimal (un seul restaurant, un seul plat), mais c'est **viable** : un utilisateur peut réellement passer une commande, et on apprend la chose la plus importante : *est-ce que les gens commandent vraiment ?*

L'objectif du MVP n'est pas de vendre, c'est d'**apprendre** au moindre coût avant d'investir massivement.

### 4.2 La valeur métier

La **valeur métier** est le bénéfice qu'apporte une fonctionnalité, soit à l'utilisateur, soit à l'entreprise. Cela peut être : générer du revenu, faire économiser du temps ou de l'argent, réduire un risque, ou augmenter la satisfaction des clients.

Le principe fondamental qui en découle : **on priorise par la valeur, pas par la facilité technique.** Il est tentant pour une équipe de faire d'abord ce qui est facile ou amusant à coder. L'Agilité impose au contraire de faire d'abord ce qui rapporte le plus au client, même si c'est plus difficile.

### 4.3 La boucle de feedback (feedback loop)

```
   Construire ───► Mesurer ───► Apprendre ──┐
       ▲                                     │
       └─────────────────────────────────────┘
```

C'est le cœur battant de l'Agilité. On construit quelque chose, on **mesure** comment les utilisateurs y réagissent, on en **tire des enseignements**, et ces enseignements alimentent la prochaine construction.

La règle d'or : **plus cette boucle est courte, mieux c'est.** Pourquoi ? Parce que plus on découvre tôt qu'on s'est trompé, moins la correction coûte cher. Découvrir une erreur après deux semaines coûte une correction de deux semaines ; la découvrir après dix-huit mois peut coûter le projet entier.

### 4.4 Definition of Ready (DoR) et Definition of Done (DoD)

Ce sont deux **listes de critères partagées** par toute l'équipe. Elles évitent les malentendus, qui sont la première cause de gaspillage dans un projet.

| | Definition of Ready (DoR) | Definition of Done (DoD) |
|--|---------------------------|--------------------------|
| **À quel moment ?** | Avant qu'un travail entre dans une itération | Pour déclarer un travail réellement terminé |
| **La question posée** | « Cette tâche est-elle prête à être développée ? » | « Ce travail est-il vraiment fini, sans réserve ? » |
| **Exemples de critères** | Le besoin est clair, estimé, ses critères d'acceptation sont écrits, ses dépendances sont connues | Le code est écrit, relu par un pair, testé, intégré, documenté, déployable et démontré |

<div class="callout warn"><span class="title">⚠️ Pourquoi la DoD est non négociable</span>
Le syndrome le plus destructeur en gestion de projet est le « c'est fini à 90 % » qui dure des semaines. Sans une <b>Definition of Done</b> claire et partagée, chacun a sa propre idée de « terminé », et le « presque fini » s'accumule jusqu'à ce que plus personne ne sache où en est réellement le projet. La DoD est une <b>checklist commune et non négociable</b> : un travail est « Done » seulement s'il coche <b>toutes</b> les cases.
</div>

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 1 : diagnostic et transition</span>
<b>Contexte :</b> « FidExpress » est une PME qui développe un logiciel de fidélité en cascade. Cycle de 12 mois, retards à répétition, clients mécontents, spécifications déjà périmées au moment de la livraison.<br><br>
<b>À vous :</b><br>
1. Listez les <b>symptômes</b> visibles, puis remontez aux <b>causes racines</b> (technique des « 5 pourquoi » : pour chaque problème, demandez « pourquoi ? » cinq fois de suite).<br>
2. Pour trois causes, proposez une <b>pratique agile</b> qui y répond directement.<br>
3. Dessinez une <b>trajectoire de transition</b> en 3 étapes sur 6 mois (commencez par une seule équipe pilote, puis généralisez).
</div>

**Éléments de correction de l'exercice :**

| Symptôme observé | Cause racine probable | Pratique agile qui y répond | Bénéfice attendu |
|------------------|----------------------|----------------------------|------------------|
| Specs périmées à la livraison | Cycle de livraison trop long | Itérations de 2-3 semaines avec démo | Feedback tôt, specs qui restent vivantes |
| Effet tunnel, client dans le flou | Aucun point d'étape produit | Revue de sprint régulière | Visibilité continue pour le client |
| Les mêmes erreurs se répètent | Aucun bilan organisé | Rétrospective d'équipe | Amélioration continue mesurable |
| Équipe surchargée, burn-out | Plan irréaliste, tout est urgent | Rythme soutenable + limite de travail en cours | Cadence tenable dans la durée |

---

## Chapitre 5 — Scrum, le cadre complet

Scrum est, de loin, le cadre agile le plus utilisé dans le monde. Ce n'est pas une méthode rigide : c'est un **cadre léger** qui définit quelques rôles, quelques réunions et quelques documents, et laisse l'équipe libre du reste.

### 5.1 Le fondement : l'empirisme

Scrum repose sur une idée philosophique appelée **empirisme** : *on ne peut pas tout savoir d'avance ; la connaissance vient de l'expérience et des décisions prises à partir de ce qu'on observe.* Cet empirisme s'appuie sur trois piliers :

- **La transparence.** Tout le monde (équipe, client, management) voit le **même état réel** du travail. Pas de chiffres maquillés, pas de « tout va bien » de façade. Sans transparence, les deux piliers suivants sont impossibles.
- **L'inspection.** On examine régulièrement et fréquemment l'avancement du produit **et** la façon de travailler, pour détecter les écarts.
- **L'adaptation.** Dès qu'on détecte un écart, on **ajuste** — le produit, le plan, ou la manière de travailler — sans attendre.

À ces trois piliers s'ajoutent **cinq valeurs** que l'équipe doit incarner : l'**engagement**, le **focus** (la concentration sur l'objectif), l'**ouverture**, le **respect** et le **courage** (notamment le courage de dire la vérité et de soulever les problèmes).

### 5.2 Vue d'ensemble du cadre

```
        ┌─────────────────── SPRINT (1 à 4 semaines, durée fixe) ──────────────────┐
        │                                                                           │
Product │  Sprint     ┌── Daily ──┐    Travail        Sprint      Sprint           │
Backlog ├─►Planning ──►│  Scrum    │──► quotidien ───► Review ────► Retrospective ──┼─► Increment
(le quoi)│  (le plan)  └───────────┘    (sur le         (montrer    (s'améliorer)    │   (utilisable,
        │              chaque jour       Sprint          au client)                  │    "Done")
        │              15 minutes        Backlog)                                    │
        └───────────────────────────────────────────────────────────────────────────┘
                          puis on enchaîne immédiatement le sprint suivant
```

Décrivons maintenant chaque élément en détail.

### 5.3 Les trois rôles (ou « responsabilités »)

Scrum définit **une seule équipe**, appelée *Scrum Team*, sans hiérarchie interne. Elle regroupe trois responsabilités distinctes.

#### Le Product Owner (PO) — il répond à « quoi » et « pourquoi »

Le Product Owner est la personne **responsable de maximiser la valeur** du produit. C'est lui — et lui seul — qui décide de ce qu'on fait et dans quel ordre.

Ses responsabilités concrètes :

- **Porter la vision du produit** : où va-t-on, et pourquoi ?
- **Constituer, ordonner et clarifier le Product Backlog** (la liste de tout ce qu'on pourrait faire — voir plus loin).
- **Prioriser** : décider quoi faire en premier, en fonction de la valeur, du risque, du coût et des dépendances.
- **Être disponible** pour l'équipe : répondre aux questions, clarifier les besoins, valider ou refuser le résultat.

Le PO utilise des outils comme le **story mapping** (cartographier le parcours utilisateur pour organiser le backlog) et des techniques de priorisation comme **MoSCoW** ou **valeur/effort** (qu'on verra au chapitre 6).

<div class="callout tip"><span class="title">💡 Le PO décrit le besoin, pas la solution</span>
Un bon Product Owner exprime un <b>besoin</b> et un <b>pourquoi</b>, puis laisse l'équipe trouver le <b>comment</b>. Il dit : « j'ai besoin que le client puisse payer en un minimum d'étapes, car on perd des ventes au moment du paiement ». Il ne dit <b>pas</b> : « ajoutez un bouton bleu de 40 pixels en bas à droite ». Le « comment » technique appartient à l'équipe.
</div>

#### Le Scrum Master (SM) — il répond à « comment bien travailler ensemble »

Le Scrum Master est un **leader serviteur** (*servant leader*). Cette expression est importante : il ne **commande** pas l'équipe, il la **sert**. Son but est de rendre l'équipe la plus efficace possible.

Ses responsabilités concrètes :

- **Faciliter** les réunions Scrum et fluidifier la collaboration.
- **Lever les obstacles** (en anglais *impediments*) : tout ce qui ralentit l'équipe (un accès qu'on n'obtient pas, un autre service qui ne répond pas, un outil qui manque). Le SM passe une grande partie de son temps à débloquer ces situations.
- **Coacher** l'équipe vers l'auto-organisation et l'amélioration continue.
- **Protéger** l'équipe des interruptions extérieures et du sur-engagement (par exemple, dire non à un manager qui veut ajouter du travail en plein milieu d'un sprint).

<div class="callout warn"><span class="title">⚠️ Un Scrum Master n'est PAS un chef de projet</span>
C'est la confusion la plus fréquente. Le Scrum Master ne distribue pas les tâches, ne fixe pas les délais à la place de l'équipe, et n'évalue pas individuellement les personnes. Son seul pouvoir est l'<b>influence</b> et le <b>coaching</b>, pas l'<b>autorité hiérarchique</b>. S'il se met à donner des ordres, ce n'est plus du Scrum.
</div>

#### Les Développeurs — ils répondent à « comment réaliser »

Les *Developers* regroupent toutes les personnes qui contribuent à construire l'incrément : développeurs au sens strict, mais aussi testeurs, designers, experts ops, etc. Deux qualités les définissent :

- Ils sont **auto-organisés** : c'est l'équipe elle-même qui décide comment se répartir et réaliser le travail, pas un chef extérieur.
- Ils sont **pluridisciplinaires** (*cross-functional*) : l'équipe possède collectivement toutes les compétences nécessaires pour livrer, sans dépendre en permanence de l'extérieur.

| | Product Owner | Scrum Master | Développeurs |
|--|---------------|--------------|--------------|
| Se concentre sur… | La **valeur** | Le bon **fonctionnement** de l'équipe | La **réalisation** |
| Est responsable de… | Le Product Backlog | Le processus Scrum | Le Sprint Backlog |
| Sa question type | « Quoi faire, et dans quel ordre ? » | « Qu'est-ce qui nous bloque ? » | « Comment le faire, et combien ça coûte ? » |

### 5.4 Les trois artefacts

Un **artefact**, en Scrum, est un élément concret qui rend le travail visible. Il y en a trois, et à chacun est associé un « engagement » qui lui donne une direction.

| Artefact | Ce que c'est | Engagement associé |
|----------|--------------|--------------------|
| **Product Backlog** | La liste **ordonnée et vivante** de tout ce qui pourrait être utile au produit. C'est la source unique du travail à faire. | **Product Goal** : l'objectif produit à moyen terme |
| **Sprint Backlog** | La sélection d'éléments choisis pour le sprint en cours, plus le plan pour les réaliser. | **Sprint Goal** : l'objectif unique du sprint |
| **Increment** | La somme de tout le travail « Done » à la fin du sprint. Il doit être **utilisable**. | **Definition of Done** : la définition de « terminé » |

<div class="callout note"><span class="title">📘 « Ordonné » et non « priorisé »</span>
On dit que le Product Backlog est <b>ordonné</b> plutôt que <b>priorisé</b>. La nuance : « priorisé » pourrait laisser croire qu'il suffit de classer par importance. « Ordonné » est plus fort : il existe un <b>ordre précis, du premier au dernier élément</b>, qui tient compte de la valeur mais aussi du risque, des dépendances et du coût. Il n'y a jamais deux éléments « ex æquo » : l'équipe sait toujours quoi prendre ensuite.
</div>

### 5.5 Les événements (les cérémonies)

Scrum définit cinq événements. Le premier, le **Sprint**, contient tous les autres.

**Le Sprint** est le conteneur : une période de durée **fixe**, de une à quatre semaines (deux semaines est le choix le plus courant). On n'allonge jamais un sprint, même si le travail n'est pas fini. Dès qu'un sprint se termine, le suivant commence immédiatement. Cette régularité crée un **rythme** (une « cadence ») rassurant et prévisible.

| Événement | Durée maximale (sprint de 2 semaines) | Qui participe | Objectif |
|-----------|----------------------------------------|---------------|----------|
| **Sprint Planning** | 4 heures | Toute l'équipe Scrum | Définir l'objectif du sprint et le plan |
| **Daily Scrum** | 15 minutes par jour | Les Développeurs | Se synchroniser et ajuster le plan du jour |
| **Sprint Review** | 2 heures | L'équipe + les parties prenantes | Inspecter le produit et recueillir le feedback |
| **Sprint Retrospective** | 1 h 30 | Toute l'équipe Scrum | Améliorer la façon de travailler |

#### Le Sprint Planning — la réunion qui lance le sprint

Au début de chaque sprint, l'équipe se réunit pour planifier. Cette réunion répond à trois questions, dans l'ordre :

1. **Pourquoi ce sprint a-t-il de la valeur ?** On formule un **Sprint Goal** (objectif de sprint) : une phrase qui donne du sens à l'ensemble. Exemple pour QuickBite : « permettre à un client de commander un plat et de payer, de bout en bout ».
2. **Que peut-on livrer dans ce sprint ?** L'équipe sélectionne, en haut du Product Backlog, les éléments qu'elle pense pouvoir terminer.
3. **Comment va-t-on les réaliser ?** Les développeurs découpent ces éléments en tâches concrètes : c'est le **plan**.

#### Le Daily Scrum — la synchronisation quotidienne

Chaque jour, à heure fixe et pour **15 minutes maximum**, les développeurs se synchronisent. Un format classique consiste à ce que chacun réponde brièvement à trois questions : *qu'ai-je terminé hier qui aide l'objectif du sprint ? que vais-je faire aujourd'hui ? qu'est-ce qui me bloque ?*

<div class="callout warn"><span class="title">⚠️ Le Daily n'est pas un reporting au chef</span>
Le Daily Scrum est une réunion <b>entre développeurs, pour les développeurs</b>. Ce n'est pas un compte-rendu fait au Scrum Master ou au manager. Si un sujet demande une discussion approfondie, on le note et on le traite <b>juste après</b>, entre les seules personnes concernées (on appelle cela « l'after-party »). C'est ce qui permet de tenir les 15 minutes.
</div>

#### La Sprint Review — montrer le produit

À la fin du sprint, l'équipe présente l'incrément réalisé **aux parties prenantes** (le client, les utilisateurs, le management). On fait une **démonstration réelle** du produit qui fonctionne (pas des diapositives !), et on recueille du feedback qui alimentera le Product Backlog. La Review inspecte **le produit**.

#### La Sprint Retrospective — améliorer la façon de travailler

Juste après la Review, l'équipe se réunit entre elle pour réfléchir non pas au produit, mais à **sa façon de travailler** : qu'est-ce qui a bien marché ? qu'est-ce qui nous a ralentis ? que va-t-on changer concrètement au prochain sprint ? La Rétrospective inspecte **le processus**.

<div class="callout tip"><span class="title">💡 Review et Rétrospective : ne pas confondre</span>
Moyen mnémotechnique : la <b>Review</b> regarde le <b>pROduit</b> (et inclut le client) ; la <b>Rétro</b> regarde l'équi<b>PE</b> et sa façon de travailler (entre membres de l'équipe uniquement). Quelques formats de rétrospective utiles : <b>Start / Stop / Continue</b> (qu'est-ce qu'on commence, arrête, continue ?), <b>Mad / Sad / Glad</b> (ce qui m'a énervé, attristé, réjoui), et les <b>4 L</b> (Liked, Learned, Lacked, Longed for).
</div>

---

## Chapitre 6 — Écrire et estimer le travail

On sait maintenant qui fait quoi et quand. Reste une question pratique : **comment décrit-on concrètement le travail à faire ?**

### 6.1 La hiérarchie : Epic → User Story → Task

```
Epic         (un gros besoin, trop gros pour un seul sprint)
  └── User Story   (un besoin utilisateur livrable en un sprint)
        └── Task   (un travail technique de quelques heures)
```

- Une **Epic** est un gros morceau de fonctionnalité qu'on ne peut pas réaliser en un seul sprint (exemple : « tout le système de paiement »). On la découpe en plusieurs User Stories.
- Une **User Story** (« récit utilisateur ») décrit un besoin **du point de vue de l'utilisateur**, suffisamment petit pour tenir dans un sprint.
- Une **Task** est une décomposition technique d'une story (exemple : « créer la table en base », « appeler l'API de paiement »). Elle se compte en heures.

### 6.2 Comment écrire une bonne User Story

La forme canonique d'une story est une phrase qui force à penser à l'utilisateur et au bénéfice :

> **En tant que** [rôle], **je veux** [action], **afin de** [bénéfice].

Exemple pour QuickBite :

> En tant que **client**, je veux **payer ma commande par carte bancaire**, afin de **finaliser mon achat sans quitter l'application**.

Cette formulation est précieuse car elle répond toujours à « pour qui ? » et surtout à « pourquoi ? ». Le « afin de » est la partie la plus importante : si on n'arrive pas à le remplir, c'est peut-être que la fonctionnalité n'a pas de valeur réelle.

### 6.3 Les critères INVEST : la check-list d'une bonne story

Pour vérifier qu'une story est bien écrite, on utilise l'acronyme **INVEST** :

| Lettre | Signifie | La question à se poser |
|--------|----------|------------------------|
| **I** | *Independent* (indépendante) | Peut-on la réaliser seule, sans dépendre d'une autre ? |
| **N** | *Negotiable* (négociable) | Le « comment » reste-t-il ouvert à la discussion ? |
| **V** | *Valuable* (à valeur) | Apporte-t-elle un bénéfice clair à quelqu'un ? |
| **E** | *Estimable* (estimable) | A-t-on assez d'infos pour estimer son effort ? |
| **S** | *Small* (petite) | Tient-elle dans un seul sprint ? |
| **T** | *Testable* (testable) | Peut-on vérifier objectivement qu'elle est réussie ? |

### 6.4 Les critères d'acceptation

Une story doit s'accompagner de **critères d'acceptation** : les conditions précises qui permettent de dire « c'est réussi ». Un format très répandu est le format **Gherkin** (Étant donné… Quand… Alors) :

```gherkin
Étant donné que je suis un client avec un panier non vide
Quand je saisis une carte bancaire valide et que je confirme
Alors le paiement est accepté
Et je reçois un récapitulatif de ma commande
```

Ces critères servent à trois choses : ils clarifient le besoin (le « T » d'INVEST), ils guident le développement, et ils servent de base aux tests.

### 6.5 Estimer : pourquoi en « points » et pas en heures

Voici un point qui surprend souvent les débutants : en Agile, on n'estime généralement **pas en heures**, mais en **points de story** (*story points*), en utilisant une suite de nombres inspirée de Fibonacci : 1, 2, 3, 5, 8, 13, 20…

Pourquoi pas en heures ? Parce que les estimations en heures donnent une **fausse impression de précision** et se révèlent presque toujours fausses (« je pensais 4 heures, ça en a pris 11 »). Les humains sont mauvais pour estimer des durées absolues, mais **bons pour comparer** : on sait facilement dire qu'une tâche est « à peu près deux fois plus grosse » qu'une autre.

Les points capturent donc la **taille relative** (complexité + effort + incertitude) d'une story par rapport aux autres. On choisit une petite story de référence (« celle-ci vaut 2 »), et on estime tout le reste par comparaison.

<div class="callout note"><span class="title">📘 La vélocité : prévoir sans promettre des heures</span>
Une fois qu'on estime en points, on observe combien de points l'équipe termine réellement à chaque sprint : c'est la <b>vélocité</b>. Si une équipe livre en moyenne 20 points par sprint, et qu'il reste 100 points dans le backlog, on peut estimer qu'il faudra environ 5 sprints. C'est une prévision <b>basée sur des faits observés</b>, bien plus fiable qu'une addition d'heures devinées.
</div>

#### Le Planning Poker : comment on estime en équipe

Pour estimer collectivement et éviter qu'une personne influence les autres, on utilise le **Planning Poker** :

1. Le Product Owner présente une story.
2. Chaque membre de l'équipe choisit **en secret** une carte (un nombre de la suite).
3. Tout le monde **révèle sa carte en même temps**.
4. Si les estimations divergent fortement, les deux extrêmes **expliquent leur raisonnement** (souvent, l'un a vu une difficulté que l'autre ignorait). Puis on rejoue, jusqu'au consensus.

L'intérêt n'est pas tant le chiffre final que **la conversation** qu'il provoque : elle révèle les incompréhensions et les risques cachés.

### 6.6 Prioriser avec MoSCoW

Pour ordonner le backlog, une technique simple est **MoSCoW**, qui classe chaque élément en quatre catégories :

- **Must** (doit) — indispensable ; sans cela, le produit n'a pas de sens. C'est le cœur du MVP.
- **Should** (devrait) — important, mais on peut s'en passer temporairement.
- **Could** (pourrait) — souhaitable si on a le temps.
- **Won't** (pas maintenant) — explicitement hors périmètre pour l'instant.

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 2 : construire un backlog et planifier un sprint</span>
<b>Produit : QuickBite.</b> Vision : « permettre à un client de commander un repas dans un restaurant proche et de payer en quelques clics ».<br><br>
<b>À vous :</b><br>
1. <b>Brainstormez</b> au moins 12 idées d'éléments de backlog.<br>
2. Écrivez <b>6 User Stories</b> au format canonique, avec des critères d'acceptation Gherkin pour deux d'entre elles.<br>
3. <b>Estimez</b>-les en Planning Poker (suite de Fibonacci).<br>
4. <b>Priorisez</b> avec MoSCoW et formulez le <b>Product Goal</b>.<br>
5. La capacité de l'équipe est de <b>20 points</b> : choisissez les stories du Sprint 1 et formulez un <b>Sprint Goal</b>.
</div>

**Exemple de correction (extrait du backlog estimé et priorisé) :**

| # | User Story | Estimation | MoSCoW |
|---|------------|-----------|--------|
| 1 | Voir la liste des restaurants proches | 5 | Must |
| 2 | Consulter le menu d'un restaurant | 3 | Must |
| 3 | Ajouter un plat au panier | 3 | Must |
| 4 | Payer ma commande par carte | 8 | Must |
| 5 | Suivre l'état de ma commande | 5 | Should |
| 6 | Noter le restaurant après livraison | 2 | Could |

**Sprint Goal proposé :** « Un client peut commander un plat dans un restaurant et le payer — parcours complet de bout en bout. » On sélectionne alors les stories 1, 2, 3 et 4, soit 19 points : cela tient dans la capacité de 20 points, et l'ensemble forme un objectif **cohérent** (et pas une simple addition de tâches sans lien).

---

## Chapitre 7 — Kanban et le pilotage par le flux

Scrum n'est pas le seul cadre agile. **Kanban** en est un autre, très différent dans sa philosophie, et tout aussi important à connaître.

### 7.1 D'où vient Kanban

Le mot *kanban* signifie « panneau » ou « carte visuelle » en japonais. La méthode vient du **système de production de Toyota** (le fameux « juste-à-temps »), où des cartes physiques circulaient pour signaler qu'il fallait réapprovisionner un poste. David J. Anderson a adapté ces idées au développement logiciel à partir de 2010.

La grande différence avec Scrum : **Kanban n'impose ni rôles, ni itérations, ni réunions obligatoires**. C'est une **méthode d'amélioration évolutive** : on part de la façon dont on travaille **déjà aujourd'hui**, et on l'améliore progressivement, sans révolution.

### 7.2 Les principes de conduite du changement

Kanban repose sur quatre principes pour démarrer en douceur :

1. **Commencer par ce que vous faites maintenant** — on ne jette rien, on observe l'existant.
2. **S'accorder pour progresser par des changements évolutifs et incrémentaux** — pas de grand chambardement.
3. **Respecter le processus, les rôles et les responsabilités actuels** — on ne supprime pas les titres ni les fonctions des gens.
4. **Encourager le leadership à tous les niveaux** — les bonnes idées d'amélioration peuvent venir de n'importe qui.

### 7.3 Les pratiques fondamentales

Kanban se résume à six pratiques. Les deux premières sont les plus importantes.

**Pratique 1 — Visualiser le travail.** On matérialise tout le travail sur un **tableau** (le tableau Kanban) divisé en colonnes représentant les étapes du flux. Chaque tâche est une carte qui se déplace de gauche à droite.

```
┌──────────┬──────────────┬──────────────┬──────────┐
│ À FAIRE  │  EN COURS (3)│  REVUE (2)   │  TERMINÉ │
├──────────┼──────────────┼──────────────┼──────────┤
│ [C7]     │ [C3] [C4]    │ [C2]         │ [C1]     │
│ [C8]     │ [C5]         │              │          │
│ [C9]     │              │              │          │
└──────────┴──────────────┴──────────────┴──────────┘
              ▲ limite = 3      ▲ limite = 2
```

Le simple fait de **rendre le travail visible** change tout : on voit immédiatement où ça coince, ce qui s'accumule, qui est surchargé.

**Pratique 2 — Limiter le travail en cours (WIP, *Work In Progress*).** C'est la pratique signature de Kanban, et la plus contre-intuitive. On fixe un **nombre maximum de cartes** autorisées simultanément dans chaque colonne. Dans l'exemple, la colonne « En cours » ne peut pas contenir plus de 3 cartes.

Pourquoi limiter volontairement le travail ? Parce que cela produit trois effets vertueux :

- On est **forcé de terminer** ce qui est en cours avant d'en commencer du nouveau. La devise de Kanban est : *« Stop starting, start finishing »* — arrêtez de commencer, commencez à finir.
- Les **goulots d'étranglement deviennent visibles** : si une colonne est pleine et bloque tout, on voit exactement où est le problème.
- Le **délai de traitement diminue** mécaniquement (on l'explique juste après).

<div class="callout danger"><span class="title">❗ Le multitâche détruit le débit</span>
Sans limite de WIP, le réflexe humain est de tout commencer en même temps. Résultat : dix choses en cours, zéro terminée, et un client qui attend tout. Limiter le WIP semble ralentir l'équipe (« comment ça, je ne peux pas commencer une nouvelle tâche ?! »), mais c'est en réalité le <b>levier numéro un</b> pour livrer plus vite. C'est prouvé par la loi de Little, ci-dessous.
</div>

### 7.4 Les métriques du flux

Kanban se pilote avec des chiffres simples.

| Métrique | Définition | À quoi elle sert |
|----------|------------|------------------|
| **Lead time** (délai de livraison) | Temps total entre le moment où le client demande quelque chose et le moment où il le reçoit | Prévoir et tenir des délais |
| **Cycle time** (temps de cycle) | Temps entre le début effectif du travail et sa fin | Améliorer l'exécution |
| **Throughput** (débit) | Nombre de tâches terminées par unité de temps (par semaine, par exemple) | Mesurer la capacité réelle de l'équipe |
| **WIP** | Nombre de tâches en cours à un instant donné | Réguler le flux |

Ces métriques sont reliées par une formule célèbre, la **loi de Little** :

> **Lead time ≈ WIP ÷ Throughput**

Lisons-la : si une équipe a 20 tâches en cours (WIP) et en termine 5 par semaine (throughput), le délai moyen est d'environ 20 ÷ 5 = **4 semaines**. Si l'on réduit le WIP à 10 (à débit constant), le délai tombe à 10 ÷ 5 = **2 semaines**. **Voilà pourquoi limiter le WIP accélère la livraison.**

<div class="callout note"><span class="title">📘 Le diagramme de flux cumulé (CFD)</span>
Le <i>Cumulative Flow Diagram</i> est un graphique qui empile, jour après jour, le nombre de tâches dans chaque état. Sa lecture est intuitive : une bande qui <b>s'élargit</b> dans le temps signale une <b>accumulation</b> (un goulot d'étranglement) ; des bandes <b>parallèles et fines</b> signalent un <b>flux sain</b> et régulier.
</div>

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 3 : simuler un flux Kanban</span>
Modélisez le flux du support de QuickBite (colonnes : Backlog → Analyse → Dev → Test → Déployé). Posez des limites de WIP réalistes. Simulez 5 « jours » en faisant entrer 2 cartes par jour et en avançant les cartes selon une capacité par colonne. Notez le délai de chaque carte. Vous verrez très probablement un <b>goulot</b> apparaître dans une colonne (souvent « Test »). Baissez alors une limite de WIP en amont, ou renforcez la colonne saturée, et rejouez : observez l'effet sur le délai moyen.
</div>

**Ce que l'exercice doit révéler :** le goulot apparaît là où les cartes s'empilent. La solution n'est presque jamais de « travailler plus vite », mais de **lisser le flux** : réduire ce qui entre en amont, ou aider la colonne saturée (entraide, ce qu'on appelle le *swarming*). La leçon profonde, issue de la *théorie des contraintes*, est qu'**optimiser chaque poste isolément ne sert à rien ; il faut optimiser le flux dans son ensemble.**

---

## Chapitre 8 — Scrum, Kanban ou ScrumBan ? Et les outils

### 8.1 Le tableau comparatif

| Critère | Scrum | Kanban |
|---------|-------|--------|
| Rythme | Itérations de durée fixe (sprints) | Flux continu, sans itérations |
| Rôles | PO, Scrum Master, Développeurs | Aucun rôle imposé |
| Engagement | Un Sprint Goal par sprint | Pas d'engagement par lot |
| Limite du travail | La capacité du sprint | Une limite de WIP par colonne |
| Changement en cours de route | Évité pendant le sprint | Possible à tout moment |
| Idéal pour… | Développer un nouveau produit | Un flux continu et imprévisible |

### 8.2 Comment choisir

- Choisissez **Scrum** quand vous **développez un produit** et que vous avez besoin de cadence, d'objectifs clairs et d'un travail planifiable par lots. C'est le cas typique d'une équipe qui construit QuickBite.
- Choisissez **Kanban** quand le travail **arrive de façon imprévisible** et qu'on ne peut pas le planifier par sprints : support client, infogérance, exploitation, production de contenu.
- Choisissez **ScrumBan** (un hybride) dans deux cas : soit une équipe Scrum **submergée par les urgences** qui cassent ses sprints, soit une équipe en **transition douce** vers l'agilité. ScrumBan garde certains éléments de Scrum (les rôles, la rétrospective) mais pilote le travail par le **flux et les limites de WIP** plutôt que par des sprints rigides.

<div class="callout tip"><span class="title">💡 Il n'y a pas de « meilleur » cadre</span>
La bonne question n'est jamais « Scrum ou Kanban, lequel est le meilleur ? », mais « <b>quel cadre correspond à la nature de mon travail ?</b> ». Une même entreprise utilise souvent Scrum pour ses équipes produit et Kanban pour son support.
</div>

### 8.3 Les outils du marché

| Outil | Points forts | Idéal pour |
|-------|--------------|------------|
| **Jira** | Très puissant, reporting riche, gère l'agilité à grande échelle | Équipes produit, grandes organisations |
| **Trello** | Extrêmement simple, prise en main immédiate | Petites équipes, Kanban léger |
| **ClickUp** | Polyvalent (tâches, documents, objectifs, vues multiples) | Équipes aux usages variés |
| **GitHub Projects** | Couplé directement au code et aux issues GitHub | Équipes de développeurs |
| **Asana** | Bonne gestion des tâches, des échéances et des dépendances | Coordination transverse |

<div class="callout lab"><span class="title">🧪 Exercice — créer votre premier board</span>
Sur <b>Trello</b> ou <b>GitHub Projects</b> (comptes gratuits) : créez le tableau QuickBite, ajoutez les colonnes d'un flux, créez 6 cartes à partir des User Stories de l'atelier 2, ajoutez des étiquettes de couleur pour le classement MoSCoW, et déplacez deux cartes pour simuler l'avancement. Si l'outil le permet, activez une limite de WIP sur la colonne « En cours ».
</div>

### 8.4 Récapitulatif du Module 1

Au terme de ce module, retenez la ligne directrice : **l'Agilité consiste à livrer de la valeur tôt et souvent, à apprendre des retours, et à s'adapter en continu.** Scrum organise cela par des **sprints** avec des rôles et des cérémonies ; Kanban l'organise par un **flux** qu'on visualise et qu'on limite. Dans les deux cas, le but final est identique : raccourcir la boucle entre une idée et sa validation par un vrai utilisateur.

Dans le Module 2, nous verrons **comment livrer techniquement** ce produit, vite et de façon fiable, grâce au DevOps.
