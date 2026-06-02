package com.quickbite.user;

import jakarta.persistence.*;

/**
 * ATELIER 2 — un rôle (ex. ADMIN, CLIENT). En base, on stocke le nom sans
 * le préfixe "ROLE_" ; ce préfixe est ajouté côté Spring Security.
 */
@Entity
@Table(name = "roles")
public class RoleEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String name;

    protected RoleEntity() { }

    public RoleEntity(String name) {
        this.name = name;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
