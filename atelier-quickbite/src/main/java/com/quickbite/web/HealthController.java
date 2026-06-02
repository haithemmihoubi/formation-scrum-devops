package com.quickbite.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

/**
 * ATELIER 0 — premier endpoint public, pour vérifier que l'application démarre.
 * Accessible sans authentification (voir SecurityConfig).
 */
@RestController
public class HealthController {

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of(
            "status", "UP",
            "service", "quickbite-api",
            "time", Instant.now().toString()
        );
    }
}
