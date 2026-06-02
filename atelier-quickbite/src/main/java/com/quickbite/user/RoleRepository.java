package com.quickbite.user;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/** ATELIER 2 — accès aux rôles en base. */
public interface RoleRepository extends JpaRepository<RoleEntity, Long> {
    Optional<RoleEntity> findByName(String name);
}
