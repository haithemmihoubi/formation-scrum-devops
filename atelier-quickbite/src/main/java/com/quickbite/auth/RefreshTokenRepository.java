package com.quickbite.auth;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/** ATELIER 3 — accès aux refresh tokens. */
public interface RefreshTokenRepository extends JpaRepository<RefreshTokenEntity, String> {
    Optional<RefreshTokenEntity> findByToken(String token);
}
