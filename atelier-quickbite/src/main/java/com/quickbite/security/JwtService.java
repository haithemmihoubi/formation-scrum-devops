package com.quickbite.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.List;

/**
 * ATELIER 3 — fabrique et valide les JWT (access token).
 * Le token est SIGNÉ (intégrité) mais PAS chiffré : ne jamais y mettre de secret.
 */
@Service
public class JwtService {

    private final SecretKey key;
    private final long accessMillis;

    public JwtService(SecurityProperties props) {
        this.key = Keys.hmacShaKeyFor(props.getJwt().getSecret().getBytes(StandardCharsets.UTF_8));
        this.accessMillis = props.getJwt().getAccessTokenMinutes() * 60_000;
    }

    /** Génère un access token de courte durée contenant le sujet et les rôles. */
    public String generateAccess(UserDetails user) {
        Date now = new Date();
        return Jwts.builder()
            .subject(user.getUsername())
            .claim("roles", user.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority).toList())
            .issuedAt(now)
            .expiration(new Date(now.getTime() + accessMillis))
            .signWith(key)
            .compact();
    }

    /** Valide la signature + l'expiration et renvoie les claims. Lève une exception si invalide. */
    public Jws<Claims> parse(String token) {
        return Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
    }

    @SuppressWarnings("unchecked")
    public List<String> extractRoles(Claims claims) {
        Object roles = claims.get("roles");
        return roles instanceof List<?> list ? (List<String>) list : List.of();
    }
}
