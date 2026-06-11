import { Component, OnInit, inject, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../core/api.service';
import { AdminSummary } from '../core/models';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [DecimalPipe],
  template: `
    <div class="container">
      <div class="card">
        <h2 style="color:var(--blue);margin-top:0">Console d'administration</h2>
        <p class="muted">Réservée au rôle <b>admin</b> (endpoint /admin/summary).</p>
        @if (error()) {
          <div class="error">{{ error() }}</div>
        } @else if (summary()) {
          <div style="display:flex;gap:20px">
            <div class="card" style="flex:1;text-align:center;background:var(--light)">
              <div class="muted">Commandes</div>
              <div style="font-size:34px;font-weight:700;color:var(--blue)">{{ summary()!.totalOrders }}</div>
            </div>
            <div class="card" style="flex:1;text-align:center;background:var(--light)">
              <div class="muted">Chiffre d'affaires</div>
              <div style="font-size:34px;font-weight:700;color:var(--green)">{{ summary()!.totalRevenue | number:'1.2-2' }} €</div>
            </div>
          </div>
        }
      </div>
    </div>
  `,
})
export class AdminComponent implements OnInit {
  private api = inject(ApiService);
  summary = signal<AdminSummary | null>(null);
  error = signal('');

  ngOnInit(): void {
    this.api.adminSummary().subscribe({
      next: (s) => this.summary.set(s),
      error: () => this.error.set('Accès refusé ou erreur serveur.'),
    });
  }
}
