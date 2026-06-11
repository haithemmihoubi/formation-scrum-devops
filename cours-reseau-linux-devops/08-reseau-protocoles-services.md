# Module 08 — Réseau : Protocoles & Services

🎯 **Objectif** : comprendre les protocoles applicatifs que tout DevOps manipule au quotidien.

## 1. DNS (Domain Name System)

Le DNS traduit les **noms de domaine** en **adresses IP**.
`exemple.com` → `93.184.216.34`

**Hiérarchie DNS** :
```
.                    (racine)
└── com              (TLD - Top Level Domain)
    └── exemple      (domaine)
        └── www      (sous-domaine)
```

**Types d'enregistrements DNS** :
| Type | Rôle |
|------|------|
| A | Nom → IPv4 |
| AAAA | Nom → IPv6 |
| CNAME | Alias vers un autre nom |
| MX | Serveur de mail |
| TXT | Texte (SPF, vérifications) |
| NS | Serveur de noms |
| PTR | IP → Nom (reverse) |

**Commandes DNS** :
```bash
nslookup exemple.com         # résolution simple
dig exemple.com              # détaillé
dig exemple.com +short       # juste l'IP
dig MX gmail.com             # serveurs de mail
host exemple.com             # alternative
cat /etc/resolv.conf         # serveurs DNS configurés
cat /etc/hosts               # résolution locale statique
```

💡 `/etc/hosts` permet de forcer une résolution locale (très utile en dev/test).

## 2. DHCP (Dynamic Host Configuration Protocol)

Le DHCP attribue **automatiquement** une configuration IP aux machines :
IP, masque, passerelle, DNS.

Processus DORA :
```
Client → DISCOVER (qui peut me donner une IP ?)
Serveur → OFFER (voici une IP proposée)
Client → REQUEST (je prends celle-là)
Serveur → ACK (validé)
```

## 3. HTTP / HTTPS

**HTTP** (HyperText Transfer Protocol) est le protocole du web (port 80). **HTTPS** = HTTP + chiffrement TLS (port 443).

**Méthodes HTTP** :
| Méthode | Usage |
|---------|-------|
| GET | Lire une ressource |
| POST | Créer une ressource |
| PUT | Remplacer une ressource |
| PATCH | Modifier partiellement |
| DELETE | Supprimer |
| HEAD | En-têtes seulement |

**Codes de statut HTTP** (à connaître par cœur) :
| Code | Signification |
|------|---------------|
| 200 | OK |
| 201 | Created |
| 301/302 | Redirection |
| 400 | Bad Request |
| 401 | Non authentifié |
| 403 | Interdit |
| 404 | Non trouvé |
| 500 | Erreur serveur |
| 502 | Bad Gateway (proxy) |
| 503 | Service indisponible |

🎯 En DevOps, un **502/503** indique souvent un backend en panne derrière un reverse proxy.

**Tester avec curl** :
```bash
curl https://exemple.com                  # récupère le contenu
curl -I https://exemple.com               # en-têtes seulement
curl -v https://exemple.com               # mode verbeux (debug)
curl -X POST -d '{"k":"v"}' \
     -H "Content-Type: application/json" \
     https://api.exemple.com/data         # requête POST
curl -o page.html https://exemple.com     # sauver dans un fichier
curl -w "%{http_code}" -s -o /dev/null https://exemple.com  # juste le code
```

## 4. SSH (Secure Shell)

SSH permet de se connecter à distance de façon **sécurisée** (port 22). C'est l'outil n°1 du DevOps.

```bash
ssh utilisateur@serveur                  # connexion
ssh -p 2222 user@serveur                 # port personnalisé
ssh -i ~/.ssh/cle.pem user@serveur       # avec une clé
```

**Authentification par clé (recommandée)** :
```bash
ssh-keygen -t ed25519 -C "mon-email"     # générer une paire de clés
ssh-copy-id user@serveur                 # copier la clé publique
# puis connexion sans mot de passe
```

- Clé **privée** (`id_ed25519`) : reste secrète sur votre machine.
- Clé **publique** (`id_ed25519.pub`) : copiée sur le serveur.

**Copier des fichiers via SSH** :
```bash
scp fichier.txt user@serveur:/chemin/    # envoyer un fichier
scp user@serveur:/chemin/fichier.txt .   # récupérer
rsync -avz dossier/ user@serveur:/dest/  # synchronisation efficace
```

**Tunnel SSH** :
```bash
ssh -L 8080:localhost:80 user@serveur    # port local → distant
```

## 5. TLS/SSL et les certificats

**TLS** chiffre les communications (HTTPS, etc.). Repose sur un système de certificats.

- Un **certificat** prouve l'identité d'un serveur.
- Émis par une **autorité de certification (CA)**.
- **Let's Encrypt** fournit des certificats gratuits (via `certbot`).

```bash
# Vérifier un certificat
openssl s_client -connect exemple.com:443
echo | openssl s_client -connect exemple.com:443 2>/dev/null | openssl x509 -noout -dates
```

🎯 En DevOps : gérer le renouvellement automatique des certificats est crucial (un certificat expiré = site down).

## 6. FTP / SFTP

- **FTP** (port 21) : transfert de fichiers **non chiffré** (à éviter).
- **SFTP** : transfert sécurisé via SSH (recommandé).

```bash
sftp user@serveur
> put fichier.txt
> get fichier.txt
> ls
```

## 7. Les serveurs web & reverse proxy

**Nginx** et **Apache** servent des sites web et font office de reverse proxy.

Configuration Nginx minimale (`/etc/nginx/sites-available/monsite`) :
```nginx
server {
    listen 80;
    server_name exemple.com;

    location / {
        proxy_pass http://localhost:3000;   # vers l'app backend
        proxy_set_header Host $host;
    }
}
```

```bash
sudo nginx -t                    # tester la config
sudo systemctl reload nginx      # appliquer
```

## 8. Les API REST

La plupart des services modernes communiquent via des **API REST** (HTTP + JSON).

```bash
# GET
curl https://api.github.com/users/torvalds

# POST avec authentification
curl -X POST https://api.exemple.com/login \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"user":"admin"}'
```

💡 `jq` permet de parser le JSON :
```bash
curl -s https://api.github.com/users/torvalds | jq '.name'
```

## Exercices

1. Résolvez l'adresse IP de `github.com` avec `dig +short`.
2. Quels sont les serveurs mail (MX) de `gmail.com` ?
3. Récupérez uniquement le code HTTP retourné par un site avec `curl`.
4. Générez une paire de clés SSH ed25519.
5. À quoi correspond un code HTTP 502 ? Et 401 ?
6. Écrivez une commande curl qui fait un POST JSON vers une API.

> ✅ Passez au [Module 09 — Outils de diagnostic](09-reseau-outils-diagnostic.md).
