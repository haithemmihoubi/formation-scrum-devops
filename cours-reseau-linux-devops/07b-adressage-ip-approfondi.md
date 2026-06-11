# Module 07b — L'adressage IP expliqué pas à pas (+ exercices corrigés)

🎯 **Objectif** : comprendre l'adressage IPv4 **en profondeur** et savoir calculer
n'importe quel sous-réseau à la main. Ce module complète le [Module 07](07-reseau-adressage-ip.md).

---

## PARTIE 1 — Comprendre ce qu'est une adresse IP

### 1.1 L'idée de base

Une adresse IP, c'est comme une **adresse postale** pour une machine. Elle doit être
**unique** dans son réseau pour que les données arrivent au bon endroit.

Une adresse IPv4 = **32 bits**, découpés en **4 octets** (4 paquets de 8 bits) :

```
   192    .   168    .    1    .   10
 11000000 . 10101000 . 00000001 . 00001010
  octet 1    octet 2    octet 3   octet 4
```

Chaque octet va de **0 à 255** (car 8 bits → 2⁸ = 256 valeurs possibles).

### 1.2 Convertir binaire ↔ décimal (la base de tout)

Chaque bit d'un octet a un **poids** :

```
 Poids :  128  64  32  16   8   4   2   1
 Bit   :   1    1   0   0   0   0   0   0   = 128 + 64 = 192
```

**Méthode décimal → binaire** : on soustrait du plus grand poids au plus petit.

Exemple : convertir **168**
```
168 ≥ 128 ? oui → bit=1, reste 168-128 = 40
 40 ≥  64 ? non → bit=0
 40 ≥  32 ? oui → bit=1, reste 40-32 = 8
  8 ≥  16 ? non → bit=0
  8 ≥   8 ? oui → bit=1, reste 0
  0 ≥   4 ? non → bit=0
  0 ≥   2 ? non → bit=0
  0 ≥   1 ? non → bit=0
Résultat : 10101000
```

**Méthode binaire → décimal** : on additionne les poids des bits à 1.
```
10101000 = 128 + 32 + 8 = 168 ✅
```

> 💡 Apprenez par cœur les poids : **128 - 64 - 32 - 16 - 8 - 4 - 2 - 1**.
> C'est l'outil n°1 du subnetting.

---

## PARTIE 2 — Le masque de sous-réseau

### 2.1 À quoi sert le masque ?

Une adresse IP contient **2 informations** mélangées :
- la **partie réseau** : « dans quel quartier j'habite »
- la **partie hôte** : « quel numéro de maison »

Le **masque** indique où s'arrête le réseau et où commence l'hôte.
Les bits à **1** du masque = partie **réseau**. Les bits à **0** = partie **hôte**.

```
IP      : 192.168.1.10   = 11000000.10101000.00000001.00001010
Masque  : 255.255.255.0  = 11111111.11111111.11111111.00000000
                            \_________ réseau _________/\_ hôte _/
```

### 2.2 La notation CIDR (/n)

Au lieu d'écrire le masque en entier, on écrit le **nombre de bits à 1** :

```
255.255.255.0   →  /24   (24 bits à 1)
255.255.0.0     →  /16
255.0.0.0       →  /8
255.255.255.192 →  /26
```

Donc `192.168.1.10/24` veut dire : IP `192.168.1.10` avec un masque de 24 bits.

### 2.3 Tableau des masques (à garder sous la main)

| CIDR | Masque décimal | Bits hôte | Hôtes utilisables |
|------|----------------|-----------|-------------------|
| /24 | 255.255.255.0 | 8 | 254 |
| /25 | 255.255.255.128 | 7 | 126 |
| /26 | 255.255.255.192 | 6 | 62 |
| /27 | 255.255.255.224 | 5 | 30 |
| /28 | 255.255.255.240 | 4 | 14 |
| /29 | 255.255.255.248 | 3 | 6 |
| /30 | 255.255.255.252 | 2 | 2 |

> 📌 Les valeurs du dernier octet des masques : **128, 192, 224, 240, 248, 252, 254, 255**.
> Mémorisez-les, elles reviennent tout le temps.

---

## PARTIE 3 — Les 4 nombres clés d'un réseau

Pour **tout** réseau, on calcule 4 choses :

