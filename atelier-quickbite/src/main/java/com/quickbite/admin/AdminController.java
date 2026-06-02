package com.quickbite.admin;

import com.quickbite.user.UserRepository;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

/**
 * ATELIER 2/3 — console d'administration. Tout est réservé au rôle ADMIN,
 * verrouillé à la fois par l'URL (/admin/**) dans SecurityConfig et par
 * l'annotation @PreAuthorize ci-dessous (défense en profondeur).
 */
@RestController
@RequestMapping("/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {

    private final UserRepository userRepo;

    public AdminController(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    @GetMapping("/users")
    public List<Map<String, Object>> users() {
        return userRepo.findAll().stream()
            .map(u -> Map.<String, Object>of(
                "id", u.getId(),
                "username", u.getUsername(),
                "roles", u.getRoles().stream().map(r -> r.getName()).toList()))
            .toList();
    }
}
