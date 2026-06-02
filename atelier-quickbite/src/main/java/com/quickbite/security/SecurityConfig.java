package com.quickbite.security;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

/**
 * Configuration centrale de Spring Security 6 (modèle SecurityFilterChain).
 *  - ATELIER 1 : règles d'accès publiques/protégées
 *  - ATELIER 2 : @EnableMethodSecurity (active @PreAuthorize) + BCrypt
 *  - ATELIER 3 : stateless + filtre JWT + gestion des erreurs 401/403
 *  - ATELIER 5 : CORS, en-têtes de sécurité, rate limiting du login
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity                         // ATELIER 2 : active @PreAuthorize
@EnableConfigurationProperties(SecurityProperties.class)
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;
    private final LoginRateLimitFilter loginRateLimitFilter;
    private final JwtEntryPoint entryPoint;
    private final RestAccessDeniedHandler accessDeniedHandler;
    private final SecurityProperties props;

    public SecurityConfig(JwtAuthFilter jwtAuthFilter,
                          LoginRateLimitFilter loginRateLimitFilter,
                          JwtEntryPoint entryPoint,
                          RestAccessDeniedHandler accessDeniedHandler,
                          SecurityProperties props) {
        this.jwtAuthFilter = jwtAuthFilter;
        this.loginRateLimitFilter = loginRateLimitFilter;
        this.entryPoint = entryPoint;
        this.accessDeniedHandler = accessDeniedHandler;
        this.props = props;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // ATELIER 5 : CORS maîtrisé
            .cors(cors -> cors.configurationSource(corsSource()))
            // ATELIER 3 : API stateless authentifiée par token -> CSRF non pertinent
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // ATELIER 1 : règles d'autorisation
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/health", "/actuator/health").permitAll()
                .requestMatchers("/auth/login", "/auth/refresh").permitAll()
                .requestMatchers("/h2-console/**").permitAll()      // dev uniquement
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            // ATELIER 3 : réponses propres 401 / 403
            .exceptionHandling(e -> e
                .authenticationEntryPoint(entryPoint)
                .accessDeniedHandler(accessDeniedHandler))
            // ATELIER 5 : en-têtes de sécurité (et autoriser la console H2 en dev)
            .headers(h -> h.frameOptions(f -> f.sameOrigin()))
            // ATELIER 5 puis 3 : rate limit avant le filtre JWT
            .addFilterBefore(loginRateLimitFilter, UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    /** ATELIER 2 — hachage des mots de passe avec BCrypt. */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /** ATELIER 3 — expose l'AuthenticationManager pour l'utiliser dans AuthService. */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration cfg) throws Exception {
        return cfg.getAuthenticationManager();
    }

    /** ATELIER 5 — origines autorisées (front Angular/React), lues dans application.yml. */
    @Bean
    public CorsConfigurationSource corsSource() {
        CorsConfiguration c = new CorsConfiguration();
        c.setAllowedOrigins(props.getCors().getAllowedOrigins());
        c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        c.setAllowedHeaders(List.of("Authorization", "Content-Type"));
        c.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/**", c);
        return src;
    }
}
