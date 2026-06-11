# Module 05 — Bash Scripting

🎯 **Objectif** : automatiser des tâches répétitives, base de l'automatisation DevOps.

## 1. Premier script

Un script bash est un fichier texte de commandes.

```bash
#!/bin/bash
# mon premier script
echo "Bonjour DevOps !"
```

- La première ligne `#!/bin/bash` s'appelle le **shebang** : elle indique l'interpréteur.
- Rendez le script exécutable et lancez-le :

```bash
chmod +x script.sh
./script.sh
# ou
bash script.sh
```

## 2. Variables

```bash
#!/bin/bash
nom="Haithem"
age=25
echo "Je m'appelle $nom et j'ai $age ans"
echo "Avec accolades : ${nom}_devops"
```

⚠️ **Pas d'espace** autour du `=` : `nom="x"` ✅, `nom = "x"` ❌.

Variables spéciales :
```bash
$0    # nom du script
$1    # premier argument
$2    # deuxième argument
$@    # tous les arguments
$#    # nombre d'arguments
$?    # code de retour de la dernière commande (0 = succès)
$$    # PID du script
```

## 3. Lire une entrée utilisateur

```bash
#!/bin/bash
read -p "Quel est votre nom ? " nom
echo "Bonjour $nom"
read -sp "Mot de passe : " mdp   # -s = caché
echo
```

## 4. Substitution de commande

```bash
date_du_jour=$(date +%Y-%m-%d)
echo "Nous sommes le $date_du_jour"
nb_fichiers=$(ls | wc -l)
echo "Il y a $nb_fichiers fichiers"
```

## 5. Conditions

```bash
#!/bin/bash
age=20
if [ $age -ge 18 ]; then
    echo "Majeur"
elif [ $age -ge 13 ]; then
    echo "Adolescent"
else
    echo "Enfant"
fi
```

**Opérateurs de comparaison numériques** :
- `-eq` égal, `-ne` différent
- `-gt` >, `-ge` >=, `-lt` <, `-le` <=

**Comparaison de chaînes** :
- `=` égal, `!=` différent, `-z` vide, `-n` non vide

**Tests de fichiers** :
- `-f` fichier existe, `-d` dossier existe
- `-e` existe, `-r` lisible, `-w` inscriptible, `-x` exécutable

```bash
if [ -f /etc/passwd ]; then
    echo "Le fichier existe"
fi

if [ -d /var/log ] && [ -w /var/log ]; then
    echo "Dossier accessible en écriture"
fi
```

💡 `[[ ]]` (double crochet) est plus puissant et recommandé en bash.

## 6. Boucles

**Boucle for** :
```bash
for i in 1 2 3 4 5; do
    echo "Itération $i"
done

for fichier in *.log; do
    echo "Traitement de $fichier"
done

for i in {1..10}; do
    echo "Nombre $i"
done
```

**Boucle while** :
```bash
compteur=1
while [ $compteur -le 5 ]; do
    echo "Compteur : $compteur"
    compteur=$((compteur + 1))
done
```

**Lire un fichier ligne par ligne** :
```bash
while read ligne; do
    echo "Ligne : $ligne"
done < fichier.txt
```

## 7. Fonctions

```bash
#!/bin/bash
saluer() {
    echo "Bonjour $1, bienvenue !"
}

verifier_service() {
    if systemctl is-active --quiet $1; then
        echo "$1 est actif"
        return 0
    else
        echo "$1 est arrêté"
        return 1
    fi
}

saluer "Haithem"
verifier_service "nginx"
```

## 8. Opérations arithmétiques

```bash
a=10
b=3
echo $((a + b))    # 13
echo $((a - b))    # 7
echo $((a * b))    # 30
echo $((a / b))    # 3 (division entière)
echo $((a % b))    # 1 (modulo)
```

## 9. Gestion des erreurs (robustesse)

```bash
#!/bin/bash
set -e      # arrête le script à la première erreur
set -u      # erreur si variable non définie
set -o pipefail  # détecte les erreurs dans les pipes
set -euo pipefail   # combinaison recommandée en production

# Vérifier le code de retour
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé !" >&2
    exit 1
fi
```

## 10. Script complet : exemple DevOps réel

```bash
#!/bin/bash
set -euo pipefail

# Script de sauvegarde simple
SOURCE="/var/www/monsite"
DEST="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="$DEST/backup_$DATE.tar.gz"

echo "[INFO] Démarrage de la sauvegarde..."

# Créer le dossier de destination s'il n'existe pas
mkdir -p "$DEST"

# Créer l'archive compressée
if tar -czf "$ARCHIVE" "$SOURCE"; then
    echo "[OK] Sauvegarde créée : $ARCHIVE"
else
    echo "[ERREUR] Échec de la sauvegarde" >&2
    exit 1
fi

# Supprimer les sauvegardes de plus de 7 jours
find "$DEST" -name "backup_*.tar.gz" -mtime +7 -delete
echo "[INFO] Anciennes sauvegardes nettoyées."

# Taille de la sauvegarde
taille=$(du -h "$ARCHIVE" | cut -f1)
echo "[INFO] Taille : $taille"
```

## 11. Bonnes pratiques

- Toujours mettre le **shebang** `#!/bin/bash`.
- Utiliser `set -euo pipefail` pour la robustesse.
- Mettre les variables entre **guillemets** : `"$var"`.
- Vérifier les arguments en entrée.
- Écrire les erreurs sur `stderr` avec `>&2`.
- Utiliser `shellcheck` pour valider vos scripts :
```bash
sudo apt install shellcheck
shellcheck script.sh
```

## Exercices

1. Écrivez un script qui prend un nom en argument et affiche « Bonjour <nom> ».
2. Écrivez un script qui vérifie si un fichier passé en argument existe.
3. Faites une boucle qui affiche les nombres pairs de 1 à 20.
4. Écrivez une fonction qui teste si un service systemd est actif.
5. Écrivez un script qui compte le nombre d'erreurs « 404 » dans un fichier log.
6. Améliorez le script de sauvegarde pour qu'il envoie un message si l'espace disque est insuffisant.

> ✅ Passez au [Module 06 — Réseau Fondamentaux](06-reseau-fondamentaux.md).
