package com.quickbite.config;

import com.quickbite.order.OrderEntity;
import com.quickbite.order.OrderRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Jeu de données de démo (commandes appartenant à l'utilisateur "client"). */
@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner seed(OrderRepository orders) {
        return args -> {
            if (orders.count() == 0) {
                orders.save(new OrderEntity("Pizza Margherita", 9.50, "client"));
                orders.save(new OrderEntity("Burger Veggie", 8.00, "client"));
            }
        };
    }
}
