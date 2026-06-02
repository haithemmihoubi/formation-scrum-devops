package com.quickbite.user;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * ATELIER 2 — charge l'utilisateur depuis la base et le traduit dans le
 * format attendu par Spring Security. Les rôles deviennent des autorités
 * préfixées "ROLE_" (attendu par hasRole(...)).
 */
@Service
public class JpaUserDetailsService implements UserDetailsService {

    private final UserRepository repo;

    public JpaUserDetailsService(UserRepository repo) {
        this.repo = repo;
    }

    @Override
    public UserDetails loadUserByUsername(String username) {
        UserEntity u = repo.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException("Identifiants invalides"));

        List<SimpleGrantedAuthority> authorities = u.getRoles().stream()
            .map(r -> new SimpleGrantedAuthority("ROLE_" + r.getName()))
            .toList();

        return User.withUsername(u.getUsername())
            .password(u.getPassword())
            .authorities(authorities)
            .build();
    }
}
