package com.quickbite.auth;

import jakarta.persistence.*;

import java.time.Instant;

/**
 * ATELIER 3 — refresh token persisté pour permettre la rotation et la révocation.
 */
@Entity
@Table(name = "refresh_tokens")
public class RefreshTokenEntity {

    @Id
    @Column(length = 64)
    private String token;          // UUID

    @Column(nullable = false)
    private String username;

    @Column(nullable = false)
    private Instant expiresAt;

    @Column(nullable = false)
    private boolean revoked = false;

    protected RefreshTokenEntity() { }

    public RefreshTokenEntity(String token, String username, Instant expiresAt) {
        this.token = token;
        this.username = username;
        this.expiresAt = expiresAt;
    }

    public boolean isValid() {
        return !revoked && expiresAt.isAfter(Instant.now());
    }

    public String getToken() { return token; }
    public String getUsername() { return username; }
    public Instant getExpiresAt() { return expiresAt; }
    public boolean isRevoked() { return revoked; }
    public void setRevoked(boolean revoked) { this.revoked = revoked; }
}
