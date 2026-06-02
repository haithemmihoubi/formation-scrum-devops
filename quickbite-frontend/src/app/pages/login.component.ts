import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="container" style="max-width:420px">
      <div class="card">
        <h2 style="color:var(--blue);margin-top:0">Connexion à QuickBite</h2>
        <p class="muted">Comptes de démo : <b>admin / admin123</b> · <b>client / client123</b></p>

        <label>Identifiant</label>
        <input [(ngModel)]="username" (keyup.enter)="submit()" autofocus />
        <div style="height:12px"></div>
        <label>Mot de passe</label>
        <input type="password" [(ngModel)]="password" (keyup.enter)="submit()" />

        <div style="height:18px"></div>
        <button (click)="submit()" [disabled]="loading()" style="width:100%">
          {{ loading() ? 'Connexion…' : 'Se connecter' }}
        </button>
        @if (error()) { <div class="error">{{ error() }}</div> }
      </div>
    </div>
  `,
})
export class LoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  username = 'admin';
  password = 'admin123';
  loading = signal(false);
  error = signal('');

  submit(): void {
    this.error.set('');
    this.loading.set(true);
    this.auth.login(this.username, this.password).subscribe({
      next: () => {
        this.loading.set(false);
        this.router.navigate(['/orders']);
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Identifiants invalides.');
      },
    });
  }
}
