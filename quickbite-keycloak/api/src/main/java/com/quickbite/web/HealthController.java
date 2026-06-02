package com.quickbite.web;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

@RestController
public class HealthController {

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("status", "UP", "service", "quickbite-api-keycloak",
                      "time", Instant.now().toString());
    }

    /** Renvoie l'identité issue du token Keycloak (utile pour vérifier les rôles). */
    @GetMapping("/me")
    public Map<String, Object> me(Authentication auth) {
        return Map.of("username", auth.getName(), "authorities", auth.getAuthorities());
    }
}
