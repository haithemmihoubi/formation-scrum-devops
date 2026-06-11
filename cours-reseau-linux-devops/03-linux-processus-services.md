# Module 03 — Linux : Processus, Services & Tâches planifiées

🎯 **Objectif** : surveiller et contrôler ce qui tourne sur un serveur, gérer les services et automatiser des tâches.

## 1. Qu'est-ce qu'un processus ?

Un **processus** est un programme en cours d'exécution. Chacun a :
- un **PID** (Process ID) unique
- un **PPID** (PID du parent)
- un propriétaire
- un état (running, sleeping, zombie...)

## 2. Lister les processus

```bash
ps aux                  # tous les processus du système
ps aux | grep nginx     # filtrer un processus précis
ps -ef                  # format alternatif
pstree                  # arborescence des processus
top                     # moniteur temps réel (q pour quitter)
htop                    # version améliorée et colorée (à installer)
```

Colonnes de `ps aux` : USER, PID, %CPU, %MEM, VSZ, RSS, STAT, START, TIME, COMMAND.

## 3. Surveiller les ressources

```bash
top              # CPU, mémoire, processus en direct
htop             # interactif (F9 pour tuer, F6 pour trier)
free -h          # mémoire RAM et swap (format lisible)
uptime           # charge système (load average)
vmstat 1         # statistiques système chaque seconde
df -h            # espace disque par partition
du -sh /var/*    # taille des dossiers
iostat           # statistiques d'E/S disque
```

📊 **Load average** : 3 chiffres = charge moyenne sur 1, 5 et 15 min. Sur une machine 4 cœurs, une charge > 4 indique une saturation.

## 4. Tuer / signaler un processus

```bash
kill 1234            # envoie SIGTERM (arrêt propre) au PID 1234
kill -9 1234         # SIGKILL (arrêt forcé, dernier recours)
kill -15 1234        # SIGTERM explicite
killall nginx        # tue tous les processus nommés nginx
pkill -f "python app"# tue par motif de ligne de commande
```

Signaux courants :
- `SIGTERM` (15) : demande polie d'arrêt
- `SIGKILL` (9) : tue immédiatement (ne peut être ignoré)
- `SIGHUP` (1) : souvent utilisé pour recharger la config

## 5. Jobs et arrière-plan

```bash
commande &           # lance en arrière-plan
Ctrl + Z             # suspend le processus courant
bg                   # reprend en arrière-plan
fg                   # ramène au premier plan
jobs                 # liste les jobs
nohup commande &     # continue après déconnexion
```

💡 En production, on préfère gérer les services longue durée via **systemd** plutôt que `nohup`.

## 6. systemd : le gestionnaire de services moderne

`systemd` est le système d'init de la plupart des distributions modernes. Il gère le démarrage et les **services** (appelés *units*).

```bash
sudo systemctl status nginx     # état d'un service
sudo systemctl start nginx      # démarrer
sudo systemctl stop nginx       # arrêter
sudo systemctl restart nginx    # redémarrer
sudo systemctl reload nginx     # recharger la config sans couper
sudo systemctl enable nginx     # démarrage auto au boot
sudo systemctl disable nginx    # désactiver le démarrage auto
sudo systemctl is-active nginx  # actif ou non
systemctl list-units --type=service  # lister les services
```

## 7. Créer son propre service systemd (très utile DevOps)

Fichier `/etc/systemd/system/monapp.service` :

```ini
[Unit]
Description=Mon application Node.js
After=network.target

[Service]
User=deploy
WorkingDirectory=/opt/monapp
ExecStart=/usr/bin/node server.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Puis :
```bash
sudo systemctl daemon-reload     # recharge la config systemd
sudo systemctl enable --now monapp
sudo systemctl status monapp
```

## 8. Consulter les journaux (logs) avec journalctl

```bash
journalctl                       # tous les logs
journalctl -u nginx              # logs d'un service précis
journalctl -u nginx -f           # suivre en temps réel
journalctl --since "1 hour ago"  # depuis 1 heure
journalctl --since today         # aujourd'hui
journalctl -p err                # uniquement les erreurs
journalctl -n 50                 # les 50 dernières lignes
```

Logs classiques aussi dans `/var/log/` :
```bash
tail -f /var/log/syslog          # journal système (Debian/Ubuntu)
tail -f /var/log/auth.log        # authentifications
tail -f /var/log/nginx/error.log # erreurs nginx
```

## 9. Planifier des tâches : cron

`cron` exécute des commandes à intervalles réguliers.

```bash
crontab -e        # éditer ses tâches planifiées
crontab -l        # lister ses tâches
```

Format d'une ligne cron :
```
* * * * * commande
| | | | |
| | | | +-- jour de la semaine (0-7, 0 et 7 = dimanche)
| | | +---- mois (1-12)
| | +------ jour du mois (1-31)
| +-------- heure (0-23)
+---------- minute (0-59)
```

Exemples :
```bash
0 2 * * *      /opt/scripts/backup.sh       # tous les jours à 2h
*/5 * * * *    /opt/scripts/check.sh         # toutes les 5 minutes
0 0 * * 0      /opt/scripts/weekly.sh        # chaque dimanche à minuit
30 8 1 * *     /opt/scripts/monthly.sh       # le 1er du mois à 8h30
```

💡 Alternative moderne : les **timers systemd** (plus robustes, journalisés).

## 10. Variables d'environnement

```bash
echo $PATH               # affiche le PATH
export API_KEY="secret"  # définir une variable d'environnement
env                      # lister toutes les variables
printenv HOME            # afficher une variable
```

Pour les rendre persistantes : `~/.bashrc`, `~/.profile` ou `/etc/environment`.

## Exercices

1. Trouvez le PID du processus consommant le plus de CPU.
2. Lancez `sleep 300 &` puis ramenez-le au premier plan, puis tuez-le.
3. Affichez l'état du service SSH (`ssh` ou `sshd`).
4. Écrivez un service systemd qui lance un script `/opt/hello.sh`.
5. Programmez une tâche cron qui exécute un script chaque jour à 23h.
6. Affichez en temps réel les logs du service SSH avec `journalctl`.

> ✅ Passez au [Module 04 — Paquets & Stockage](04-linux-paquets-stockage.md).
