# MODULE 3 — Spring Security

## Chapitre 15 — Les fondamentaux de la sécurité applicative

Avant d'écrire la moindre ligne de Spring Security, il faut maîtriser un socle de concepts. Sans eux, on configure des choses sans comprendre ce qu'on protège, et on crée des failles.

### 15.1 Authentification et autorisation : deux choses distinctes

Ce sont les deux piliers de la sécurité, et on les confond très souvent. Pourtant, ils répondent à deux questions différentes :

- L'**authentification** (en abrégé *AuthN*) répond à : **« Qui es-tu ? »** On vérifie l'**identité** : tu prétends être Alice ; prouve-le (avec un mot de passe, un token, un certificat…).
- L'**autorisation** (en abrégé *AuthZ*) répond à : **« As-tu le droit de faire cela ? »** Une fois qu'on sait que tu es Alice, a-t-elle la permission d'accéder à la console d'administration ?

L'ordre est immuable : on authentifie **d'abord**, on autorise **ensuite**.

| | Authentification (AuthN) | Autorisation (AuthZ) |
|--|--------------------------|----------------------|
| Question posée | « Qui es-tu ? » | « As-tu le droit ? » |
| Vérifie | L'identité | Les permissions |
| Vient | En premier | Après |
| Exemple QuickBite | Se connecter à l'application | Accéder à la console admin |

<div class="callout danger"><span class="title">❗ Une erreur de raisonnement dangereuse</span>
Un utilisateur <b>authentifié n'est pas pour autant autorisé</b>. Le fait de savoir « c'est bien Alice » ne dit rien sur ce qu'Alice a le droit de faire. Les deux contrôles sont indépendants et tous les deux obligatoires. Oublier le second (l'autorisation) est la cause de la faille la plus répandue du web : le « <i>Broken Access Control</i> », numéro 1 du classement OWASP.
</div>

### 15.2 Stateful ou stateless : deux façons de « se souvenir » de l'utilisateur

Une fois l'utilisateur connecté, comment le serveur se souvient-il de lui à la requête suivante ? Deux approches opposées :

