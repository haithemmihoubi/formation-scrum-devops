# Module 07 — Réseau : Adressage IP & Sous-réseaux

🎯 **Objectif** : maîtriser l'adressage IPv4, les masques et le subnetting (essentiel pour le cloud et Kubernetes).

## 1. L'adresse IPv4

Une adresse IPv4 est composée de **4 octets** (32 bits), notés en décimal séparés par des points :

```
192.168.1.10
 |   |   | |
 octets (0 à 255 chacun)
```

En binaire :
```
192      168      1        10
11000000 10101000 00000001 00001010
```

Chaque octet = 8 bits → 2⁸ = 256 valeurs (0 à 255).

## 2. Adresses privées vs publiques

**Adresses privées** (non routables sur Internet, usage interne) :
| Plage | Classe | Usage |
|-------|--------|-------|
| 10.0.0.0 – 10.255.255.255 | A | Grandes entreprises |
| 172.16.0.0 – 172.31.255.255 | B | Moyennes |
| 192.168.0.0 – 192.168.255.255 | C | Maison / petits réseaux |

**Adresses publiques** : tout le reste, uniques sur Internet, attribuées par les FAI.

Adresses spéciales :
- `127.0.0.1` : **localhost** (la machine elle-même, loopback)
- `0.0.0.0` : toutes les interfaces / route par défaut
- `255.255.255.255` : broadcast

## 3. Le masque de sous-réseau

Le **masque** sépare l'adresse en deux parties :
- **Partie réseau** (network) : identifie le réseau
- **Partie hôte** (host) : identifie la machine dans le réseau

```
IP      : 192.168.1.10
Masque  : 255.255.255.0
          \_______/  \_/
           réseau    hôte
```

Le masque `255.255.255.0` signifie : les 3 premiers octets = réseau, le dernier = hôtes.

## 4. La notation CIDR

CIDR = nombre de bits à 1 dans le masque, noté `/n` :

| Masque décimal | CIDR | Nb d'hôtes utilisables |
|----------------|------|------------------------|
| 255.0.0.0 | /8 | 16 777 214 |
| 255.255.0.0 | /16 | 65 534 |
| 255.255.255.0 | /24 | 254 |
| 255.255.255.128 | /25 | 126 |
| 255.255.255.192 | /26 | 62 |
| 255.255.255.224 | /27 | 30 |
| 255.255.255.240 | /28 | 14 |

Exemple : `192.168.1.0/24` = réseau avec 256 adresses (254 utilisables).

📌 **Formule** : nombre d'hôtes utilisables = 2^(bits hôte) − 2
(on retire l'adresse réseau et l'adresse de broadcast).

## 5. Adresse réseau, broadcast et plage utilisable

Pour `192.168.1.0/24` :
- **Adresse réseau** : `192.168.1.0` (première, non assignable)
- **Première utilisable** : `192.168.1.1`
- **Dernière utilisable** : `192.168.1.254`
- **Broadcast** : `192.168.1.255` (dernière, envoie à tous)

## 6. Le subnetting (découpage)

Découper un réseau en sous-réseaux plus petits.

Exemple : on a `192.168.1.0/24` et on veut **4 sous-réseaux**.
- 4 = 2² → on emprunte **2 bits** à la partie hôte.
- Nouveau masque : `/24 + 2 = /26` → `255.255.255.192`
- Chaque sous-réseau a 2^(8-2) = 64 adresses (62 utilisables).

| Sous-réseau | Plage | Broadcast |
|-------------|-------|-----------|
| 192.168.1.0/26 | .1 – .62 | .63 |
| 192.168.1.64/26 | .65 – .126 | .127 |
| 192.168.1.128/26 | .129 – .190 | .191 |
| 192.168.1.192/26 | .193 – .254 | .255 |

🎯 **Pourquoi c'est utile en DevOps ?** Dans AWS/Azure/GCP, vous créez des **VPC** et des **subnets** avec ces notations CIDR. Kubernetes attribue aussi des plages CIDR aux pods et services.

## 7. La passerelle par défaut (gateway)

C'est l'adresse du routeur qui permet de sortir du réseau local. Souvent `.1` ou `.254`.

```
Machine : 192.168.1.10/24
Gateway : 192.168.1.1
```

Tout trafic vers une IP hors du réseau local passe par la gateway.

## 8. IPv6 (notion)

IPv4 est limité (~4 milliards d'adresses, épuisées). IPv6 utilise **128 bits** :
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```
- Notation hexadécimale, 8 groupes de 4
- Les zéros peuvent être compressés : `2001:db8:85a3::8a2e:370:7334`
- `::1` = localhost en IPv6

## 9. NAT (Network Address Translation)

Le **NAT** permet à plusieurs machines d'un réseau privé de partager une seule IP publique. Votre box fait du NAT : toutes vos machines (192.168.x.x) sortent sur Internet avec une seule IP publique.

🎯 En cloud, le NAT Gateway permet aux instances privées d'accéder à Internet sans être exposées.

## 10. Configurer une IP sous Linux

```bash
ip addr show                # afficher les adresses IP
ip a                        # raccourci
ip route show               # table de routage
ip route get 8.8.8.8        # quelle route pour cette IP ?

# Configuration temporaire
sudo ip addr add 192.168.1.50/24 dev eth0
sudo ip route add default via 192.168.1.1

# Configuration permanente (Ubuntu = netplan)
# /etc/netplan/00-config.yaml
```

Exemple netplan :
```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.50/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

## Exercices

1. Pour le réseau `10.0.0.0/8`, combien d'hôtes utilisables ?
2. Donnez l'adresse réseau et le broadcast de `192.168.10.0/24`.
3. Découpez `192.168.0.0/24` en 2 sous-réseaux. Donnez leurs plages.
4. Quelle est l'adresse de loopback ? À quoi sert-elle ?
5. `172.20.5.3` est-elle une adresse privée ou publique ?
6. Quel masque décimal correspond à `/27` ? Combien d'hôtes utilisables ?

> ✅ Passez au [Module 08 — Protocoles & Services](08-reseau-protocoles-services.md).
