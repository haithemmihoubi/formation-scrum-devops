package com.quickbite.auth;

import com.quickbite.auth.AuthDtos.LoginRequest;
import com.quickbite.auth.AuthDtos.RefreshRequest;
import com.quickbite.auth.AuthDtos.TokenResponse;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * ATELIER 3 — endpoints d'authentification (publics) + /users/me (protégé).
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    @org.springframework.web.bind.annotation.ResponseStatus(org.springframework.http.HttpStatus.CREATED)
    public TokenResponse register(@Valid @RequestBody AuthDtos.RegisterRequest req) {
        return authService.register(req.username(), req.password());
    }

    @PostMapping("/login")
    public TokenResponse login(@Valid @RequestBody LoginRequest req) {
        return authService.login(req.username(), req.password());
    }

    @PostMapping("/refresh")
    public TokenResponse refresh(@Valid @RequestBody RefreshRequest req) {
        return authService.refresh(req.refreshToken());
    }

    /** Renvoie l'identité de l'utilisateur authentifié (à partir du token). */
    @GetMapping("/me")
    public Map<String, Object> me(Authentication auth) {
        return Map.of(
            "username", auth.getName(),
            "authorities", auth.getAuthorities()
        );
    }
}