1. **Adresse réseau** : la première adresse → identifie le réseau (non assignable).
2. **Première adresse utilisable** : adresse réseau + 1.
3. **Dernière adresse utilisable** : broadcast − 1.
4. **Adresse de broadcast** : la dernière adresse → envoie à tout le monde (non assignable).

### Formule du nombre d'hôtes

```
Nombre d'hôtes utilisables = 2^(bits hôte) − 2
```
Le **−2** correspond à l'adresse réseau et au broadcast, qu'on ne peut pas donner à une machine.

Exemple `/24` : bits hôte = 8 → 2⁸ − 2 = 256 − 2 = **254 hôtes**.

---

## PARTIE 4 — Méthode universelle de calcul (à appliquer toujours)

Voici **LA** méthode à suivre pour n'importe quel exercice de subnetting.

> **Donnée** : une IP + un CIDR, par exemple `192.168.1.100/26`.

**Étape 1 — Trouver le masque et l'octet « intéressant ».**
`/26` → masque `255.255.255.192`. Le 4ᵉ octet (192) est l'octet qui change.

**Étape 2 — Calculer le « pas » (block size).**
```
Pas = 256 − valeur de l'octet du masque
Pas = 256 − 192 = 64
```
Les réseaux vont donc de 64 en 64 : `0, 64, 128, 192`.

**Étape 3 — Situer l'IP dans le bon bloc.**
L'IP finit par `.100`. Entre quels multiples de 64 ? → entre 64 et 128.
Donc **adresse réseau = .64**.

**Étape 4 — En déduire les 4 nombres.**
```
Adresse réseau    : 192.168.1.64
1ʳᵉ utilisable    : 192.168.1.65
Dernière utilisable: 192.168.1.126
Broadcast         : 192.168.1.127   (réseau suivant .128, donc broadcast = .127)
```

✅ Avec ces 4 étapes (masque → pas → bloc → 4 nombres), vous résolvez **tout**.

---

## PARTIE 5 — Le subnetting : découper un réseau

### 5.1 Pourquoi découper ?

- **Sécurité** : isoler des groupes (serveurs, postes, invités).
- **Performance** : réduire les domaines de broadcast.
- **Organisation** : un sous-réseau par service / par zone cloud.

### 5.2 Découper selon un nombre de SOUS-RÉSEAUX

On **emprunte des bits** à la partie hôte. Pour obtenir N sous-réseaux, il faut
**b** bits tels que `2^b ≥ N`.

| Sous-réseaux voulus | Bits à emprunter |
|---------------------|------------------|
| 2 | 1 |
| 4 | 2 |
| 8 | 3 |
| 16 | 4 |
| 32 | 5 |

Exemple : découper `192.168.1.0/24` en **4** sous-réseaux.
- 4 = 2² → emprunter **2 bits** → nouveau masque `/24 + 2 = /26`.
- Pas = 256 − 192 = 64.
- Sous-réseaux : `.0`, `.64`, `.128`, `.192`.

### 5.3 Découper selon un nombre d'HÔTES

On garde **assez de bits hôte** pour le besoin : `2^h − 2 ≥ hôtes voulus`.

Exemple : il me faut un réseau pour **50 machines**.
- `2^5 − 2 = 30` ❌ (trop peu) → `2^6 − 2 = 62` ✅
- 6 bits hôte → masque `/26`.

---

## PARTIE 6 — EXERCICES CORRIGÉS

> Essayez **avant** de dérouler la solution. Prenez un papier et appliquez la méthode des 4 étapes.

### 🟢 Niveau 1 — Lecture d'adresse

**Exercice 1.1** — `10.20.30.40` est-elle privée ou publique ?

<details><summary>Solution</summary>

`10.x.x.x` appartient à la plage privée `10.0.0.0 – 10.255.255.255` → **privée**.
</details>

**Exercice 1.2** — Convertir `192` et `240` en binaire.

<details><summary>Solution</summary>

- `192` = 128 + 64 = `11000000`
- `240` = 128 + 64 + 32 + 16 = `11110000`
</details>

**Exercice 1.3** — Convertir `10101100` en décimal.

<details><summary>Solution</summary>

128 + 32 + 8 + 4 = **172**.
</details>

---

### 🟡 Niveau 2 — Réseau / Broadcast

**Exercice 2.1** — Pour `192.168.10.0/24`, donnez adresse réseau, 1ʳᵉ et dernière utilisable, broadcast.

<details><summary>Solution</summary>

