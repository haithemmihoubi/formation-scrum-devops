# Cours détaillé : Réseau & Linux pour le DevOps

Bienvenue dans ce cours complet conçu pour donner toutes les bases **Linux** et **Réseau** indispensables à une carrière DevOps. Le cours alterne théorie, commandes pratiques et exercices.

## Public visé
- Futurs ingénieurs DevOps / SRE
- Développeurs souhaitant maîtriser l'infrastructure
- Administrateurs systèmes en reconversion

## Prérequis
- Notions de base en informatique
- Un ordinateur avec accès à un terminal Linux (machine, VM, WSL2 ou conteneur Docker)

## Plan du cours

| # | Module | Description |
|---|--------|-------------|
| 00 | [Introduction au DevOps](00-introduction-devops.md) | Culture, principes, place de Linux/réseau |
| 01 | [Linux — Fondamentaux](01-linux-fondamentaux.md) | Système de fichiers, commandes essentielles |
| 02 | [Linux — Utilisateurs & Permissions](02-linux-utilisateurs-permissions.md) | Users, groupes, droits, sudo |
| 03 | [Linux — Processus & Services](03-linux-processus-services.md) | Processus, systemd, journaux, cron |
| 04 | [Linux — Gestion des paquets & stockage](04-linux-paquets-stockage.md) | apt/yum, disques, montage, LVM |
| 05 | [Bash Scripting](05-bash-scripting.md) | Variables, conditions, boucles, fonctions |
| 06 | [Réseau — Fondamentaux & modèles](06-reseau-fondamentaux.md) | OSI, TCP/IP, encapsulation |
| 07 | [Réseau — Adressage IP & sous-réseaux](07-reseau-adressage-ip.md) | IPv4, masques, subnetting, CIDR |
| 07b | [Adressage IP approfondi (+ exos corrigés)](07b-adressage-ip-approfondi.md) | Méthode pas à pas, calculs, VLSM, exercices |
| 08 | [Réseau — Protocoles & services](08-reseau-protocoles-services.md) | DNS, DHCP, HTTP, SSH, TLS |
| 09 | [Réseau — Diagnostic & outils Linux](09-reseau-outils-diagnostic.md) | ping, ip, ss, tcpdump, curl |
| 10 | [Sécurité & Pare-feu](10-securite-parefeu.md) | iptables, firewalld, SSH durci, bonnes pratiques |
| 11 | [Mise en pratique DevOps](11-pratique-devops.md) | Conteneurs, reverse proxy, CI/CD, projet final |
| 12 | [Travaux pratiques & exercices](12-travaux-pratiques.md) | TP guidés et corrigés |

## Comment suivre ce cours
1. Lisez chaque module dans l'ordre.
2. Reproduisez **toutes** les commandes dans votre terminal.
3. Faites les exercices à la fin de chaque module avant de passer au suivant.
4. Tenez un fichier de notes personnelles.

## Conventions
- `$` : commande exécutée en utilisateur normal
- `#` : commande exécutée en root (ou avec `sudo`)
- Les blocs `bash` sont à reproduire tels quels
- 💡 = astuce, ⚠️ = attention, 🎯 = objectif DevOps

---
Bon apprentissage ! 🚀
