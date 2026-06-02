package com.quickbite.order;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/** ATELIER 2 — accès aux commandes. */
public interface OrderRepository extends JpaRepository<OrderEntity, Long> {
    List<OrderEntity> findByOwner(String owner);
}
