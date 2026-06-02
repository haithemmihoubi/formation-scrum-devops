package com.quickbite.admin;

import com.quickbite.order.OrderRepository;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * Console d'administration : réservée au rôle Keycloak "admin"
 * (verrou URL /admin/** + @PreAuthorize, défense en profondeur).
 */
@RestController
@RequestMapping("/admin")
@PreAuthorize("hasRole('admin')")
public class AdminController {

    private final OrderRepository orders;
    public AdminController(OrderRepository orders) { this.orders = orders; }

    @GetMapping("/summary")
    public Map<String, Object> summary() {
        return Map.of(
            "totalOrders", orders.count(),
            "totalRevenue", orders.findAll().stream().mapToDouble(o -> o.getPrice()).sum()
        );
    }
}
