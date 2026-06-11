# Module 10 — Sécurité & Pare-feu

🎯 **Objectif** : sécuriser un serveur Linux et filtrer le trafic réseau.

## 1. Principes de sécurité (defense in depth)

- **Moindre privilège** : chaque user/service n'a que les droits strictement nécessaires.
- **Surface d'attaque minimale** : fermer tout ce qui n'est pas utilisé.
- **Défense en profondeur** : plusieurs couches (pare-feu + auth + chiffrement).
- **Mises à jour** : appliquer régulièrement les correctifs de sécurité.
- **Journalisation** : tout tracer pour détecter et investiguer.

## 2. Le pare-feu : concept

Un pare-feu filtre le trafic selon des règles : **autoriser** ou **bloquer** en fonction de l'IP source/destination, du port, du protocole.

Politique recommandée : **deny by default** (tout bloquer, puis autoriser uniquement le nécessaire).

## 3. UFW (Uncomplicated Firewall — Ubuntu/Debian)

Le plus simple pour débuter.

```bash
sudo ufw status                  # état
sudo ufw enable                  # activer
sudo ufw disable                 # désactiver

# Politique par défaut
sudo ufw default deny incoming   # bloquer tout en entrée
sudo ufw default allow outgoing  # autoriser tout en sortie

# Autoriser des services
sudo ufw allow 22/tcp            # SSH
sudo ufw allow 80/tcp            # HTTP
sudo ufw allow 443/tcp           # HTTPS
sudo ufw allow from 192.168.1.0/24  # depuis un réseau
sudo ufw allow from 1.2.3.4 to any port 22  # SSH depuis une IP précise

# Supprimer une règle
sudo ufw delete allow 80/tcp
sudo ufw status numbered         # voir avec numéros
```

⚠️ Avant d'activer UFW à distance, **autorisez SSH** sinon vous vous bloquez !

## 4. firewalld (RHEL / CentOS / Rocky)

```bash
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --remove-port=8080/tcp --permanent
```

`--permanent` rend la règle persistante après redémarrage.

## 5. iptables (bas niveau, universel)

iptables est le moteur sous-jacent. Plus complexe mais incontournable.

```bash
sudo iptables -L -n -v               # lister les règles
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # autoriser SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT   # autoriser HTTP
sudo iptables -A INPUT -i lo -j ACCEPT               # loopback
sudo iptables -P INPUT DROP                          # politique par défaut : bloquer
sudo iptables -D INPUT 1                             # supprimer la règle n°1
```

Concepts : **chaînes** (INPUT, OUTPUT, FORWARD), **cibles** (ACCEPT, DROP, REJECT).

💡 `nftables` est le successeur moderne d'iptables.

## 6. Sécuriser SSH (priorité absolue)

SSH est la porte d'entrée des serveurs → cible n°1 des attaques.

Fichier `/etc/ssh/sshd_config` :
```
PermitRootLogin no              # interdire la connexion root directe
PasswordAuthentication no       # forcer l'authentification par clé
PubkeyAuthentication yes
Port 2222                       # changer le port (réduit le bruit)
AllowUsers deploy               # limiter aux users autorisés
MaxAuthTries 3                  # limiter les tentatives
```

```bash
sudo systemctl restart sshd     # appliquer
```

**Bonnes pratiques SSH** :
- Toujours utiliser des **clés** (jamais de mot de passe).
- Désactiver le login root.
- Installer **fail2ban** pour bannir les IP qui brute-forcent.

```bash
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

## 7. Gestion des secrets

⚠️ **Ne jamais** mettre de mots de passe / clés API en clair dans le code ou Git.

Bonnes pratiques :
- Variables d'environnement (`.env` non commité, dans `.gitignore`).
- Gestionnaires de secrets : **HashiCorp Vault**, **AWS Secrets Manager**, **Sealed Secrets** (Kubernetes).
- Permissions strictes sur les fichiers de secrets (`chmod 600`).

```bash
# Vérifier qu'aucun secret n'est commité
git log -p | grep -i "password"
```

## 8. Mises à jour de sécurité

```bash
sudo apt update && sudo apt upgrade -y          # Debian/Ubuntu
sudo unattended-upgrades                         # mises à jour auto
sudo dnf update --security                       # RHEL : sécurité seule
```

## 9. Durcissement de base d'un serveur (checklist)

- [ ] Mettre à jour le système
- [ ] Créer un user non-root avec sudo
- [ ] Désactiver le login root SSH
- [ ] Authentification SSH par clé uniquement
- [ ] Activer le pare-feu (deny par défaut)
- [ ] Installer fail2ban
- [ ] Fermer les ports/services inutiles
- [ ] Activer les mises à jour automatiques de sécurité
- [ ] Configurer la journalisation
- [ ] Sauvegardes régulières testées

## 10. Surveiller la sécurité

```bash
last                       # dernières connexions
lastb                      # tentatives échouées
who                        # connectés actuellement
sudo grep "Failed password" /var/log/auth.log   # échecs SSH
sudo ss -tulpn             # ports ouverts (réduire la surface)
sudo journalctl -u sshd | grep -i fail
```

## Exercices

1. Configurez UFW : bloquer tout en entrée, autoriser SSH, HTTP et HTTPS.
2. Listez vos règles UFW avec leurs numéros.
3. Dans `sshd_config`, quelles 2 options désactiveriez-vous en priorité ?
4. Installez fail2ban et vérifiez le statut de la jail SSH.
5. Trouvez les tentatives de connexion SSH échouées dans les logs.
6. Listez tous les ports ouverts et identifiez ceux que vous pourriez fermer.

> ✅ Passez au [Module 11 — Mise en pratique DevOps](11-pratique-devops.md).
