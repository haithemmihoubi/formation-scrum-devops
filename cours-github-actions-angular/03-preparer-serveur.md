# Préparer le serveur et les accès

Le runner GitHub doit pouvoir **se connecter au serveur** et y **lancer Docker**. Ce
module prépare le terrain côté serveur, puis enregistre les accès dans les **secrets**
GitHub.

## 1. Installer Docker sur le serveur

Sur un serveur Ubuntu/Debian fraîchement provisionné :

```bash
# Installation officielle de Docker
curl -fsSL https://get.docker.com | sh

# Démarrer Docker au boot
sudo systemctl enable --now docker

# Vérifier
docker --version
```

## 2. Créer un utilisateur de déploiement

On évite d'utiliser `root` pour le déploiement. On crée un utilisateur dédié, membre du
groupe `docker` (pour lancer des conteneurs sans `sudo`) :

```bash
sudo adduser --disabled-password deployer
sudo usermod -aG docker deployer
```

> **Sécurité :** un utilisateur dédié limite la casse si la clé fuite, et trace clairement
> « qui » déploie dans les logs du serveur.

## 3. Générer une paire de clés SSH dédiée

Le runner s'authentifiera par **clé SSH** (jamais par mot de passe). On génère une paire
**spécifique au déploiement** — pas votre clé personnelle.

```bash
# Sur votre poste (ou le serveur), SANS passphrase pour l'automatisation
ssh-keygen -t ed25519 -C "github-actions-deploy" -f deploy_key
# → produit deux fichiers :
#   deploy_key       (clé PRIVÉE  → ira dans les secrets GitHub)
#   deploy_key.pub   (clé PUBLIQUE → ira sur le serveur)
```

### Autoriser la clé publique sur le serveur

```bash
# Ajouter la clé PUBLIQUE aux clés autorisées de l'utilisateur deployer
ssh-copy-id -i deploy_key.pub deployer@VOTRE_SERVEUR
# (ou copier manuellement le contenu dans ~deployer/.ssh/authorized_keys)
```

Tester la connexion avec la clé **privée** :

```bash
ssh -i deploy_key deployer@VOTRE_SERVEUR "docker ps"
```

Si cette commande liste les conteneurs, le runner pourra faire de même.

## 4. Enregistrer les secrets dans GitHub

> **Règle absolue : aucune clé, aucun mot de passe, aucune IP sensible dans le code.**
> Tout passe par les **secrets chiffrés** de GitHub.

Dans le dépôt GitHub : **Settings ▸ Secrets and variables ▸ Actions ▸ New repository secret**.

| Secret | Contenu | Exemple |
|--------|---------|---------|
| `DEPLOY_HOST` | IP ou domaine du serveur | `203.0.113.10` |
| `DEPLOY_USER` | utilisateur SSH | `deployer` |
| `DEPLOY_SSH_KEY` | **contenu** du fichier `deploy_key` (clé privée) | `-----BEGIN OPENSSH...` |
| `DEPLOY_PORT` | port SSH (optionnel, défaut 22) | `22` |

Pour copier la clé privée intégralement dans le presse-papier :

```bash
cat deploy_key      # copier TOUT, y compris les lignes BEGIN/END
```

> **`GITHUB_TOKEN` : pas besoin de le créer.** GitHub injecte automatiquement ce secret
> dans chaque workflow. Il sert à s'authentifier sur le registry **GHCR** (voir module 06).

## 5. Checklist avant d'écrire le workflow

- [ ] Docker installé et actif sur le serveur (`docker ps` fonctionne).
- [ ] Utilisateur `deployer` créé et membre du groupe `docker`.
- [ ] Paire de clés `deploy_key` / `deploy_key.pub` générée.
- [ ] Clé publique ajoutée à `authorized_keys` sur le serveur.
- [ ] `ssh -i deploy_key deployer@serveur "docker ps"` réussit.
- [ ] Secrets `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY` enregistrés sur GitHub.

Tout est prêt : on peut maintenant écrire le pipeline complet.
