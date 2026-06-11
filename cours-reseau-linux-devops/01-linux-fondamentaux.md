# Module 01 — Linux : Fondamentaux

🎯 **Objectif** : être à l'aise dans un terminal Linux, naviguer, manipuler fichiers et texte.

## 1. Architecture de Linux

```
+------------------------------------------+
|        Applications (bash, nginx...)     |
+------------------------------------------+
|        Shell (interface utilisateur)     |
+------------------------------------------+
|        Noyau (Kernel)                    |  <- gère CPU, mémoire, périphériques
+------------------------------------------+
|        Matériel (Hardware)               |
+------------------------------------------+
```

- **Noyau (kernel)** : cœur du système, gère les ressources.
- **Shell** : interpréteur de commandes (le plus courant : `bash`, aussi `zsh`, `sh`).
- **Distribution** : noyau + outils + gestionnaire de paquets (Ubuntu, Debian, CentOS...).

## 2. Le terminal et le shell

```bash
whoami          # affiche l'utilisateur courant
hostname        # nom de la machine
date            # date et heure
uname -a        # infos sur le noyau et l'OS
echo "Bonjour"  # affiche du texte
pwd             # répertoire courant (Print Working Directory)
```

💡 La structure d'une commande : `commande [options] [arguments]`
Exemple : `ls -l /home` → commande `ls`, option `-l`, argument `/home`.

## 3. Arborescence du système de fichiers (FHS)

Sous Linux, **tout est fichier** et tout part de la racine `/`.

| Dossier | Rôle |
|---------|------|
| `/` | Racine de tout le système |
| `/home` | Dossiers personnels des utilisateurs |
| `/root` | Dossier personnel de root |
| `/etc` | Fichiers de configuration |
| `/var` | Données variables (logs dans `/var/log`) |
| `/tmp` | Fichiers temporaires |
| `/usr` | Programmes et bibliothèques |
| `/bin`, `/sbin` | Commandes système essentielles |
| `/opt` | Logiciels tiers |
| `/dev` | Périphériques (disques, etc.) |
| `/proc`, `/sys` | Infos noyau en temps réel (virtuels) |
| `/mnt`, `/media` | Points de montage |

## 4. Navigation dans les fichiers

```bash
pwd                 # où suis-je ?
ls                  # lister le contenu
ls -l               # format long (droits, taille, date)
ls -la              # inclut les fichiers cachés (commençant par .)
ls -lh              # tailles lisibles (K, M, G)
cd /var/log         # aller dans un dossier (chemin absolu)
cd ..               # remonter d'un niveau
cd ~                # aller dans son home
cd -                # revenir au dossier précédent
tree                # affiche l'arborescence (à installer)
```

📌 **Chemin absolu** vs **relatif** :
- Absolu : commence par `/` → `/home/haithem/docs`
- Relatif : par rapport au dossier courant → `docs/notes.txt`, `../config`

## 5. Manipuler fichiers et dossiers

```bash
mkdir projet                 # créer un dossier
mkdir -p a/b/c               # créer une arborescence complète
touch fichier.txt            # créer un fichier vide
cp source.txt dest.txt       # copier un fichier
cp -r dossier1 dossier2      # copier un dossier (récursif)
mv ancien.txt nouveau.txt    # renommer ou déplacer
rm fichier.txt               # supprimer un fichier
rm -r dossier                # supprimer un dossier
rm -rf dossier               # forcer la suppression ⚠️ DANGEREUX
```

⚠️ `rm -rf /` peut détruire tout le système. Vérifiez toujours deux fois.

## 6. Lire et afficher le contenu

```bash
cat fichier.txt        # affiche tout le fichier
less fichier.txt       # lecture page par page (q pour quitter)
head -n 20 fichier     # 20 premières lignes
tail -n 20 fichier     # 20 dernières lignes
tail -f /var/log/syslog  # suit le fichier en temps réel (très utile DevOps !)
wc -l fichier          # compte le nombre de lignes
```

💡 `tail -f` est essentiel pour surveiller les logs d'une application en direct.

## 7. Rechercher des fichiers et du texte

```bash
find /etc -name "*.conf"          # trouver des fichiers par nom
find /var -type f -size +100M     # fichiers de plus de 100 Mo
find . -mtime -1                  # modifiés il y a moins d'1 jour

grep "erreur" fichier.log         # chercher un mot dans un fichier
grep -i "error" app.log           # insensible à la casse
grep -r "TODO" .                  # récursif dans tous les fichiers
grep -n "404" access.log          # affiche les numéros de ligne
grep -v "INFO" app.log            # inverse : lignes SANS "INFO"
```

## 8. Les redirections et les pipes

C'est **le superpouvoir** du shell : combiner des commandes.

```bash
echo "test" > fichier.txt     # écrit dans fichier (écrase)
echo "ligne 2" >> fichier.txt # ajoute à la fin (append)
commande 2> erreurs.log       # redirige les erreurs (stderr)
commande > sortie.log 2>&1    # redirige sortie + erreurs

# Le pipe | envoie la sortie d'une commande vers une autre
cat access.log | grep "404" | wc -l       # compte les erreurs 404
ps aux | grep nginx                        # filtre les processus nginx
ls -l /etc | sort | head                   # trie et prend le début
```

📊 **Flux standards** :
- `stdin` (0) : entrée
- `stdout` (1) : sortie normale
- `stderr` (2) : sortie d'erreur

## 9. Éditer des fichiers (nano & vim)

```bash
nano fichier.txt    # éditeur simple (Ctrl+O sauver, Ctrl+X quitter)
vim fichier.txt     # éditeur puissant
```

**Bases de Vim** (incontournable car présent partout) :
- `i` : mode insertion
- `Échap` : revenir en mode normal
- `:w` : sauvegarder
- `:q` : quitter
- `:wq` : sauvegarder et quitter
- `:q!` : quitter sans sauver
- `/mot` : rechercher

## 10. Aide et documentation

```bash
man ls          # manuel d'une commande
ls --help       # aide rapide
which python3   # où se trouve un exécutable
type cd         # type d'une commande
apropos network # chercher des commandes par mot-clé
```

## Exercices

1. Créez l'arborescence `~/devops/projet1/logs` en une seule commande.
2. Créez un fichier `notes.txt`, écrivez-y 3 lignes avec `echo` et `>>`.
3. Affichez uniquement les lignes contenant le mot « erreur » d'un fichier log.
4. Comptez combien de fichiers `.conf` existent dans `/etc` (et sous-dossiers).
5. Copiez `/etc/hostname` dans votre home, renommez-le `mon-host.txt`.
6. Utilisez un pipe pour afficher les 5 plus gros fichiers de `/var/log`.

> ✅ Passez au [Module 02 — Utilisateurs & Permissions](02-linux-utilisateurs-permissions.md).
