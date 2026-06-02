package com.quickbite.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * ATELIER 5 — limitation de débit simple sur /auth/login pour freiner la
 * force brute. Implémentation en mémoire (fenêtre fixe) — en production on
 * utiliserait Bucket4j ou l'API Gateway. Pédagogique mais fonctionnel.
 */
@Component
public class LoginRateLimitFilter extends OncePerRequestFilter {

    private static final int MAX_ATTEMPTS = 5;          // par fenêtre
    private static final long WINDOW_MS = 60_000;       // 1 minute

    private record Counter(AtomicInteger count, long windowStart) { }
    private final Map<String, Counter> buckets = new ConcurrentHashMap<>();

    @Override
    protected void doFilterInternal(@NonNull HttpServletRequest req,
                                    @NonNull HttpServletResponse res,
                                    @NonNull FilterChain chain)
            throws ServletException, IOException {

        boolean isLogin = "POST".equalsIgnoreCase(req.getMethod())
                && "/auth/login".equals(req.getServletPath());

        if (isLogin && isBlocked(clientKey(req))) {
            res.setStatus(429);   // Too Many Requests
            res.setContentType("application/json");
            res.getWriter().write("{\"error\":\"Trop de tentatives. Réessayez plus tard.\"}");
            return;
        }
        chain.doFilter(req, res);
    }

    private boolean isBlocked(String key) {
        long now = System.currentTimeMillis();
        Counter c = buckets.compute(key, (k, existing) -> {
            if (existing == null || now - existing.windowStart() > WINDOW_MS) {
                return new Counter(new AtomicInteger(1), now);
            }
            existing.count().incrementAndGet();
            return existing;
        });
        return c.count().get() > MAX_ATTEMPTS;
    }

    private String clientKey(HttpServletRequest req) {
        String fwd = req.getHeader("X-Forwarded-For");
        return (fwd != null && !fwd.isBlank()) ? fwd.split(",")[0].trim() : req.getRemoteAddr();
    }
}
