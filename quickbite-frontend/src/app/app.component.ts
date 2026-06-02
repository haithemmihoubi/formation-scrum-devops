import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet, Router } from '@angular/router';
import { AuthService } from './core/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <header style="background:var(--blue);color:#fff;padding:12px 20px;display:flex;align-items:center;gap:20px">
      <strong style="font-size:18px">🍔 QuickBite</strong>
      @if (auth.isLoggedIn()) {
        <nav style="display:flex;gap:16px;flex:1">
          <a routerLink="/orders" style="color:#fff">Commandes</a>
          @if (auth.isAdmin()) {
            <a routerLink="/admin" style="color:var(--yellow)">Admin</a>
          }
        </nav>
        <span class="muted" style="color:#cdd6e0">
          {{ auth.user()?.username }}
          @if (auth.isAdmin()) { <span class="badge admin">ADMIN</span> }
          @else { <span class="badge client">CLIENT</span> }
        </span>
        <button class="secondary" (click)="logout()">Déconnexion</button>
      } @else {
        <span style="flex:1"></span>
        <span class="muted" style="color:#cdd6e0">Formation — H. Mihoubi</span>
      }
    </header>
    <router-outlet />
  `,
})
export class AppComponent {
  auth = inject(AuthService);
  private router = inject(Router);

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
