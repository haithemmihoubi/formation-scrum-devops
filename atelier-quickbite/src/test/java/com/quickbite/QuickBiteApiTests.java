package com.quickbite;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Tests d'intégration de l'API QuickBite — vérifient automatiquement les
 * scénarios de sécurité enseignés (le pipeline CI exécute ces tests).
 *
 * On se connecte une seule fois par rôle (@BeforeAll) pour rester sous la
 * limite du rate-limiting sur /auth/login.
 */
@SpringBootTest
@AutoConfigureMockMvc
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class QuickBiteApiTests {

    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;

    private String adminToken;
    private String clientToken;

    private String login(String user, String pwd) throws Exception {
        String body = mvc.perform(post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"" + user + "\",\"password\":\"" + pwd + "\"}"))
            .andExpect(status().isOk())
            .andReturn().getResponse().getContentAsString();
        JsonNode node = json.readTree(body);
        return node.get("accessToken").asText();
    }

    @BeforeAll
    void loginOnce() throws Exception {
        adminToken = login("admin", "admin123");
        clientToken = login("client", "client123");
    }

    @Test
    void health_estPublic() throws Exception {
        mvc.perform(get("/health"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    void sansToken_renvoie401() throws Exception {
        mvc.perform(get("/auth/me"))
           .andExpect(status().isUnauthorized());
    }

    @Test
    void me_avecTokenAdmin_renvoie200() throws Exception {
        mvc.perform(get("/auth/me").header("Authorization", "Bearer " + adminToken))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.username").value("admin"));
    }

    @Test
    void adminUsers_avecAdmin_renvoie200() throws Exception {
        mvc.perform(get("/admin/users").header("Authorization", "Bearer " + adminToken))
           .andExpect(status().isOk());
    }

    @Test
    void adminUsers_avecClient_renvoie403() throws Exception {
        mvc.perform(get("/admin/users").header("Authorization", "Bearer " + clientToken))
           .andExpect(status().isForbidden());
    }

    @Test
    void clientPeutCreerUneCommande_renvoie201() throws Exception {
        mvc.perform(post("/orders")
                .header("Authorization", "Bearer " + clientToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"item\":\"Tacos\",\"price\":7.5}"))
           .andExpect(status().isCreated())
           .andExpect(jsonPath("$.owner").value("client"));
    }

    @Test
    void clientNePeutPasSupprimer_renvoie403() throws Exception {
        mvc.perform(delete("/orders/1").header("Authorization", "Bearer " + clientToken))
           .andExpect(status().isForbidden());
    }

    @Test
    void mauvaisMotDePasse_renvoie401() throws Exception {
        mvc.perform(post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"admin\",\"password\":\"WRONG\"}"))
           .andExpect(status().isUnauthorized());
    }
}
