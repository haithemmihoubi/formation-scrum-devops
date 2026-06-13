# Aller plus loin, dépanner & checklist

Le pipeline fonctionne. Voici les techniques pour l'optimiser, les pannes courantes et
une checklist finale.

## 1. Accélérer le pipeline : le cache

Réinstaller `node_modules` et rebuilder l'image à chaque run est lent. Deux caches
combinés divisent le temps par deux ou trois.

```yaml
# Cache des dépendances npm
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'

# Cache des couches Docker (réutilisé entre les runs)
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 2. Tester plusieurs versions : les matrices

Une **matrice** rejoue le même job sur plusieurs configurations, **en parallèle** :

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node-version }}
  - run: npm ci && npm test
```

GitHub lance ici **trois jobs simultanés**, un par version de Node.

## 3. Ne pas bloquer sur les étapes non critiques

```yaml
- name: Lint
  run: npx ng lint
  continue-on-error: true     # un warning de lint ne bloque pas le déploiement
```

`continue-on-error: true` laisse le job continuer même si la step échoue — à réserver aux
étapes **informatives**, jamais aux tests qui garantissent la qualité.

## 4. Les expressions et contextes utiles

| Expression | Donne |
|-----------|-------|
| `${{ github.sha }}` | hash du commit |
| `${{ github.ref }}` | référence (`refs/heads/main`) |
| `${{ github.actor }}` | auteur du déclenchement |
| `${{ github.repository }}` | `organisation/depot` |
| `${{ github.event_name }}` | `push`, `pull_request`… |
| `${{ secrets.X }}` / `${{ vars.X }}` | secret / variable |

Conditions fréquentes :

```yaml
if: github.ref == 'refs/heads/main'                    # seulement sur main
if: github.event_name == 'push'                        # seulement sur push, pas PR
if: success() && github.ref == 'refs/heads/main'       # combiné
```

## 5. Notifier l'équipe

On ajoute une notification finale (Slack, Discord, e-mail) conditionnée au résultat :

```yaml
- name: Notifier en cas d'échec
  if: failure()
  run: echo "Le déploiement a échoué sur ${{ github.sha }}"
  # ... ou une action Slack/Discord du Marketplace
```

`failure()`, `success()`, `always()` permettent de réagir selon l'issue du job.

## 6. Dépannage : les erreurs les plus fréquentes

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| `npm ci` échoue | pas de `package-lock.json` | committer le lockfile |
| Mauvais dossier copié | chemin `dist/` erroné | Angular 17+ → `dist/<app>/browser` |
| 404 en rafraîchissant une route | config SPA Nginx absente | `try_files ... /index.html` |
| `permission denied (publickey)` | clé SSH invalide ou non autorisée | recopier `deploy_key`, vérifier `authorized_keys` |
| `denied: permission_denied` au push GHCR | permissions du token | ajouter `packages: write` |
| `docker: command not found` (serveur) | Docker non installé | installer Docker, ajouter l'user au groupe `docker` |
| Le job `deploy` ne se lance pas | condition `if:` ou `needs:` | vérifier la branche et la réussite du job précédent |
| Conteneur redémarre en boucle | erreur applicative | `docker logs <nom>` sur le serveur |

> **Méthode :** lire les logs **de bas en haut** dans l'onglet Actions, repérer la
> **première** step en rouge. C'est presque toujours là qu'est la cause réelle.

## 7. Bonnes pratiques

- **Épingler les versions d'actions** (`@v4`) — jamais de tag mouvant non maîtrisé.
- **Un workflow = une responsabilité** claire et lisible.
- **`timeout-minutes:`** sur chaque job pour éviter un runner bloqué qui consomme.
- **Filtrer avec `paths:`** dans un monorepo.
- **Tester en PR, déployer sur `main`** — la séparation que nous avons mise en place.
- **Tracer par hash de commit** pour des rollbacks fiables.
- **Tout secret dans les Secrets**, jamais dans le code.

## 8. Checklist finale du pipeline

- [ ] Le Dockerfile multi-stage builde et démarre **en local**.
- [ ] Le workflow est dans `.github/workflows/`.
- [ ] `on:` déclenche sur les bonnes branches, filtré par `paths:`.
- [ ] Job `build` : checkout → setup-node → `npm ci` → build → image → **smoke test**.
- [ ] Job `push-image` : conditionné `main`/`develop`, login GHCR, tags via metadata.
- [ ] Job `deploy` : conditionné `main`, SSH, `pull` + `run` + **healthcheck**.
- [ ] Secrets `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY` configurés.
- [ ] Caches npm et Docker activés.
- [ ] `--restart unless-stopped` sur le conteneur de prod.
- [ ] (Optionnel) Environnement `production` avec approbation manuelle.

---

## Conclusion

Vous disposez d'un pipeline **CI/CD complet** : chaque `git push` sur `main` compile
l'application Angular, construit et teste une image Docker, la publie sur GHCR, puis la
déploie automatiquement sur votre serveur via SSH — **de façon reproductible, tracée et
sécurisée**.

Le déploiement n'est plus un rituel manuel stressant : c'est un **effet de bord du
merge**. C'est tout l'intérêt du DevOps.

> **Pour aller plus loin :** reverse-proxy Traefik/Nginx avec HTTPS automatique
> (Let's Encrypt), déploiement *blue-green* sans coupure, orchestration avec Docker Swarm
> ou Kubernetes, et tests end-to-end (Cypress/Playwright) intégrés au job `build`.