- **Stateful (avec session).** Le serveur crée une **session** en mémoire et donne au client un identifiant de session (un cookie `JSESSIONID`). À chaque requête, le client renvoie ce cookie, et le serveur retrouve la session. Simple, mais le serveur doit **garder un état** : si on a plusieurs serveurs, il faut partager les sessions entre eux, ce qui complique la mise à l'échelle.
- **Stateless (avec token).** Le serveur ne garde **rien** en mémoire. Il remet au client un **token** (typiquement un JWT, qu'on verra au chapitre 18) qui contient lui-même les informations d'identité, signées. À chaque requête, le client présente ce token, et le serveur le vérifie sans rien avoir à stocker.

| Critère | Stateful (session) | Stateless (token) |
|---------|--------------------|--------------------|
| Stockage côté serveur | Oui (les sessions) | Aucun |
| Mise à l'échelle horizontale | Difficile | Facile |
| Révocation immédiate | Facile (on invalide la session) | Difficile (le token reste valide jusqu'à expiration) |
| Cas d'usage idéal | Application web classique | API REST, application mobile, microservices |

Pour une **API REST** moderne (notre cas avec QuickBite), on choisit presque toujours le **stateless**, car il s'adapte naturellement à la montée en charge et aux clients variés (web, mobile).

### 15.3 Stocker les mots de passe : le hachage

Voici une règle absolue : **on ne stocke jamais un mot de passe en clair**, ni même chiffré de façon réversible. On stocke un **hachage** (*hash*) : le résultat d'une fonction mathématique à sens unique. À la connexion, on hache le mot de passe saisi et on compare au hachage stocké. Ainsi, même si la base de données est volée, les mots de passe ne sont pas directement exposés.

Mais tous les hachages ne se valent pas. Pour les mots de passe, il faut une fonction **lente** et **salée** :

- Le **sel** (*salt*) est une valeur aléatoire, différente pour chaque mot de passe, ajoutée avant le hachage. Il empêche les attaques par tables précalculées (*rainbow tables*).
- La **lenteur** est volontaire : elle ralentit l'attaquant qui essaierait des millions de mots de passe (force brute), sans gêner l'utilisateur légitime qui ne se connecte qu'une fois.

```java
@Bean
public PasswordEncoder passwordEncoder() {
    // BCrypt avec un "coût" (work factor) de 12 :
    // plus le coût est élevé, plus le hachage est lent (donc sûr)
    return new BCryptPasswordEncoder(12);
}
```

| Algorithme | Caractéristique |
|------------|-----------------|
| **BCrypt** | Standard éprouvé, intègre le sel, coût ajustable. Le choix par défaut sûr. |
| **Argon2** | Lauréat du concours mondial de hachage de mots de passe ; résistant aux attaques par GPU. Recommandé pour les nouveaux projets. |
| **PBKDF2** | Largement supporté, conforme aux normes FIPS. |
| ~~MD5, SHA-1, SHA-256 seuls~~ | **À proscrire pour les mots de passe** : ils sont conçus pour être rapides, donc faciles à attaquer par force brute. |

<div class="callout warn"><span class="title">⚠️ « Mais SHA-256 est réputé sûr, non ? »</span>
SHA-256 est un excellent hachage… pour vérifier l'intégrité d'un fichier. Mais pour un mot de passe, sa <b>rapidité</b> est un défaut : un attaquant peut tester des milliards de combinaisons par seconde. BCrypt et Argon2 sont <b>volontairement lents</b>, ce qui rend la force brute économiquement impossible. La vitesse, qualité ailleurs, est un défaut ici.
</div>

### 15.4 Les attaques courantes et leurs parades

| Attaque | En quoi elle consiste | La parade |
|---------|----------------------|-----------|
| **Force brute** | Essayer des milliers de mots de passe jusqu'à trouver | Hachage lent, limitation du débit, blocage du compte, double authentification |
| **MITM** (homme du milieu) | Intercepter le trafic entre client et serveur | **HTTPS/TLS partout**, en-tête HSTS |
| **XSS** | Injecter du JavaScript malveillant dans une page | Échapper les sorties, politique CSP, cookies `HttpOnly` |
| **CSRF** | Forcer le navigateur d'une victime à envoyer une requête à son insu | Token anti-CSRF, attribut de cookie `SameSite`, ou API stateless |
| **Injection SQL** | Glisser du code SQL dans un champ de saisie | Requêtes paramétrées, utilisation d'un ORM |

---

## Chapitre 16 — L'architecture de Spring Security 6

### 16.1 L'idée centrale : une chaîne de filtres

Spring Security ne s'éparpille pas dans tout votre code. Il s'insère **avant** votre application, sous la forme d'une **chaîne de filtres** (`SecurityFilterChain`). Chaque requête HTTP entrante traverse cette chaîne **avant** d'atteindre votre contrôleur. Chaque filtre a un rôle : l'un extrait les identifiants, un autre vérifie l'autorisation, etc.

```
Requête ─► [chaîne de filtres Security] ─► AuthenticationManager ─► AuthenticationProvider
                  │                                                        │
                  │                                                UserDetailsService
                  ▼                                                        │
            SecurityContext  ◄──── Authentication (l'utilisateur + ses rôles)
                  │
                  ▼
        AuthorizationManager (a-t-il le droit ?) ─► votre Contrôleur
```

### 16.2 Les composants, un par un

| Composant | Son rôle |
|-----------|----------|
| `SecurityFilterChain` | Déclare les règles : quelles URL sont publiques, lesquelles sont protégées, comment on se connecte |
| `AuthenticationManager` | Le chef d'orchestre de l'authentification |
| `AuthenticationProvider` | Celui qui vérifie réellement les identifiants |
| `UserDetailsService` | Celui qui va chercher l'utilisateur (par exemple dans la base de données) |
| `UserDetails` / `GrantedAuthority` | La représentation de l'utilisateur et de ses rôles/permissions |
| `SecurityContext` | Le « porte-document » qui conserve l'utilisateur authentifié pendant toute la durée de la requête |

Le flux se lit ainsi : la requête arrive, les filtres en extraient les identifiants, l'`AuthenticationManager` délègue à un `AuthenticationProvider` qui, via le `UserDetailsService`, charge l'utilisateur et vérifie son mot de passe. Si tout est bon, un objet `Authentication` (contenant l'identité et les rôles) est placé dans le `SecurityContext`. Ensuite, pour chaque ressource demandée, l'`AuthorizationManager` vérifie que cet utilisateur a bien le droit d'y accéder.

### 16.3 Le grand changement de Spring Security 6

<div class="callout danger"><span class="title">❗ WebSecurityConfigurerAdapter n'existe plus</span>
Si vous trouvez sur Internet du code qui étend <code>WebSecurityConfigurerAdapter</code> et surcharge une méthode <code>configure(HttpSecurity http)</code>, c'est de l'<b>ancien code (Spring Security 5)</b>. Cette classe a été <b>supprimée</b> en Spring Security 6. Le nouveau modèle consiste à déclarer un <b>bean</b> de type <code>SecurityFilterChain</code> et à configurer la sécurité avec une <b>syntaxe à base de lambdas</b>. Beaucoup de tutoriels obsolètes traînent encore : vérifiez toujours la version.
</div>

Voici la configuration **moderne**, telle qu'on l'écrit aujourd'hui :

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/", "/public/**").permitAll()   // accès libre
                .requestMatchers("/admin/**").hasRole("ADMIN")    // réservé aux admins
                .anyRequest().authenticated()                     // tout le reste : connecté
            )
            .httpBasic(Customizer.withDefaults())   // active l'authentification Basic
            .formLogin(Customizer.withDefaults());  // active le formulaire de login
        return http.build();
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

Lisez la section `authorizeHttpRequests` de haut en bas, comme une liste de règles évaluées dans l'ordre : les URL publiques d'abord, puis les URL d'admin réservées au rôle ADMIN, et enfin une règle « attrape-tout » qui exige au minimum d'être authentifié.

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 1 : premier projet sécurisé</span>
1. Générez un projet Spring Boot 3 (dépendances Web + Security) sur <a href="https://start.spring.io">start.spring.io</a>. Lancez-le et observez : Spring Security protège <b>tout</b> par défaut et génère un mot de passe affiché dans la console.<br>
2. Créez un contrôleur avec une route publique <code>/</code> et une route protégée <code>/private</code>, puis configurez la <code>SecurityFilterChain</code>.<br>
3. Définissez deux utilisateurs en mémoire (<code>user</code> et <code>admin</code>) avec des rôles différents, et testez l'accès à <code>/admin</code>.
</div>

```java
@Bean
UserDetailsService users(PasswordEncoder encoder) {
    UserDetails user = User.withUsername("user")
        .password(encoder.encode("user123")).roles("USER").build();
    UserDetails admin = User.withUsername("admin")
        .password(encoder.encode("admin123")).roles("ADMIN").build();
    return new InMemoryUserDetailsManager(user, admin);
}
```

---

## Chapitre 17 — Authentification et autorisation (RBAC)

On passe maintenant des utilisateurs « en mémoire » (pratiques pour démarrer) à de vrais utilisateurs persistés en base, et on met en place un contrôle d'accès fin.

### 17.1 Charger les utilisateurs depuis la base

On crée une entité JPA pour représenter un utilisateur :

```java
@Entity
@Table(name = "users")
public class UserEntity {
    @Id @GeneratedValue
    private Long id;
    @Column(unique = true, nullable = false)
    private String username;
    @Column(nullable = false)
    private String password;           // le HASH BCrypt, jamais le mot de passe en clair
    @ManyToMany(fetch = FetchType.EAGER)
    private Set<RoleEntity> roles = new HashSet<>();
    // getters / setters
}
```

Puis on implémente un `UserDetailsService` qui va chercher cet utilisateur et le traduit dans le format attendu par Spring Security :

```java
@Service
public class JpaUserDetailsService implements UserDetailsService {

    private final UserRepository repo;
    public JpaUserDetailsService(UserRepository repo) { this.repo = repo; }

    @Override
    public UserDetails loadUserByUsername(String username) {
        UserEntity u = repo.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException(username));
        // on transforme les rôles en "autorités" comprises par Spring
        var authorities = u.getRoles().stream()
            .map(r -> new SimpleGrantedAuthority("ROLE_" + r.getName()))
            .collect(Collectors.toList());
        return new org.springframework.security.core.userdetails.User(
            u.getUsername(), u.getPassword(), authorities);
    }
}
```

<div class="callout tip"><span class="title">💡 Message d'erreur volontairement vague</span>
Lorsqu'une connexion échoue, renvoyez toujours un message <b>générique</b> du type « identifiants invalides », sans préciser si c'est le nom d'utilisateur ou le mot de passe qui est faux. Sinon, un attaquant peut <b>énumérer les comptes existants</b> (« ce login existe, mais pas ce mot de passe »). Ne donnez jamais d'information utile à l'attaquant.
</div>

### 17.2 Rôles, autorités, permissions

Distinguons deux niveaux de granularité :

- Un **rôle** est un regroupement large : `ROLE_ADMIN`, `ROLE_USER`. C'est grossier.
- Une **autorité** ou **permission** est un droit précis : `order:read` (lire les commandes), `order:cancel` (annuler une commande). C'est fin.

Un modèle **RBAC** mature associe : *un utilisateur a des rôles, et chaque rôle regroupe des permissions*. On contrôle ensuite les accès par **permission** plutôt que par rôle. Pourquoi ? Parce que si demain on crée un nouveau rôle « Manager » qui peut lire mais pas annuler les commandes, on lui attribue simplement la permission `order:read` — sans toucher au code, qui vérifie des permissions et non des rôles.

```
Utilisateur ──*..*── Rôle ──*..*── Permission
   alice          ADMIN          order:read, order:cancel, user:manage
   bob            CLIENT         order:read, order:create
```

### 17.3 Protéger les méthodes

On active la sécurité au niveau des méthodes :

```java
@Configuration
@EnableMethodSecurity   // active @PreAuthorize, @PostAuthorize, etc.
public class MethodSecurityConfig { }
```

Puis on annote directement les méthodes des contrôleurs :

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping
    @PreAuthorize("hasAuthority('order:read')")   // exige la permission de lecture
    public List<OrderDto> all() { ... }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")             // exige le rôle ADMIN
    public void delete(@PathVariable Long id) { ... }

    // Expression plus fine : un admin OU le propriétaire de la ressource
    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or #username == authentication.name")
    public OrderDto getOne(@PathVariable Long id,
                           @RequestParam String username) { ... }
}
```

| Annotation | Quand elle est évaluée | Remarque |
|------------|------------------------|----------|
| `@PreAuthorize` | **Avant** l'exécution de la méthode | La plus utilisée ; accepte des expressions riches |
| `@PostAuthorize` | **Après**, sur la valeur de retour | Pour filtrer selon l'objet renvoyé |
| `@Secured` | Avant | Plus ancien, ne gère que les rôles |

<div class="callout warn"><span class="title">⚠️ Le piège du préfixe ROLE_</span>
En Spring Security, <code>hasRole('ADMIN')</code> cherche en réalité une autorité nommée <code>ROLE_ADMIN</code> : le préfixe <code>ROLE_</code> est ajouté automatiquement. Si vos rôles en base sont déjà préfixés (ou pas), c'est une source de bugs très fréquente où l'accès est refusé sans raison apparente. Choisissez une convention et tenez-vous-y.
</div>

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 2 : modèle rôles/permissions</span>
1. Créez les entités <code>UserEntity</code> et <code>RoleEntity</code> (avec permissions) et leurs repositories ; insérez un admin et un client.<br>
2. Implémentez le <code>JpaUserDetailsService</code>.<br>
3. Protégez <code>/orders</code> (lecture pour CLIENT), <code>/admin/**</code> (ADMIN), et la suppression (ADMIN uniquement).<br>
4. Testez avec Postman et vérifiez bien les codes de réponse : <b>200</b> (autorisé), <b>401</b> (non authentifié), <b>403</b> (authentifié mais pas le droit).
</div>

<div class="callout note"><span class="title">📘 401 contre 403 : la nuance à retenir</span>
Ces deux codes d'erreur sont souvent confondus. <b>401 Unauthorized</b> signifie « je ne sais pas qui tu es » (tu n'es pas authentifié, ou ton token est invalide). <b>403 Forbidden</b> signifie « je sais qui tu es, mais tu n'as pas le droit ». Le 401 concerne l'authentification, le 403 concerne l'autorisation.
</div>

---

## Chapitre 18 — Les tokens JWT en détail

### 18.1 Ce qu'est un JWT et pourquoi il est pratique

Un **JWT** (*JSON Web Token*) est un jeton **auto-porteur** : il contient lui-même les informations d'identité de l'utilisateur, et il est **signé** numériquement. Grâce à la signature, le serveur peut vérifier que le token est authentique **sans interroger la base de données** à chaque requête. C'est exactement ce qu'il faut pour le **stateless** vu au chapitre 15.

Un JWT se compose de **trois parties**, encodées et séparées par des points :

```
header.payload.signature

eyJhbGciOiJIUzI1NiJ9 . eyJzdWIiOiJhbGljZSIsInJvbGUiOiJBRE1JTiJ9 . 3xT9...signature
```

| Partie | Contenu | Exemple |
|--------|---------|---------|
| **Header** | L'algorithme de signature et le type | `{"alg":"HS256","typ":"JWT"}` |
| **Payload** | Les *claims* : identité, rôles, date d'expiration… | `{"sub":"alice","role":"ADMIN","exp":...}` |
| **Signature** | La signature cryptographique du header + payload | garantit l'**intégrité** |

<div class="callout danger"><span class="title">❗ Un JWT n'est PAS chiffré — il est seulement signé</span>
C'est le malentendu le plus dangereux. Le payload d'un JWT est seulement <b>encodé</b> en base64 : n'importe qui peut le décoder et <b>lire son contenu</b> (essayez sur le site jwt.io). La signature garantit qu'il n'a pas été <b>modifié</b>, mais <b>pas</b> qu'il est secret. Conséquence : ne mettez <b>jamais</b> de donnée sensible (mot de passe, numéro de carte, secret) dans un JWT.
</div>

### 18.2 Access token et refresh token

Un seul token poserait un dilemme : s'il dure longtemps, le risque est grand en cas de vol ; s'il dure peu, l'utilisateur doit se reconnecter sans cesse. La solution est d'utiliser **deux tokens** :

- L'**access token** a une durée **courte** (5 à 15 minutes) et accompagne chaque requête. S'il est volé, le risque est limité dans le temps.
- Le **refresh token** a une durée **longue** (plusieurs jours), est stocké de façon sécurisée, et ne sert qu'à **une seule chose** : obtenir un nouvel access token quand l'ancien expire.

```
Connexion ──► access token (15 min) + refresh token (7 jours)
   │
   ├─ requêtes à l'API avec l'access token
   │
   └─ access token expiré ──► POST /auth/refresh (avec le refresh token)
                                       │
                                       └──► nouvel access token
```

<div class="callout warn"><span class="title">⚠️ Rotation et stockage des refresh tokens</span>
Deux bonnes pratiques essentielles : (1) appliquez la <b>rotation</b> — chaque fois qu'un refresh token est utilisé, il est invalidé et remplacé par un nouveau, ce qui permet de détecter un vol. (2) Stockez les refresh tokens en base pour pouvoir les <b>révoquer</b>. Côté navigateur, préférez un cookie <code>HttpOnly</code> + <code>SameSite</code> plutôt que le <code>localStorage</code>, qui est vulnérable aux attaques XSS.
</div>

### 18.3 Implémenter JWT dans Spring Security 6

Il existe deux approches. L'approche **« maison »** (un filtre que l'on écrit soi-même) est excellente pour **comprendre la mécanique** ; l'approche **« resource server »** standard de Spring est celle qu'on privilégie en production car elle demande très peu de code. Présentons d'abord l'approche maison.

**Le service qui fabrique et lit les tokens** (avec la bibliothèque JJWT) :

```java
@Service
public class JwtService {
    private final SecretKey key = Keys.hmacShaKeyFor(
        System.getenv("JWT_SECRET").getBytes(StandardCharsets.UTF_8));

    public String generateAccess(UserDetails user) {
        return Jwts.builder()
            .subject(user.getUsername())
            .claim("roles", user.getAuthorities().stream()
                 .map(GrantedAuthority::getAuthority).toList())
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + 900_000)) // 15 minutes
            .signWith(key)
            .compact();
    }

    public Jws<Claims> parse(String token) {
        return Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
    }
}
```

**Le filtre** qui, à chaque requête, lit le token et place l'utilisateur dans le contexte de sécurité :

```java
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtService jwt;
    public JwtAuthFilter(JwtService jwt) { this.jwt = jwt; }

    @Override
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String header = req.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            try {
                Claims claims = jwt.parse(header.substring(7)).getPayload();
                var roles = ((List<?>) claims.get("roles")).stream()
                    .map(r -> new SimpleGrantedAuthority(r.toString())).toList();
                var auth = new UsernamePasswordAuthenticationToken(
                    claims.getSubject(), null, roles);
                SecurityContextHolder.getContext().setAuthentication(auth);
            } catch (JwtException e) {
                SecurityContextHolder.clearContext();  // token invalide → non authentifié
            }
        }
        chain.doFilter(req, res);
    }
}
```

**La configuration stateless**, qui désactive les sessions et insère notre filtre :

```java
@Bean
SecurityFilterChain api(HttpSecurity http, JwtAuthFilter jwtFilter) throws Exception {
    http
        .csrf(csrf -> csrf.disable())   // API stateless → CSRF non pertinent (voir ch. 20)
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/auth/**").permitAll()
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
    return http.build();
}
```

L'**approche standard** (resource server), pour comparaison, se résume à quelques lignes : Spring valide alors lui-même les tokens à partir d'une URL de clés publiques (JWKS) fournie par le serveur d'autorisation.

```java
http.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
```

### 18.4 Gérer proprement les erreurs

On distingue les deux cas vus au chapitre 17 :

```java
// 401 : l'utilisateur n'est pas authentifié
@Component
public class JwtEntryPoint implements AuthenticationEntryPoint {
    public void commence(HttpServletRequest req, HttpServletResponse res,
                         AuthenticationException ex) throws IOException {
        res.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Authentification requise");
    }
}

// 403 : l'utilisateur est authentifié mais n'a pas le droit
@Component
public class RestAccessDeniedHandler implements AccessDeniedHandler {
    public void handle(HttpServletRequest req, HttpServletResponse res,
                       AccessDeniedException ex) throws IOException {
        res.sendError(HttpServletResponse.SC_FORBIDDEN, "Accès refusé");
    }
}
```

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 3 : API REST sécurisée par JWT</span>
Implémentez les endpoints suivants : <code>POST /auth/login</code> (renvoie access + refresh), <code>POST /auth/refresh</code> (renvoie un nouvel access), <code>GET /users/me</code> (authentifié) et <code>GET /admin/users</code> (réservé ADMIN).<br><br>
<b>Critères de réussite :</b> la connexion renvoie deux tokens ; <code>/users/me</code> fonctionne avec le Bearer ; <code>/admin/users</code> renvoie 403 pour un non-admin ; un token expiré renvoie un 401 propre, et le refresh fournit un nouvel access token.<br><br>
<b>Pièges à éviter :</b> oublier <code>STATELESS</code> (Spring recrée alors des sessions), placer le filtre au mauvais endroit, ou utiliser un secret trop court pour HS256 (il faut au moins 256 bits).
</div>

---

## Chapitre 19 — OAuth2, OpenID Connect et Keycloak

### 19.1 Le problème : déléguer l'authentification

Jusqu'ici, notre application gérait elle-même les mots de passe. Mais souvent, on veut :

- permettre la connexion « avec Google » ou « avec GitHub » (sans gérer de mot de passe) ;
- centraliser l'authentification de plusieurs applications (le *Single Sign-On*, ou SSO) ;
- qu'une application puisse accéder à mes données sur un autre service, **sans lui donner mon mot de passe**.

C'est exactement ce que résolvent OAuth2 et OpenID Connect.

### 19.2 OAuth2 et OpenID Connect : la différence

- **OAuth2** est un protocole d'**autorisation déléguée**. Il répond à : « cette application a-t-elle le droit d'accéder à telles ressources en mon nom ? » Il n'a pas été conçu, à l'origine, pour dire **qui** est l'utilisateur.
- **OpenID Connect (OIDC)** est une **couche d'authentification** ajoutée par-dessus OAuth2. Il répond à : « **qui** est l'utilisateur ? » et ajoute pour cela un **ID token**.

En résumé : OAuth2 gère l'**autorisation**, OIDC ajoute l'**authentification**. Aujourd'hui, quand on parle de « se connecter avec Google », on utilise OIDC.

### 19.3 Les acteurs

| Rôle | Description |
|------|-------------|
| **Resource Owner** | L'utilisateur (le propriétaire des données) |
| **Client** | L'application qui veut accéder aux ressources (notre front, par exemple) |
| **Authorization Server** | Le serveur qui authentifie et délivre les tokens (Keycloak, Google…) |
| **Resource Server** | L'API qui héberge les ressources protégées (notre QuickBite API) |

### 19.4 Le flow recommandé : Authorization Code + PKCE

Il existe plusieurs « flows » (scénarios d'échange). Le standard actuel pour le web et le mobile est l'**Authorization Code Flow**, renforcé par **PKCE** :

```
Utilisateur ─► Client ─► Authorization Server (affiche la page de connexion)
                              │  (l'utilisateur s'authentifie et consent)
        ◄── code d'autorisation ─┘
Client ─► échange ce code (+ son secret PKCE) ─► Authorization Server
        ◄──── access token (+ id token + refresh) ─┘
Client ─► appelle l'API avec l'access token ─► Resource Server
```

| Flow | Usage | Statut |
|------|-------|--------|
| **Authorization Code + PKCE** | Web, mobile, applications monopage (SPA) | **Recommandé** |
| Client Credentials | De machine à machine (pas d'utilisateur) | OK pour les services |
| ~~Implicit~~ | Ancien flow pour SPA | **Déconseillé** (remplacé par Code+PKCE) |
| ~~Password (ROPC)~~ | L'app récupère directement le mot de passe | **Déconseillé** |

<div class="callout note"><span class="title">📘 À quoi sert PKCE ?</span>
PKCE (<i>Proof Key for Code Exchange</i>) protège les clients « publics » (applications mobiles ou monopages) qui ne peuvent pas garder un secret. Le principe : au début, le client invente un secret aléatoire (<code>code_verifier</code>) et n'envoie que son empreinte (<code>code_challenge</code>). À la fin, il prouve qu'il détient bien le secret original. Ainsi, même si un attaquant intercepte le code d'autorisation, il ne peut pas l'échanger sans le secret.
</div>

### 19.5 ID token contre access token

Une distinction subtile mais importante en OIDC :

- L'**ID token** prouve **qui est l'utilisateur** (il contient son nom, son e-mail…). Il est destiné au **client** (l'application front).
- L'**access token** autorise l'accès à une **API**. Il est destiné au **resource server** (l'API).

### 19.6 Keycloak : le serveur d'identité

**Keycloak** est un serveur open source de gestion des identités et des accès (IAM). Il fait office d'*Authorization Server* : il gère les utilisateurs, l'authentification, le SSO, les rôles, et délivre les tokens. On le lance facilement avec Docker :

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:24.0 start-dev
```

| Concept Keycloak | Définition |
|------------------|------------|
| **Realm** | Un espace totalement isolé regroupant ses propres utilisateurs, clients et rôles |
| **Client** | Une application enregistrée (un front, une API…) |
| **Roles** | Les rôles, définis au niveau du realm ou d'un client |
| **Mappers** | Ce qui injecte des données (rôles, attributs) dans les tokens |

Côté Spring, on configure alors l'application **soit en client** (pour gérer le login), **soit en resource server** (pour valider les tokens émis par Keycloak) :

```yaml
# L'API en resource server : elle valide les tokens émis par Keycloak
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: http://localhost:8080/realms/quickbite
```

<div class="callout tip"><span class="title">💡 Mapper les rôles Keycloak</span>
Keycloak place les rôles dans une partie du token nommée <code>realm_access.roles</code> (ou <code>resource_access</code>). Par défaut, Spring ne sait pas les y trouver. Vous devez écrire un petit « converter » qui extrait ces rôles et les transforme en autorités préfixées <code>ROLE_</code>, pour que <code>hasRole()</code> fonctionne. C'est la cause n°1 des « 403 inexpliqués » avec Keycloak.
</div>

<div class="callout lab"><span class="title">🧪 Exercice — Atelier 4 : login OAuth2 et front protégé</span>
1. Lancez Keycloak (Docker), créez un realm <code>quickbite</code>, un client, des rôles (<code>admin</code>, <code>client</code>) et deux utilisateurs.<br>
2. Configurez l'API en resource server et mappez les rôles Keycloak.<br>
3. Obtenez un token via Keycloak (avec Postman) et appelez <code>/admin/**</code> pour vérifier l'autorisation.<br>
4. Configurez un front (Angular ou React) avec une bibliothèque OIDC, en Authorization Code + PKCE ; le front appelle l'API avec le token et affiche ou masque la console admin selon le rôle.<br><br>
<b>Astuce de debug :</b> collez le token sur <b>jwt.io</b> pour vérifier les claims et les rôles. C'est extrêmement révélateur.
</div>

---

## Chapitre 20 — Durcissement et bonnes pratiques (OWASP)

On a une application qui authentifie et autorise. Reste à la **durcir** contre le monde réel.

### 20.1 CORS et CSRF : deux notions qu'on confond toujours

Malgré leurs noms proches, ce sont deux choses **totalement différentes** :

| | CORS | CSRF |
|--|------|------|
| Ce que c'est | Une **permission** : autoriser un site d'un **autre domaine** à appeler votre API depuis un navigateur | Une **attaque** (et sa parade) : empêcher qu'une requête soit forgée à l'insu de l'utilisateur |
| Nature | Un mécanisme de sécurité du navigateur | Une vulnérabilité |
| Concerne | Les API appelées par un front hébergé ailleurs | Les sessions et les cookies |

```java
@Bean
CorsConfigurationSource corsSource() {
    CorsConfiguration c = new CorsConfiguration();
    c.setAllowedOrigins(List.of("https://app.quickbite.com")); // qui a le droit d'appeler
    c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    c.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    UrlBasedCorsConfigurationSource s = new UrlBasedCorsConfigurationSource();
    s.registerCorsConfiguration("/**", c);
    return s;
}
```

<div class="callout warn"><span class="title">⚠️ Quand désactiver CSRF (et quand surtout pas)</span>
On voit beaucoup de code qui désactive CSRF sans réfléchir. La règle : pour une API <b>stateless</b> authentifiée par token (sans cookie de session), CSRF n'est pas pertinent, on peut le désactiver. Mais pour une application web classique <b>avec session et cookies</b>, CSRF doit <b>impérativement rester activé</b>. Ne désactivez jamais CSRF « par habitude » ou pour faire taire une erreur.
</div>

### 20.2 Limiter le débit (rate limiting)

Pour contrer la force brute et les abus, on **limite le nombre de requêtes** par client ou par adresse IP sur une période donnée. En Spring, on peut utiliser la bibliothèque **Bucket4j**, ou mieux, traiter cela en amont au niveau de la **passerelle d'API** (API Gateway) ou du reverse proxy. C'est particulièrement crucial sur l'endpoint de connexion.

### 20.3 Gérer les exceptions sans fuiter d'information

Une erreur mal gérée peut révéler à l'attaquant des détails internes (structure de la base, chemins de fichiers…). On centralise donc la gestion des erreurs pour **logger le détail côté serveur** mais ne renvoyer au client qu'un **message générique** :

```java
@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiError> handle(Exception ex) {
        // on loggue le détail en interne, on renvoie un message neutre au client
        return ResponseEntity.status(500).body(new ApiError("Erreur interne"));
    }
}
```

### 20.4 Audit et journalisation

Tracez les **événements de sécurité** : connexions réussies et échouées, accès refusés. Avec Spring Boot Actuator, exposez ces informations — mais **protégez** ces endpoints, ne les ouvrez pas publiquement. Et une règle absolue : **ne journalisez jamais de secret, de mot de passe ou de token.**

### 20.5 Architecture microservices : la passerelle d'API

Dans une architecture en microservices, on place une **API Gateway** (par exemple Spring Cloud Gateway) en point d'entrée unique. Elle centralise l'authentification, la limitation de débit, le routage et la terminaison TLS :

```
Client ─► API Gateway (authentification, rate limit, TLS) ─► Service A
                                                          ├► Service B
                                                          └► Service C
```

On prévoit aussi la **rotation des clés de signature** des JWT : en gardant plusieurs clés actives identifiées par un `kid`, on peut renouveler régulièrement les clés sans invalider brutalement tous les tokens existants.

### 20.6 La check-list de durcissement OWASP

L'**OWASP** (*Open Worldwide Application Security Project*) publie le « Top 10 » des risques de sécurité web. Voici une check-list pratique inspirée de leurs recommandations :

- [ ] HTTPS/TLS partout, HSTS activé, redirection automatique HTTP → HTTPS.
- [ ] Mots de passe hachés avec BCrypt ou Argon2, et politique de robustesse.
- [ ] Tokens à durée courte, rotation des refresh tokens, secret de signature fort.
- [ ] Validation et nettoyage de **toutes** les entrées (contre les injections).
- [ ] En-têtes de sécurité : CSP, X-Content-Type-Options, X-Frame-Options.
- [ ] CORS restrictif et CSRF cohérent avec le modèle de session.
- [ ] Limitation de débit et blocage de compte sur la connexion.
- [ ] Principe du moindre privilège partout (rôles, permissions, comptes de service).
- [ ] Dépendances tenues à jour (scan de vulnérabilités), aucun secret en clair.
- [ ] Journaux d'audit sans données sensibles, supervision des anomalies.

<div class="callout danger"><span class="title">❗ Le risque numéro un, encore et toujours</span>
Dans le classement OWASP actuel, le risque le plus répandu est le « <b>Broken Access Control</b> » — c'est-à-dire une autorisation mal faite ou absente. C'est précisément ce que les chapitres 17 et 18 vous ont appris à éviter. La leçon : la partie la plus importante de la sécurité n'est pas la cryptographie sophistiquée, c'est de <b>vérifier rigoureusement, à chaque accès, que l'utilisateur a bien le droit</b>.
</div>

<div class="callout lab"><span class="title">🧪 Exercice — TP final : un système complet et sécurisé</span>
Livrez un système QuickBite complet intégrant tout le module : une <b>API REST sécurisée par JWT</b> (login/refresh, endpoints protégés) ; une <b>console admin avec RBAC</b> (rôles et permissions fins) ; une <b>intégration Keycloak</b> (authentification et rôles délégués) ; un <b>front protégé en OAuth2/OIDC</b> ; et une <b>documentation Postman</b> accompagnée d'une note de sécurité (CORS, CSRF, rotation, check-list OWASP renseignée).
</div>

### 20.7 Conclusion du cursus complet

Vous avez parcouru les trois piliers d'un produit logiciel moderne, et ils forment un tout cohérent :

- Le **Module 1 (Agile)** vous a appris à décider **quoi** construire, **dans quel ordre**, et comment apprendre vite des utilisateurs.
- Le **Module 2 (DevOps)** vous a appris à **livrer** ce produit vite et de façon fiable, du code à la production.
- Le **Module 3 (Sécurité)** vous a appris à **protéger** ce qui est livré.

La phrase à emporter : **on construit le bon produit (Agile), on le livre bien (DevOps), et on le protège sérieusement (Sécurité).** Ces trois disciplines ne sont pas des silos : ce sont trois facettes d'un même métier, celui de livrer de la valeur, durablement et en confiance.
