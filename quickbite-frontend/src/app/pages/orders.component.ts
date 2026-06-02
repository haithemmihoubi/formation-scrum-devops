import { Component, OnInit, inject, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../core/api.service';
import { AuthService } from '../core/auth.service';
import { Order } from '../core/models';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [FormsModule, DecimalPipe],
  template: `
    <div class="container">
      <div class="card">
        <h2 style="color:var(--blue);margin-top:0">Mes commandes</h2>

        <div style="display:flex;gap:10px;align-items:end;flex-wrap:wrap;margin-bottom:16px">
          <div style="flex:2;min-width:160px">
            <label>Plat</label>
            <input [(ngModel)]="item" placeholder="Ex. Pizza Margherita" />
          </div>
          <div style="flex:1;min-width:100px">
            <label>Prix (€)</label>
            <input type="number" [(ngModel)]="price" />
          </div>
          <button (click)="add()" [disabled]="!item || price <= 0">Ajouter</button>
        </div>

        @if (orders().length === 0) {
          <p class="muted">Aucune commande pour l'instant.</p>
        } @else {
          <table>
            <thead><tr><th>#</th><th>Plat</th><th>Prix</th><th></th></tr></thead>
            <tbody>
              @for (o of orders(); track o.id) {
                <tr>
                  <td>{{ o.id }}</td>
                  <td>{{ o.item }}</td>
                  <td>{{ o.price | number:'1.2-2' }} €</td>
                  <td style="text-align:right">
                    @if (isAdmin) {
                      <button class="secondary" (click)="remove(o.id)">Supprimer</button>
                    }
                  </td>
                </tr>
              }
            </tbody>
          </table>
        }
        @if (error()) { <div class="error">{{ error() }}</div> }
        <p class="muted" style="margin-top:14px">
          La suppression n'est visible/possible que pour un <b>ADMIN</b> (sinon l'API renvoie 403).
        </p>
      </div>
    </div>
  `,
})
export class OrdersComponent implements OnInit {
  private api = inject(ApiService);
  private auth = inject(AuthService);

  orders = signal<Order[]>([]);
  error = signal('');
  item = '';
  price = 0;
  isAdmin = this.auth.isAdmin();

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.api.myOrders().subscribe({
      next: (o) => this.orders.set(o),
      error: () => this.error.set('Impossible de charger les commandes.'),
    });
  }

  add(): void {
    this.error.set('');
    this.api.createOrder(this.item, this.price).subscribe({
      next: () => {
        this.item = '';
        this.price = 0;
        this.load();
      },
      error: () => this.error.set('Création refusée.'),
    });
  }

  remove(id: number): void {
    this.error.set('');
    this.api.deleteOrder(id).subscribe({
      next: () => this.load(),
      error: () => this.error.set('Suppression refusée (403 si non admin).'),
    });
  }
}
