# Module 09 — Réseau : Diagnostic & Outils Linux

🎯 **Objectif** : savoir diagnostiquer un problème réseau, compétence quotidienne du DevOps.

## 1. La méthode de diagnostic (couche par couche)

Quand « ça ne marche pas », remontez les couches :
1. **Physique/interface** : la carte réseau est-elle UP ? (`ip a`)
2. **IP** : ai-je une adresse, une route ? (`ip a`, `ip route`)
3. **Connectivité** : puis-je joindre la machine ? (`ping`)
4. **DNS** : le nom se résout-il ? (`dig`, `nslookup`)
5. **Port/Service** : le port est-il ouvert ? (`ss`, `nc`, `telnet`)
6. **Application** : l'appli répond-elle ? (`curl`)

## 2. Voir la configuration réseau

```bash
ip a                 # adresses IP des interfaces
ip link              # état des interfaces (UP/DOWN)
ip route             # table de routage
ip neigh             # table ARP (voisins)
hostname -I          # IP de la machine
cat /etc/resolv.conf # serveurs DNS

# Anciennes commandes (paquet net-tools, encore courantes)
ifconfig             # config interfaces
route -n             # routage
netstat -tulpn       # ports en écoute
```

## 3. Tester la connectivité : ping

`ping` envoie des paquets ICMP pour tester si une machine répond.

```bash
ping google.com           # test continu (Ctrl+C pour arrêter)
ping -c 4 google.com      # 4 paquets seulement
ping -c 4 8.8.8.8         # tester par IP (isole le DNS)
```

💡 Si `ping 8.8.8.8` marche mais `ping google.com` échoue → **problème DNS**.

## 4. Tracer le chemin : traceroute

Affiche tous les routeurs (sauts) jusqu'à la destination.

```bash
traceroute google.com     # chemin complet
tracepath google.com      # variante sans root
mtr google.com            # traceroute + ping en continu (top !)
```

## 5. Tester un port : la vraie question DevOps

« Le port est-il ouvert et joignable ? »

```bash
# Avec netcat (nc)
nc -zv serveur 22         # teste le port 22
nc -zv 192.168.1.10 80    # teste le port 80

# Avec telnet
telnet serveur 443

# Test bash pur (sans outil)
timeout 2 bash -c "echo > /dev/tcp/serveur/22" && echo "ouvert" || echo "fermé"

# Scanner plusieurs ports avec nmap
nmap -p 1-1000 serveur    # scan de ports
nmap -sV serveur          # détecte les versions de services
```

## 6. Voir les connexions et ports en écoute : ss

`ss` (remplace `netstat`) montre les sockets/connexions.

```bash
ss -tulpn          # TCP+UDP en écoute, avec processus et ports
ss -t              # connexions TCP établies
ss -tan            # toutes les connexions TCP (numérique)
ss -s              # statistiques résumées
ss -tp state established  # connexions actives
```

Options : `-t` TCP, `-u` UDP, `-l` listening, `-p` processus, `-n` numérique.

🎯 **Cas typique** : « mon app écoute-t-elle bien sur le port 3000 ? »
```bash
ss -tulpn | grep 3000
```

## 7. Analyser le trafic : tcpdump

Capture les paquets réseau pour un diagnostic approfondi.

```bash
sudo tcpdump -i eth0                       # capture sur eth0
sudo tcpdump -i any port 80                # uniquement le port 80
sudo tcpdump -i any host 192.168.1.10      # une IP précise
sudo tcpdump -i any port 443 -w capture.pcap  # sauver pour Wireshark
sudo tcpdump -i any -n port 53             # voir les requêtes DNS
```

💡 Le fichier `.pcap` s'analyse ensuite dans **Wireshark** (interface graphique).

## 8. Télécharger / tester des URL : curl & wget

```bash
# curl (le couteau suisse)
curl -I https://exemple.com               # en-têtes
curl -v https://exemple.com               # debug complet
curl -L https://exemple.com               # suit les redirections
curl --resolve exemple.com:443:1.2.3.4 https://exemple.com  # forcer une IP
curl -w "DNS:%{time_namelookup} Connect:%{time_connect} Total:%{time_total}\n" \
     -s -o /dev/null https://exemple.com  # mesurer les temps

# wget
wget https://exemple.com/fichier.zip      # télécharger
wget -c https://...                        # reprendre un téléchargement
```

## 9. Le pare-feu local en diagnostic

Parfois « le port est fermé » = le pare-feu bloque.

```bash
sudo iptables -L -n -v      # règles iptables
sudo ufw status verbose     # statut UFW (Ubuntu)
sudo firewall-cmd --list-all  # firewalld (RHEL)
```

(Détaillé dans le [Module 10](10-securite-parefeu.md).)

## 10. Scénarios de diagnostic concrets

**Scénario A — « Le site ne répond pas »**
```bash
ping -c2 site.com           # 1. réseau OK ?
dig +short site.com         # 2. DNS résout ?
nc -zv site.com 443         # 3. port ouvert ?
curl -I https://site.com    # 4. appli répond ?
```

**Scénario B — « Mon conteneur ne joint pas la BDD »**
```bash
ss -tulpn | grep 5432       # la BDD écoute-t-elle ?
nc -zv db-host 5432         # joignable depuis ici ?
ping db-host                # résolution + réseau ?
```

**Scénario C — « Lenteur réseau »**
```bash
mtr destination             # où est la latence ?
curl -w "@format.txt" ...   # décomposer les temps
```

## 11. Tableau récapitulatif des outils

| Besoin | Outil |
|--------|-------|
| Voir mon IP / routes | `ip a`, `ip route` |
| Tester si une machine répond | `ping` |
| Tracer le chemin | `traceroute`, `mtr` |
| Tester un port | `nc -zv`, `nmap` |
| Voir mes ports ouverts | `ss -tulpn` |
| Résoudre un nom | `dig`, `nslookup` |
| Tester une URL HTTP | `curl`, `wget` |
| Capturer le trafic | `tcpdump`, Wireshark |

## Exercices

1. Affichez l'adresse IP et la passerelle par défaut de votre machine.
2. Vérifiez si `8.8.8.8` répond avec exactement 3 paquets.
3. Listez tous les ports en écoute sur votre machine avec le nom des processus.
4. Testez si le port 443 de `github.com` est ouvert avec `nc`.
5. Tracez le chemin réseau jusqu'à `1.1.1.1`.
6. Avec `curl`, mesurez le temps total de chargement d'un site web.

> ✅ Passez au [Module 10 — Sécurité & Pare-feu](10-securite-parefeu.md).
