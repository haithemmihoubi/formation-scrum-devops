import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet, Router } from '@angular/router';
import { AuthService } from './core/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <header style="background:var(--blue);color:#fff;padding:12px 20px;display:flex;align-items:center;gap:20px">
      <strong style="font-size:18px">🍔 QuickBite <span style="color:var(--yellow)">· Keycloak</span></strong>
      @if (auth.isLoggedIn()) {
        <nav style="display:flex;gap:16px" class="spacer">
          <a routerLink="/orders" style="color:#fff">Commandes</a>
          @if (auth.isAdmin()) { <a routerLink="/admin" style="color:var(--yellow)">Admin</a> }
        </nav>
        <span class="muted" style="color:#cdd6e0">
          {{ auth.user()?.username }}
          @if (auth.isAdmin()) { <span class="badge admin">admin</span> } @else { <span class="badge client">client</span> }
        </span>
        <button class="secondary" (click)="logout()">Déconnexion</button>
      } @else {
        <span class="spacer"></span>
        <span class="muted" style="color:#cdd6e0">Formation — H. Mihoubi</span>
      }
    </header>
    <router-outlet />
  `,
})
export class AppComponent {
  auth = inject(AuthService);
  private router = inject(Router);
  logout(): void { this.auth.logout(); this.router.navigate(['/login']); }
}