- Masque `/24` → pas = 256 − 255... non : le 4ᵉ octet du masque vaut 0, on prend tout l'octet.
- Réseau : `192.168.10.0`
- 1ʳᵉ utilisable : `192.168.10.1`
- Dernière utilisable : `192.168.10.254`
- Broadcast : `192.168.10.255`
- Hôtes : 2⁸ − 2 = **254**
</details>

**Exercice 2.2** — Combien d'hôtes utilisables dans un `/16` ?

<details><summary>Solution</summary>

Bits hôte = 32 − 16 = 16 → 2¹⁶ − 2 = 65 536 − 2 = **65 534**.
</details>

**Exercice 2.3** — Quel est le masque décimal d'un `/27` ? Combien d'hôtes ?

<details><summary>Solution</summary>

- `/27` → 3 octets pleins + 3 bits → 4ᵉ octet = 11100000 = 224 → `255.255.255.224`
- Bits hôte = 5 → 2⁵ − 2 = **30 hôtes**
</details>

---

### 🟠 Niveau 3 — Méthode des 4 étapes

**Exercice 3.1** — Pour l'IP `192.168.1.100/26`, donnez les 4 nombres du réseau auquel elle appartient.

<details><summary>Solution</summary>

1. Masque `/26` = `255.255.255.192`, octet intéressant = 4ᵉ.
2. Pas = 256 − 192 = **64** → blocs : 0, 64, 128, 192.
3. `.100` est entre 64 et 128 → réseau = **.64**.
4.
   - Réseau : `192.168.1.64`
   - 1ʳᵉ utilisable : `192.168.1.65`
   - Dernière utilisable : `192.168.1.126`
   - Broadcast : `192.168.1.127`
</details>

**Exercice 3.2** — Pour `172.16.5.200/28`, donnez réseau et broadcast.

<details><summary>Solution</summary>

1. `/28` = `255.255.255.240`, pas = 256 − 240 = **16**.
2. Blocs : 0, 16, 32, ... 192, **208**, ... `.200` est entre 192 et 208 → réseau = **.192**.
3.
   - Réseau : `172.16.5.192`
   - Broadcast : `172.16.5.207` (réseau suivant .208 → broadcast = .207)
   - Utilisables : `.193` à `.206` (14 hôtes)
</details>

**Exercice 3.3** — `10.0.0.130/25` appartient à quel réseau ?

<details><summary>Solution</summary>

1. `/25` = `255.255.255.128`, pas = 256 − 128 = **128**.
2. Blocs : 0, 128. `.130` est dans le bloc **.128**.
3.
   - Réseau : `10.0.0.128`
   - 1ʳᵉ utilisable : `10.0.0.129`
   - Dernière : `10.0.0.254`
   - Broadcast : `10.0.0.255`
</details>

---

### 🔴 Niveau 4 — Subnetting (découpage)

**Exercice 4.1** — Découpez `192.168.0.0/24` en **4 sous-réseaux égaux**. Donnez-les tous.

<details><summary>Solution</summary>

- 4 = 2² → emprunter 2 bits → `/26`, pas = 64.

| # | Réseau | Plage utilisable | Broadcast |
|---|--------|------------------|-----------|
| 1 | 192.168.0.0/26 | .1 – .62 | .63 |
| 2 | 192.168.0.64/26 | .65 – .126 | .127 |
| 3 | 192.168.0.128/26 | .129 – .190 | .191 |
| 4 | 192.168.0.192/26 | .193 – .254 | .255 |
</details>

**Exercice 4.2** — Vous avez `172.16.0.0/16` et devez créer **8 sous-réseaux**. Masque ? 3 premiers sous-réseaux ?

<details><summary>Solution</summary>

- 8 = 2³ → emprunter 3 bits → `/16 + 3 = /19` → masque `255.255.224.0`.
- L'octet intéressant est le **3ᵉ**, pas = 256 − 224 = **32**.

| # | Réseau |
|---|--------|
| 1 | 172.16.0.0/19 |
| 2 | 172.16.32.0/19 |
| 3 | 172.16.64.0/19 |

Chaque sous-réseau : 2^(32−19) − 2 = 2¹³ − 2 = **8190 hôtes**.
</details>

**Exercice 4.3** — Il vous faut un réseau pour **exactement 100 machines**. Quel est le plus petit masque possible ?

<details><summary>Solution</summary>

