package com.quickbite.auth;

import org.springframework.boot.context.properties.ConfigurationProperties;

/** Paramètres de connexion à Keycloak (préfixe "keycloak" dans application.yml). */
@ConfigurationProperties(prefix = "keycloak")
public class KeycloakProps {
    private String baseUrl;
    private String realm;
    private String publicClientId;
    private String backendClientId;
    private String backendClientSecret;
    private String defaultRole = "client";

    public String tokenUrl() {
        return baseUrl + "/realms/" + realm + "/protocol/openid-connect/token";
    }
    public String logoutUrl() {
        return baseUrl + "/realms/" + realm + "/protocol/openid-connect/logout";
    }
    public String adminUsersUrl() {
        return baseUrl + "/admin/realms/" + realm + "/users";
    }
    public String adminRoleUrl(String role) {
        return baseUrl + "/admin/realms/" + realm + "/roles/" + role;
    }

    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String v) { this.baseUrl = v; }
    public String getRealm() { return realm; }
    public void setRealm(String v) { this.realm = v; }
    public String getPublicClientId() { return publicClientId; }
    public void setPublicClientId(String v) { this.publicClientId = v; }
    public String getBackendClientId() { return backendClientId; }
    public void setBackendClientId(String v) { this.backendClientId = v; }
    public String getBackendClientSecret() { return backendClientSecret; }
    public void setBackendClientSecret(String v) { this.backendClientSecret = v; }
    public String getDefaultRole() { return defaultRole; }
    public void setDefaultRole(String v) { this.defaultRole = v; }
}
