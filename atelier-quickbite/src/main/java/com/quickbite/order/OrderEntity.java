package com.quickbite.order;

import jakarta.persistence.*;

/** ATELIER 2 — une commande, appartenant à un utilisateur (par son username). */
@Entity
@Table(name = "orders")
public class OrderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String item;

    @Column(nullable = false)
    private double price;

    @Column(nullable = false)
    private String owner;   // username du propriétaire

    protected OrderEntity() { }

    public OrderEntity(String item, double price, String owner) {
        this.item = item;
        this.price = price;
        this.owner = owner;
    }

    public Long getId() { return id; }
    public String getItem() { return item; }
    public void setItem(String item) { this.item = item; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public String getOwner() { return owner; }
    public void setOwner(String owner) { this.owner = owner; }
}
