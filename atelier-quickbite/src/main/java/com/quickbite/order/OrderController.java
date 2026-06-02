package com.quickbite.order;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

/**
 * ATELIER 2 — endpoints protégés par RBAC.
 *  - lister/créer : tout utilisateur authentifié (il ne voit que SES commandes) ;
 *  - supprimer : réservé au rôle ADMIN.
 */
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderRepository repo;

    public OrderController(OrderRepository repo) {
        this.repo = repo;
    }

    public record CreateOrder(@NotBlank String item, @Positive double price) { }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public List<OrderEntity> myOrders(Authentication auth) {
        return repo.findByOwner(auth.getName());
    }

    @PostMapping
    @PreAuthorize("hasRole('CLIENT') or hasRole('ADMIN')")
    @ResponseStatus(HttpStatus.CREATED)
    public OrderEntity create(@org.springframework.web.bind.annotation.RequestBody CreateOrder body,
                              Authentication auth) {
        return repo.save(new OrderEntity(body.item(), body.price(), auth.getName()));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        if (!repo.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Commande introuvable");
        }
        repo.deleteById(id);
    }
}
