package com.quickbite.auth;

import com.quickbite.auth.AuthDtos.*;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Façade d'authentification (endpoints publics) devant Keycloak :
 *   POST /auth/register  -> crée un compte (rôle client)
 *   POST /auth/login     -> access + refresh tokens
 *   POST /auth/refresh   -> renouvelle l'access token
 *   POST /auth/logout    -> invalide la session Keycloak
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    private final KeycloakClient keycloak;

    public AuthController(KeycloakClient keycloak) {
        this.keycloak = keycloak;
    }

    @PostMapping("/register")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Object> register(@Valid @RequestBody RegisterRequest req) {
        return keycloak.register(req);
    }

    @PostMapping("/login")
    public Map<String, Object> login(@Valid @RequestBody LoginRequest req) {
        return keycloak.login(req.username(), req.password());
    }

    @PostMapping("/refresh")
    public Map<String, Object> refresh(@Valid @RequestBody RefreshRequest req) {
        return keycloak.refresh(req.refreshToken());
    }

    @PostMapping("/logout")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void logout(@Valid @RequestBody LogoutRequest req) {
        keycloak.logout(req.refreshToken());
    }
}
