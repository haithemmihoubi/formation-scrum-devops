# Module 06 — Réseau : Fondamentaux & Modèles

🎯 **Objectif** : comprendre comment les données circulent sur un réseau, base indispensable du DevOps.

## 1. Qu'est-ce qu'un réseau ?

Un **réseau** est un ensemble d'équipements (ordinateurs, serveurs, routeurs...) interconnectés qui s'échangent des données. Internet est le « réseau des réseaux ».

Types de réseaux :
- **LAN** (Local Area Network) : réseau local (maison, bureau)
- **WAN** (Wide Area Network) : étendu (entre villes, Internet)
- **VLAN** : réseau local virtuel (segmentation logique)
- **VPN** : réseau privé virtuel (tunnel sécurisé)

## 2. Le modèle OSI (7 couches)

Le modèle **OSI** décrit comment les données voyagent, en 7 couches :

| # | Couche | Rôle | Exemples |
|---|--------|------|----------|
| 7 | Application | Interface utilisateur | HTTP, DNS, SSH, FTP |
| 6 | Présentation | Format, chiffrement | TLS/SSL, JPEG |
| 5 | Session | Gère les sessions | sockets |
| 4 | Transport | Fiabilité, ports | TCP, UDP |
| 3 | Réseau | Adressage, routage | IP, ICMP |
| 2 | Liaison | Adresses MAC, trames | Ethernet, ARP |
| 1 | Physique | Signaux, câbles | câbles, Wi-Fi |

💡 Moyen mnémotechnique : « **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing » (de 7 à 1).

## 3. Le modèle TCP/IP (4 couches — le vrai)

En pratique, Internet utilise le modèle **TCP/IP**, plus simple :

| Couche TCP/IP | Équivaut OSI | Protocoles |
|---------------|--------------|------------|
| Application | 5-6-7 | HTTP, DNS, SSH, FTP |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP |
| Accès réseau | 1-2 | Ethernet, Wi-Fi |

## 4. L'encapsulation

Quand vous envoyez des données, chaque couche ajoute un **en-tête** (header) :

```
[ Données ]
[ En-tête TCP | Données ]                 → Segment
[ En-tête IP | TCP | Données ]            → Paquet
[ En-tête Ethernet | IP | TCP | Données ] → Trame
```

À la réception, le processus inverse (décapsulation) retire les en-têtes couche par couche.

## 5. Adresses MAC vs adresses IP

- **Adresse MAC** : identifiant physique de la carte réseau, gravé en usine (ex : `00:1A:2B:3C:4D:5E`). Unique, ne change pas. Couche 2.
- **Adresse IP** : identifiant logique, attribué par le réseau, peut changer (ex : `192.168.1.10`). Couche 3.

Analogie : la MAC est comme le numéro de série de votre téléphone, l'IP est comme votre numéro de téléphone (qui peut changer d'opérateur).

## 6. TCP vs UDP (couche transport)

| Critère | TCP | UDP |
|---------|-----|-----|
| Connexion | Orienté connexion | Sans connexion |
| Fiabilité | Garantie (accusés de réception) | Aucune garantie |
| Ordre | Données dans l'ordre | Pas d'ordre garanti |
| Vitesse | Plus lent | Plus rapide |
| Usage | Web, mail, SSH, BDD | Streaming, DNS, jeux, VoIP |

**TCP — Three-way handshake** (établissement de connexion) :
```
Client  --- SYN --->     Serveur
Client  <-- SYN-ACK ---  Serveur
Client  --- ACK --->     Serveur
   (connexion établie)
```

## 7. Les ports

Un **port** identifie un service précis sur une machine (0–65535).
Une connexion = IP source:port → IP destination:port.

Ports « bien connus » à mémoriser :

| Port | Service |
|------|---------|
| 20/21 | FTP |
| 22 | SSH |
| 25 | SMTP (mail) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP alternatif |
| 27017 | MongoDB |

💡 Ports < 1024 = privilégiés (nécessitent root pour être ouverts).

## 8. Les équipements réseau

- **Switch (commutateur)** : relie les machines d'un LAN (couche 2, MAC).
- **Routeur** : relie des réseaux différents, fait du routage (couche 3, IP).
- **Passerelle (gateway)** : porte de sortie vers d'autres réseaux.
- **Load balancer** : répartit le trafic entre plusieurs serveurs.
- **Pare-feu (firewall)** : filtre le trafic selon des règles.
- **Proxy / Reverse proxy** : intermédiaire (Nginx, HAProxy).

## 9. Le chemin d'une requête web (vue d'ensemble)

Quand vous tapez `https://exemple.com` :
1. **DNS** : `exemple.com` → adresse IP (ex : `93.184.216.34`).
2. **TCP** : ouverture de connexion (handshake) sur le port 443.
3. **TLS** : négociation du chiffrement (HTTPS).
4. **HTTP** : envoi de la requête `GET /`.
5. Le serveur répond avec le HTML.
6. Le navigateur affiche la page.

🎯 En DevOps, comprendre ce chemin permet de savoir **où** ça casse (DNS ? réseau ? appli ? certificat ?).

## Exercices

1. Citez les 7 couches du modèle OSI dans l'ordre.
2. Quelle est la différence entre une adresse MAC et une adresse IP ?
3. Pour télécharger un gros fichier de façon fiable, TCP ou UDP ?
4. Sur quel port tourne HTTPS ? Et SSH ? Et PostgreSQL ?
5. Décrivez les 3 étapes du three-way handshake TCP.
6. Expliquez ce qui se passe quand on tape une URL dans un navigateur.

> ✅ Passez au [Module 07 — Adressage IP](07-reseau-adressage-ip.md).
