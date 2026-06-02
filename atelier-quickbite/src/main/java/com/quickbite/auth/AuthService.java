package com.quickbite.auth;

import com.quickbite.auth.AuthDtos.TokenResponse;
import com.quickbite.security.JwtService;
import com.quickbite.security.SecurityProperties;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

/**
 * ATELIER 3 — logique d'authentification : login (émission access + refresh)
 * et refresh AVEC ROTATION (l'ancien refresh token est révoqué et remplacé).
 */
@Service
public class AuthService {

    private final AuthenticationManager authManager;
    private final UserDetailsService userDetailsService;
    private final JwtService jwtService;
    private final RefreshTokenRepository refreshRepo;
    private final long refreshDays;

    public AuthService(AuthenticationManager authManager,
                       UserDetailsService userDetailsService,
                       JwtService jwtService,
                       RefreshTokenRepository refreshRepo,
                       SecurityProperties props) {
        this.authManager = authManager;
        this.userDetailsService = userDetailsService;
        this.jwtService = jwtService;
        this.refreshRepo = refreshRepo;
        this.refreshDays = props.getJwt().getRefreshTokenDays();
    }

    @Transactional
    public TokenResponse login(String username, String password) {
        // Vérifie les identifiants ; lève une AuthenticationException si invalides (-> 401).
        authManager.authenticate(new UsernamePasswordAuthenticationToken(username, password));
        UserDetails user = userDetailsService.loadUserByUsername(username);
        String access = jwtService.generateAccess(user);
        String refresh = createRefreshToken(username);
        return TokenResponse.of(access, refresh);
    }

    @Transactional
    public TokenResponse refresh(String refreshToken) {
        RefreshTokenEntity stored = refreshRepo.findByToken(refreshToken)
            .filter(RefreshTokenEntity::isValid)
            .orElseThrow(() -> new IllegalArgumentException("Refresh token invalide ou expiré"));

        // Rotation : on révoque l'ancien et on en émet un nouveau.
        stored.setRevoked(true);
        refreshRepo.save(stored);

        UserDetails user = userDetailsService.loadUserByUsername(stored.getUsername());
        String access = jwtService.generateAccess(user);
        String newRefresh = createRefreshToken(stored.getUsername());
        return TokenResponse.of(access, newRefresh);
    }

    private String createRefreshToken(String username) {
        String token = UUID.randomUUID().toString();
        Instant expiry = Instant.now().plus(refreshDays, ChronoUnit.DAYS);
        refreshRepo.save(new RefreshTokenEntity(token, username, expiry));
        return token;
    }
}
