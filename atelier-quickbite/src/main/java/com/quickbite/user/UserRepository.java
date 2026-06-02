package com.quickbite.user;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/** ATELIER 2 — accès aux utilisateurs en base. */
public interface UserRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByUsername(String username);
    boolean existsByUsername(String username);
}
