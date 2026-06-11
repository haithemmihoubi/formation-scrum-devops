package com.quickbite.auth;

import jakarta.validation.constraints.NotBlank;

/** ATELIER 3 — objets de transfert (DTO) des endpoints d'authentification. */
public class AuthDtos {

    public record RegisterRequest(
        @NotBlank String username,
        @NotBlank @jakarta.validation.constraints.Size(min = 6) String password) { }

    public record LoginRequest(
        @NotBlank String username,
        @NotBlank String password) { }

    public record RefreshRequest(
        @NotBlank String refreshToken) { }

    public record TokenResponse(
        String accessToken,
        String refreshToken,
        String tokenType) {
        public static TokenResponse of(String access, String refresh) {
            return new TokenResponse(access, refresh, "Bearer");
        }
    }
}
