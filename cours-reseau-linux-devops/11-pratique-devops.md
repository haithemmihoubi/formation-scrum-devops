# Module 11 — Mise en pratique DevOps

🎯 **Objectif** : relier Linux + Réseau dans des cas concrets d'infrastructure DevOps.

## 1. Docker : Linux + réseau en action

Docker isole des applications dans des **conteneurs** (basés sur les namespaces et cgroups du noyau Linux).

```bash
# Installation rapide (Ubuntu)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # éviter sudo (reconnexion requise)

# Commandes de base
docker ps                       # conteneurs en cours
docker ps -a                    # tous les conteneurs
docker images                   # images locales
docker run -d -p 8080:80 nginx  # lancer nginx, port 8080 → 80
docker logs <id>                # voir les logs
docker exec -it <id> bash       # entrer dans un conteneur
docker stop <id> / docker rm <id>
docker build -t monapp .        # construire une image
```

**Le réseau dans Docker** :
```bash
docker network ls                       # réseaux Docker
docker network create mon-reseau        # créer un réseau
docker run --network mon-reseau ...      # connecter un conteneur
```

🎯 `-p 8080:80` = **port mapping** : relie le port 8080 de l'hôte au port 80 du conteneur. C'est ici que vos connaissances réseau (ports, NAT) servent directement.

## 2. Dockerfile : automatiser une image

```dockerfile
FROM node:20-alpine          # image de base légère (Alpine Linux)
WORKDIR /app                 # dossier de travail
COPY package*.json ./        # copier les dépendances
RUN npm install              # installer
COPY . .                     # copier le code
EXPOSE 3000                  # documenter le port
CMD ["node", "server.js"]    # commande de démarrage
```

```bash
docker build -t monapp:1.0 .
docker run -d -p 3000:3000 monapp:1.0
```

## 3. docker-compose : orchestrer plusieurs services

`docker-compose.yml` — exemple app web + base de données :
```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-net

volumes:
  db-data:

networks:
  app-net:
```

```bash
docker compose up -d        # démarrer
docker compose logs -f      # suivre les logs
docker compose down         # arrêter et nettoyer
```

💡 Notez : `web` joint `db` par son **nom de service** (DNS interne Docker) → vos connaissances DNS s'appliquent.

## 4. Reverse proxy Nginx devant des conteneurs

Scénario réel : Nginx reçoit le trafic public (443) et le redirige vers les conteneurs internes.

```nginx
server {
    listen 443 ssl;
    server_name app.exemple.com;

    ssl_certificate     /etc/letsencrypt/live/app.exemple.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.exemple.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:4000;
    }
}
```

Architecture :
```
Internet → :443 Nginx (reverse proxy) → :3000 frontend
                                       → :4000 backend
                                       → :5432 base de données (privé)
```

## 5. Certificat HTTPS gratuit avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d app.exemple.com
# Renouvellement automatique testé via :
sudo certbot renew --dry-run
```

## 6. CI/CD : enchaîner Linux + réseau + scripts

Un pipeline CI/CD automatise build → test → déploiement. Exemple `.gitlab-ci.yml` :

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t monapp:$CI_COMMIT_SHORT_SHA .

test:
  stage: test
  script:
    - npm install
    - npm test

deploy:
  stage: deploy
  script:
    - ssh deploy@serveur "docker pull monapp && docker compose up -d"
  only:
    - main
```

🎯 Le déploiement utilise **SSH** + **scripts bash** + **Docker** : tout ce que vous avez appris !

## 7. Infrastructure as Code (notion)

Au lieu de configurer les serveurs à la main, on les décrit dans du code.

**Ansible** (configuration) — exemple playbook :
```yaml
- hosts: serveurs_web
  become: yes
  tasks:
    - name: Installer nginx
      apt:
        name: nginx
        state: present
    - name: Démarrer nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

```bash
ansible-playbook -i inventaire deploy.yml
```

**Terraform** (provisionnement cloud) crée des VM, réseaux, VPC... avec des fichiers `.tf`.

## 8. Monitoring (notion)

Surveiller pour réagir avant la panne :
- **Prometheus** : collecte des métriques (CPU, RAM, requêtes).
- **Grafana** : tableaux de bord visuels.
- **ELK / Loki** : centralisation des logs.
- **Alertmanager** : alertes (Slack, email).

Métriques système rapides (les bases) :
```bash
uptime; free -h; df -h; ss -s
```

## 9. Projet fil rouge

**Objectif** : déployer une application web complète, sécurisée et monitorée.

Étapes :
1. Provisionner un serveur Linux (VM ou cloud).
2. Durcir la sécurité (user sudo, SSH par clé, UFW, fail2ban).
3. Installer Docker et docker-compose.
4. Déployer une app + base de données via docker-compose.
5. Mettre un reverse proxy Nginx + HTTPS Let's Encrypt.
6. Écrire un script bash de sauvegarde planifié par cron.
7. Configurer le pare-feu (seuls 22, 80, 443 ouverts).
8. Diagnostiquer la chaîne avec `curl`, `ss`, `dig`, `journalctl`.

## Exercices

1. Lancez un conteneur nginx accessible sur le port 8080 de votre machine.
2. Écrivez un Dockerfile pour une petite app et construisez l'image.
3. Créez un `docker-compose.yml` avec une app et une base PostgreSQL.
4. Configurez un reverse proxy Nginx vers un conteneur.
5. Écrivez un script de déploiement qui pull une image et redémarre via compose.
6. Listez les ports ouverts par vos conteneurs avec `ss` ou `docker ps`.

> ✅ Passez au [Module 12 — Travaux pratiques](12-travaux-pratiques.md).