- `2^6 − 2 = 62` ❌ ; `2^7 − 2 = 126` ✅ → besoin de **7 bits hôte**.
- Masque = 32 − 7 = **/25** (`255.255.255.128`).
- Capacité : 126 hôtes (couvre les 100).
</details>

**Exercice 4.4 (synthèse)** — Une entreprise reçoit `192.168.50.0/24`. Elle veut :
- un sous-réseau pour 60 PC,
- un sous-réseau pour 25 imprimantes,
- un sous-réseau pour 10 serveurs.

Proposez un découpage (VLSM — masques de tailles variables).

<details><summary>Solution</summary>

On commence par le plus gros besoin (VLSM = on alloue du plus grand au plus petit).

**1) 60 PC** → `2^6 − 2 = 62` ✅ → `/26` (pas 64)
   - `192.168.50.0/26` → .1 à .62 (broadcast .63)

**2) 25 imprimantes** → `2^5 − 2 = 30` ✅ → `/27` (pas 32)
   - On continue après .63 → `192.168.50.64/27` → .65 à .94 (broadcast .95)

**3) 10 serveurs** → `2^4 − 2 = 14` ✅ → `/28` (pas 16)
   - On continue après .95 → `192.168.50.96/28` → .97 à .110 (broadcast .111)

| Usage | Réseau | Masque | Plage | Broadcast |
|-------|--------|--------|-------|-----------|
| PC (60) | 192.168.50.0 | /26 | .1–.62 | .63 |
| Imprimantes (25) | 192.168.50.64 | /27 | .65–.94 | .95 |
| Serveurs (10) | 192.168.50.96 | /28 | .97–.110 | .111 |

Il reste de l'espace libre à partir de `192.168.50.112` pour de futurs réseaux. 🎉
</details>

---

## PARTIE 7 — Vérifier ses calculs sous Linux

Inutile de tout faire à la main en production : des outils valident vos calculs.

```bash
# ipcalc : l'outil idéal d'apprentissage
sudo apt install ipcalc
ipcalc 192.168.1.100/26
# Affiche : Network, HostMin, HostMax, Broadcast, nb d'hôtes...

ipcalc 192.168.0.0/24 -s 60 25 10   # propose un découpage VLSM

# Voir sa propre config
ip a
ip route
```

Exemple de sortie `ipcalc 192.168.1.100/26` :
```
Address:   192.168.1.100
Netmask:   255.255.255.192 = 26
Network:   192.168.1.64/26
HostMin:   192.168.1.65
HostMax:   192.168.1.126
Broadcast: 192.168.1.127
Hosts/Net: 62
```

> 🎯 **En DevOps**, ces calculs servent directement à dimensionner un **VPC AWS**,
> un **subnet Azure**, ou la plage **CIDR des pods** dans Kubernetes.

---

## PARTIE 8 — Mémo express (à imprimer)

```
Poids des bits      : 128 64 32 16 8 4 2 1
Valeurs de masque   : 128 192 224 240 248 252 254 255
Hôtes utilisables   : 2^(bits hôte) − 2
Pas (block size)    : 256 − octet du masque

Méthode 4 étapes :
 1. Masque + octet intéressant
 2. Pas = 256 − octet du masque
 3. Trouver le bloc qui contient l'IP → adresse réseau
 4. Réseau / 1ʳᵉ / dernière / broadcast
```

| CIDR | Masque | Hôtes |
|------|--------|-------|
| /24 | .0 | 254 |
| /25 | .128 | 126 |
| /26 | .192 | 62 |
| /27 | .224 | 30 |
| /28 | .240 | 14 |
| /29 | .248 | 6 |
| /30 | .252 | 2 |

---

## Exercices supplémentaires (sans solution — entraînez-vous !)

1. `10.10.10.77/26` → réseau, broadcast, plage utilisable.
2. Découpez `192.168.100.0/24` en 8 sous-réseaux. Donnez les 8.
3. Il vous faut 500 hôtes : quel masque minimum ?
4. `172.16.20.130/25` appartient à quel réseau ?
5. Convertissez `255.255.255.248` en notation CIDR.
6. VLSM sur `10.0.0.0/24` pour : 100 hôtes, 50 hôtes, 20 hôtes, 2 hôtes (liaison).

> 💡 Vérifiez vos réponses avec `ipcalc`.

> 🔙 Retour au [Module 07](07-reseau-adressage-ip.md) ou au [sommaire](README.md).
