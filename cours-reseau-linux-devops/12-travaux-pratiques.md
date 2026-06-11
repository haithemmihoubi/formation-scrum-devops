# Module 12 — Travaux Pratiques & Exercices corrigés

🎯 **Objectif** : consolider par la pratique. Essayez **avant** de regarder les corrigés.

## TP 1 — Exploration du système

**Énoncé** : Collectez les informations système d'une machine Linux.

<details>
<summary>Corrigé</summary>

```bash
uname -a                    # noyau et architecture
cat /etc/os-release         # distribution
nproc                       # nombre de CPU
free -h                     # mémoire
df -h                       # disques
ip a                        # réseau
uptime                      # charge et durée de fonctionnement
who                         # utilisateurs connectés
```
</details>

## TP 2 — Manipulation de fichiers et texte

**Énoncé** : À partir d'un fichier `access.log`, comptez le nombre de requêtes avec un code 404 et affichez les 5 IP les plus fréquentes.

<details>
<summary>Corrigé</summary>

```bash
# Nombre de 404
grep " 404 " access.log | wc -l

# Top 5 des IP (1er champ)
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
```
</details>

## TP 3 — Utilisateurs et permissions

**Énoncé** : Créez un user `webadmin`, un groupe `web`, un dossier `/srv/site` appartenant à `webadmin:web` avec permissions `750`.

<details>
<summary>Corrigé</summary>

```bash
sudo groupadd web
sudo useradd -m -s /bin/bash -G web webadmin
sudo mkdir -p /srv/site
sudo chown -R webadmin:web /srv/site
sudo chmod 750 /srv/site
ls -ld /srv/site            # vérification
```
</details>

## TP 4 — Script de monitoring

**Énoncé** : Écrivez un script qui affiche une alerte si l'utilisation disque de `/` dépasse 80 %.

<details>
<summary>Corrigé</summary>

```bash
#!/bin/bash
set -euo pipefail

SEUIL=80
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

if [ "$USAGE" -ge "$SEUIL" ]; then
    echo "[ALERTE] Disque / à ${USAGE}% (seuil ${SEUIL}%)" >&2
    exit 1
else
    echo "[OK] Disque / à ${USAGE}%"
fi
```
</details>

## TP 5 — Service systemd

**Énoncé** : Créez un service systemd qui lance un script `/opt/hello/run.sh` au démarrage et le redémarre s'il plante.

<details>
<summary>Corrigé</summary>

```bash
# 1. Le script
sudo mkdir -p /opt/hello
echo -e '#!/bin/bash\nwhile true; do echo "vivant $(date)"; sleep 10; done' \
  | sudo tee /opt/hello/run.sh
sudo chmod +x /opt/hello/run.sh

# 2. Le service : /etc/systemd/system/hello.service
```
```ini
[Unit]
Description=Service Hello
After=network.target

[Service]
ExecStart=/opt/hello/run.sh
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
# 3. Activer
sudo systemctl daemon-reload
sudo systemctl enable --now hello
sudo systemctl status hello
journalctl -u hello -f
```
</details>

## TP 6 — Subnetting

**Énoncé** : On vous donne `172.16.0.0/16`. Découpez-le pour obtenir au moins 8 sous-réseaux. Donnez le nouveau masque et les 3 premiers sous-réseaux.

<details>
<summary>Corrigé</summary>

- 8 sous-réseaux = 2³ → emprunter 3 bits → `/16 + 3 = /19`
- Masque `/19` = `255.255.224.0`
- Incrément du 3e octet : 256 − 224 = **32**

| Sous-réseau | Plage |
|-------------|-------|
| 172.16.0.0/19 | 172.16.0.1 – 172.16.31.254 |
| 172.16.32.0/19 | 172.16.32.1 – 172.16.63.254 |
| 172.16.64.0/19 | 172.16.64.1 – 172.16.95.254 |

Chaque sous-réseau : 2^(32-19) − 2 = **8190 hôtes**.
</details>

## TP 7 — Diagnostic réseau

**Énoncé** : Un site `monapp.local` ne répond pas. Décrivez et exécutez la démarche de diagnostic complète.

<details>
<summary>Corrigé</summary>

```bash
# 1. Résolution DNS
dig +short monapp.local
nslookup monapp.local
cat /etc/hosts                       # résolution locale ?

# 2. Connectivité réseau
ping -c 3 monapp.local
ping -c 3 <IP>                       # contourner le DNS

# 3. Port ouvert ?
nc -zv monapp.local 443
ss -tulpn | grep 443                 # côté serveur

# 4. Application répond ?
curl -Iv https://monapp.local

# 5. Logs côté serveur
sudo journalctl -u nginx -n 50
sudo tail -f /var/log/nginx/error.log
```
Conclusion type : si DNS échoue → corriger `/etc/hosts` ou le DNS ; si port fermé → pare-feu ou service arrêté ; si 502 → backend down.
</details>

## TP 8 — Pare-feu

**Énoncé** : Sécurisez un serveur web avec UFW : seuls SSH (depuis votre réseau local uniquement), HTTP et HTTPS doivent être accessibles.

<details>
<summary>Corrigé</summary>

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```
</details>

## TP 9 — Déploiement Docker complet

**Énoncé** : Déployez une app web + Redis via docker-compose, exposée sur le port 8080.

<details>
<summary>Corrigé</summary>

`docker-compose.yml` :
```yaml
version: "3.8"
services:
  app:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - cache
  cache:
    image: redis:alpine
```
```bash
docker compose up -d
curl -I http://localhost:8080      # vérifier
docker compose ps
docker compose logs -f
```
</details>

## TP 10 — Automatisation par cron

**Énoncé** : Planifiez une sauvegarde quotidienne d'un dossier à 2h du matin, avec rotation (garder 7 jours).

<details>
<summary>Corrigé</summary>

Script `/opt/scripts/backup.sh` :
```bash
#!/bin/bash
set -euo pipefail
SRC="/srv/site"
DEST="/backups"
mkdir -p "$DEST"
tar -czf "$DEST/site_$(date +%F).tar.gz" "$SRC"
find "$DEST" -name "site_*.tar.gz" -mtime +7 -delete
```
```bash
chmod +x /opt/scripts/backup.sh
crontab -e
# ajouter :
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```
</details>

---

## Évaluation finale (auto-test)

Cochez ce que vous savez faire sans aide :

- [ ] Naviguer et manipuler des fichiers en ligne de commande
- [ ] Gérer utilisateurs, groupes et permissions
- [ ] Gérer des services avec systemd et lire les logs
- [ ] Installer des paquets et gérer le stockage
- [ ] Écrire un script bash robuste avec conditions et boucles
- [ ] Expliquer les modèles OSI / TCP/IP
- [ ] Calculer un sous-réseau (subnetting) en CIDR
- [ ] Utiliser DNS, HTTP, SSH, curl
- [ ] Diagnostiquer un problème réseau couche par couche
- [ ] Configurer un pare-feu et sécuriser SSH
- [ ] Déployer une app conteneurisée avec reverse proxy

## Pour aller plus loin

- **Certifications** : LPIC-1, RHCSA, CompTIA Linux+, CKA (Kubernetes).
- **Pratique** : montez un homelab (VirtualBox/Proxmox), KillerCoda, Katacoda-like.
- **Lectures** : « The Linux Command Line » (W. Shotts), documentation Docker/Kubernetes.
- **Suite logique** : Git avancé, Kubernetes, Terraform, Ansible, observabilité.

🎉 **Félicitations !** Vous avez les fondations Linux & Réseau d'un DevOps.

> 🔙 Retour au [sommaire](README.md).
