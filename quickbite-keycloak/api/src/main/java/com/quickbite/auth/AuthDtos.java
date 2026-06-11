package com.quickbite.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** DTO des endpoints d'authentification (façade devant Keycloak). */
public class AuthDtos {

    public record RegisterRequest(
        @NotBlank String username,
        @Email @NotBlank String email,
        @NotBlank @Size(min = 6) String password,
        String firstName,
        String lastName) { }

    public record LoginRequest(
        @NotBlank String username,
        @NotBlank String password) { }

    public record RefreshRequest(
        @NotBlank String refreshToken) { }

    public record LogoutRequest(
        @NotBlank String refreshToken) { }
}
