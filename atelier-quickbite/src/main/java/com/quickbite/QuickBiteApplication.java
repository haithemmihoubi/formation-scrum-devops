package com.quickbite;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Point d'entrée de l'API QuickBite — projet fil rouge de la formation.
 * On démarre l'application avec : mvn spring-boot:run
 */
@SpringBootApplication
public class QuickBiteApplication {

    public static void main(String[] args) {
        SpringApplication.run(QuickBiteApplication.class, args);
    }
}
