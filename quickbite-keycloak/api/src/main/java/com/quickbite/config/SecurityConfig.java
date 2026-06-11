package com.quickbite.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.*;

/**
 * Sécurité OIDC : l'API est un RESOURCE SERVER. Elle ne gère ni login ni
 * mots de passe — c'est Keycloak qui authentifie et émet les tokens.
 * Ici on : (1) valide les JWT via l'issuer Keycloak, (2) mappe les rôles
 * Keycloak (realm_access.roles) vers des autorités ROLE_*.
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Value("${quickbite.cors.allowed-origins}")
    private List<String> allowedOrigins;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .cors(c -> c.configurationSource(corsSource()))
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/health", "/actuator/health/**").permitAll()
                .requestMatchers("/auth/**").permitAll()
                .requestMatchers("/admin/**").hasRole("admin")
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt ->
                jwt.jwtAuthenticationConverter(jwtAuthConverter())));
        return http.build();
    }

    /** Convertit le token Keycloak en Authentication Spring (rôles + identité). */
    private JwtAuthenticationConverter jwtAuthConverter() {
        JwtAuthenticationConverter conv = new JwtAuthenticationConverter();
        conv.setPrincipalClaimName("preferred_username");
        conv.setJwtGrantedAuthoritiesConverter(SecurityConfig::extractRoles);
        return conv;
    }

    @SuppressWarnings("unchecked")
    private static Collection<GrantedAuthority> extractRoles(Jwt jwt) {
        Map<String, Object> realmAccess = jwt.getClaim("realm_access");
        if (realmAccess == null) return List.of();
        Collection<String> roles = (Collection<String>) realmAccess.getOrDefault("roles", List.of());
        List<GrantedAuthority> authorities = new ArrayList<>();
        for (String r : roles) {
            authorities.add(new SimpleGrantedAuthority("ROLE_" + r));
        }
        return authorities;
    }

    @Bean
    public CorsConfigurationSource corsSource() {
        CorsConfiguration c = new CorsConfiguration();
        c.setAllowedOrigins(allowedOrigins);
        c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        c.setAllowedHeaders(List.of("Authorization", "Content-Type"));
        c.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/**", c);
        return src;
    }
}
