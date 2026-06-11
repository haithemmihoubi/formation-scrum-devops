# Module 02 — Linux : Utilisateurs, Groupes & Permissions

🎯 **Objectif** : maîtriser la sécurité d'accès aux fichiers, essentielle en production.

## 1. Le modèle multi-utilisateurs

Linux est nativement multi-utilisateurs. Chaque utilisateur a :
- un **UID** (User ID) unique
- un ou plusieurs **groupes** (GID)
- un dossier personnel (`/home/utilisateur`)
- un shell par défaut

Le super-utilisateur **root** (UID 0) a tous les droits.

```bash
id                  # affiche UID, GID et groupes de l'utilisateur courant
whoami              # nom de l'utilisateur
who                 # qui est connecté
cat /etc/passwd     # liste des utilisateurs
cat /etc/group      # liste des groupes
cat /etc/shadow     # mots de passe (chiffrés, root only)
```

Format d'une ligne `/etc/passwd` :
```
haithem:x:1000:1000:Haithem:/home/haithem:/bin/bash
   |     |  |    |     |          |            |
  nom   pwd UID GID  commentaire home       shell
```

## 2. Gérer les utilisateurs

```bash
sudo useradd -m -s /bin/bash alice   # créer un user avec home et bash
sudo passwd alice                    # définir son mot de passe
sudo usermod -aG docker alice        # ajouter alice au groupe docker
sudo userdel -r alice                # supprimer alice et son home
sudo adduser bob                     # alternative interactive (Debian/Ubuntu)
```

💡 `-aG` = **append** au **G**roupe. Oublier le `-a` retire les autres groupes !

## 3. Gérer les groupes

```bash
sudo groupadd developpeurs           # créer un groupe
sudo gpasswd -a alice developpeurs   # ajouter alice au groupe
groups alice                         # voir les groupes d'alice
sudo groupdel developpeurs           # supprimer le groupe
```

## 4. sudo et l'élévation de privilèges

`sudo` permet d'exécuter une commande en tant que root (ou autre user).

```bash
sudo apt update            # exécute en root
sudo -i                    # ouvre un shell root
sudo -u alice commande     # exécute en tant qu'alice
visudo                     # éditer les droits sudo en sécurité
```

⚠️ **Bonne pratique DevOps** : on ne se connecte JAMAIS directement en root sur un serveur. On utilise un compte normal + `sudo`. Cela permet la traçabilité (qui a fait quoi).

## 5. Comprendre les permissions

```bash
ls -l fichier.txt
# -rw-r--r-- 1 haithem developpeurs 1024 juin 5 10:00 fichier.txt
```

Décortiquons `-rw-r--r--` :

```
 -    rw-      r--      r--
type proprio  groupe   autres
```

- **1er caractère** : type (`-` fichier, `d` dossier, `l` lien)
- **3 blocs de 3** : droits du **propriétaire**, du **groupe**, des **autres**
- `r` = read (lecture, valeur 4)
- `w` = write (écriture, valeur 2)
- `x` = execute (exécution, valeur 1)

## 6. Notation octale (numérique)

Chaque bloc = somme des valeurs :

| Droits | Calcul | Octal |
|--------|--------|-------|
| `rwx` | 4+2+1 | 7 |
| `rw-` | 4+2 | 6 |
| `r-x` | 4+1 | 5 |
| `r--` | 4 | 4 |
| `---` | 0 | 0 |

Exemples courants :
- `755` = `rwxr-xr-x` (scripts, dossiers)
- `644` = `rw-r--r--` (fichiers de config)
- `600` = `rw-------` (clés privées, secrets)
- `777` = `rwxrwxrwx` ⚠️ à éviter (tout le monde peut tout faire)

## 7. Modifier les permissions

```bash
chmod 755 script.sh          # notation octale
chmod +x script.sh           # rendre exécutable
chmod -x script.sh           # retirer l'exécution
chmod u+w fichier            # ajouter écriture au propriétaire (user)
chmod g-r fichier            # retirer lecture au groupe
chmod o=r fichier            # autres = lecture seule
chmod -R 755 dossier/        # récursif sur tout un dossier
```

Notation symbolique : `u`=user, `g`=group, `o`=others, `a`=all ; `+`/`-`/`=`.

## 8. Changer le propriétaire

```bash
sudo chown alice fichier.txt          # change le propriétaire
sudo chown alice:devs fichier.txt     # propriétaire ET groupe
sudo chown -R alice:devs /app         # récursif
sudo chgrp devs fichier.txt           # change uniquement le groupe
```

## 9. Cas pratiques DevOps

```bash
# Sécuriser une clé SSH privée
chmod 600 ~/.ssh/id_rsa

# Rendre un script de déploiement exécutable
chmod +x deploy.sh

# Donner à l'app web les droits sur son dossier
sudo chown -R www-data:www-data /var/www/monsite

# Permissions correctes pour un dossier web
sudo find /var/www -type d -exec chmod 755 {} \;
sudo find /var/www -type f -exec chmod 644 {} \;
```

## 10. Permissions spéciales (notions avancées)

- **SUID** (`s` sur user) : le programme s'exécute avec les droits du propriétaire.
- **SGID** (`s` sur group) : héritage du groupe.
- **Sticky bit** (`t`) : sur `/tmp`, seul le propriétaire peut supprimer ses fichiers.

```bash
chmod u+s programme    # SUID
chmod g+s dossier      # SGID
chmod +t /partage      # sticky bit
```

## Exercices

1. Créez un utilisateur `deploy` avec un home et le shell bash.
2. Créez un groupe `web` et ajoutez-y `deploy`.
3. Créez un fichier et donnez-lui les permissions `640` en octal. Vérifiez avec `ls -l`.
4. Quel est l'octal de `rwxr-x---` ?
5. Sécurisez un fichier `secret.key` pour que seul le propriétaire puisse le lire/écrire.
6. Changez le propriétaire d'un dossier `/app` vers `deploy:web` récursivement.

> ✅ Passez au [Module 03 — Processus & Services](03-linux-processus-services.md).
