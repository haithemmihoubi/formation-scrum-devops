package com.quickbite.config;

import com.quickbite.order.OrderEntity;
import com.quickbite.order.OrderRepository;
import com.quickbite.user.RoleEntity;
import com.quickbite.user.RoleRepository;
import com.quickbite.user.UserEntity;
import com.quickbite.user.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * ATELIER 2 — jeu de données de démarrage : deux rôles (ADMIN, CLIENT) et
 * deux utilisateurs, avec mots de passe hachés en BCrypt.
 *   admin / admin123   (ROLE_ADMIN)
 *   client / client123 (ROLE_CLIENT)
 */
@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner seed(UserRepository users,
                           RoleRepository roles,
                           OrderRepository orders,
                           PasswordEncoder encoder) {
        return args -> {
            if (users.count() > 0) return;

            RoleEntity admin = roles.save(new RoleEntity("ADMIN"));
            RoleEntity client = roles.save(new RoleEntity("CLIENT"));

            UserEntity a = new UserEntity("admin", encoder.encode("admin123"));
            a.addRole(admin);
            users.save(a);

            UserEntity c = new UserEntity("client", encoder.encode("client123"));
            c.addRole(client);
            users.save(c);

            orders.save(new OrderEntity("Pizza Margherita", 9.50, "client"));
            orders.save(new OrderEntity("Burger Veggie", 8.00, "client"));

            System.out.println(">>> QuickBite : données initialisées (admin/admin123, client/client123)");
        };
    }
}
