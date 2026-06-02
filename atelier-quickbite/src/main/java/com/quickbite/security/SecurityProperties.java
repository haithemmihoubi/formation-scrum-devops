package com.quickbite.security;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.List;

/**
 * Lie les propriétés "quickbite.security.*" du fichier application.yml.
 */
@ConfigurationProperties(prefix = "quickbite.security")
public class SecurityProperties {

    private final Jwt jwt = new Jwt();
    private final Cors cors = new Cors();

    public Jwt getJwt() { return jwt; }
    public Cors getCors() { return cors; }

    public static class Jwt {
        private String secret;
        private long accessTokenMinutes = 15;
        private long refreshTokenDays = 7;

        public String getSecret() { return secret; }
        public void setSecret(String secret) { this.secret = secret; }
        public long getAccessTokenMinutes() { return accessTokenMinutes; }
        public void setAccessTokenMinutes(long v) { this.accessTokenMinutes = v; }
        public long getRefreshTokenDays() { return refreshTokenDays; }
        public void setRefreshTokenDays(long v) { this.refreshTokenDays = v; }
    }

    public static class Cors {
        private List<String> allowedOrigins = List.of();
        public List<String> getAllowedOrigins() { return allowedOrigins; }
        public void setAllowedOrigins(List<String> v) { this.allowedOrigins = v; }
    }
}
