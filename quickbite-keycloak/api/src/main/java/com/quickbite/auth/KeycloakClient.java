package com.quickbite.auth;

import com.quickbite.auth.AuthDtos.RegisterRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;
import org.springframework.web.server.ResponseStatusException;

import java.net.URI;
import java.util.List;
import java.util.Map;

/**
 * Façade d'authentification : l'API parle à Keycloak.
 *  - login / refresh / logout : endpoint token OIDC (client public "quickbite")
 *  - register (signup) : Admin API via un service account ("quickbite-backend")
 * Architecture enterprise : aucun mot de passe géré par l'API, provisioning
 * des comptes par l'API d'administration de Keycloak.
 */
@Service
public class KeycloakClient {

    private final KeycloakProps props;
    private final RestClient http = RestClient.create();

    public KeycloakClient(KeycloakProps props) {
        this.props = props;
    }

    // ---------- Login / Refresh / Logout (client public) ----------

    public Map<String, Object> login(String username, String password) {
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("client_id", props.getPublicClientId());
        form.add("grant_type", "password");
        form.add("username", username);
        form.add("password", password);
        return token(form, "Identifiants invalides");
    }

    public Map<String, Object> refresh(String refreshToken) {
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("client_id", props.getPublicClientId());
        form.add("grant_type", "refresh_token");
        form.add("refresh_token", refreshToken);
        return token(form, "Refresh token invalide ou expiré");
    }

    public void logout(String refreshToken) {
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("client_id", props.getPublicClientId());
        form.add("refresh_token", refreshToken);
        try {
            http.post().uri(props.logoutUrl())
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .body(form).retrieve().toBodilessEntity();
        } catch (Exception ignored) { /* logout best-effort */ }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> token(MultiValueMap<String, String> form, String errMsg) {
        try {
            return http.post().uri(props.tokenUrl())
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .body(form).retrieve().body(Map.class);
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, errMsg);
        }
    }

    // ---------- Signup (Admin API via service account) ----------

    public Map<String, Object> register(RegisterRequest req) {
        String adminToken = serviceToken();

        String firstName = (req.firstName() == null || req.firstName().isBlank())
            ? req.username() : req.firstName();
        String lastName = (req.lastName() == null || req.lastName().isBlank())
            ? "User" : req.lastName();

        Map<String, Object> userRep = Map.of(
            "username", req.username(),
            "email", req.email(),
            "firstName", firstName,
            "lastName", lastName,
            "enabled", true,
            "emailVerified", true,
            "requiredActions", List.of(),
            "credentials", List.of(Map.of(
                "type", "password", "value", req.password(), "temporary", false))
        );

        ResponseEntity<Void> created;
        try {
            created = http.post().uri(props.adminUsersUrl())
                .header("Authorization", "Bearer " + adminToken)
                .contentType(MediaType.APPLICATION_JSON)
                .body(userRep).retrieve().toBodilessEntity();
        } catch (org.springframework.web.client.HttpClientErrorException.Conflict c) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Cet utilisateur existe déjà");
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "Échec de création du compte");
        }

        String userId = extractId(created.getHeaders().getLocation());
        assignRealmRole(adminToken, userId, props.getDefaultRole());

        return Map.of("id", userId, "username", req.username(), "role", props.getDefaultRole());
    }

    @SuppressWarnings("unchecked")
    private String serviceToken() {
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("client_id", props.getBackendClientId());
        form.add("client_secret", props.getBackendClientSecret());
        form.add("grant_type", "client_credentials");
        Map<String, Object> resp = http.post().uri(props.tokenUrl())
            .contentType(MediaType.APPLICATION_FORM_URLENCODED)
            .body(form).retrieve().body(Map.class);
        return (String) resp.get("access_token");
    }

    @SuppressWarnings("unchecked")
    private void assignRealmRole(String adminToken, String userId, String roleName) {
        Map<String, Object> role = http.get().uri(props.adminRoleUrl(roleName))
            .header("Authorization", "Bearer " + adminToken)
            .retrieve().body(Map.class);
        http.post().uri(props.adminUsersUrl() + "/" + userId + "/role-mappings/realm")
            .header("Authorization", "Bearer " + adminToken)
            .contentType(MediaType.APPLICATION_JSON)
            .body(List.of(role)).retrieve().toBodilessEntity();
    }

    private String extractId(URI location) {
        if (location == null) throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "Réponse Keycloak invalide");
        String path = location.getPath();
        return path.substring(path.lastIndexOf('/') + 1);
    }
}
