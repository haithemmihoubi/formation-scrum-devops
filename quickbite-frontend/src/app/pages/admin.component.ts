import { Component, OnInit, inject, signal } from '@angular/core';
import { ApiService } from '../core/api.service';
import { AdminUser } from '../core/models';

@Component({
  selector: 'app-admin',
  standalone: true,
  template: `
    <div class="container">
      <div class="card">
        <h2 style="color:var(--blue);margin-top:0">Console d'administration</h2>
        <p class="muted">Accessible uniquement avec le rôle <b>ADMIN</b> (endpoint /admin/users).</p>

        @if (error()) {
          <div class="error">{{ error() }}</div>
        } @else {
          <table>
            <thead><tr><th>#</th><th>Utilisateur</th><th>Rôles</th></tr></thead>
            <tbody>
              @for (u of users(); track u.id) {
                <tr>
                  <td>{{ u.id }}</td>
                  <td>{{ u.username }}</td>
                  <td>
                    @for (r of u.roles; track r) {
                      <span class="badge" [class.admin]="r === 'ADMIN'" [class.client]="r === 'CLIENT'">{{ r }}</span>
                    }
                  </td>
                </tr>
              }
            </tbody>
          </table>
        }
      </div>
    </div>
  `,
})
export class AdminComponent implements OnInit {
  private api = inject(ApiService);
  users = signal<AdminUser[]>([]);
  error = signal('');

  ngOnInit(): void {
    this.api.adminUsers().subscribe({
      next: (u) => this.users.set(u),
      error: () => this.error.set('Accès refusé ou erreur serveur.'),
    });
  }
}
