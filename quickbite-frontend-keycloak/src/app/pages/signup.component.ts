import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule, RouterLink],
  template: `
    <div class="container narrow">
      <div class="card">
        <h2 style="color:var(--blue);margin-top:0">Créer un compte</h2>
        <p class="muted">Le compte reçoit le rôle <b>client</b> (via Keycloak).</p>

        <label>Identifiant</label>
        <input [(ngModel)]="username" />
        <div style="height:10px"></div>
        <label>Email</label>
        <input [(ngModel)]="email" type="email" />
        <div style="height:10px"></div>
        <label>Prénom / Nom</label>
        <div style="display:flex;gap:8px"><input [(ngModel)]="firstName" placeholder="Prénom"/><input [(ngModel)]="lastName" placeholder="Nom"/></div>
        <div style="height:10px"></div>
        <label>Mot de passe (min. 6)</label>
        <input type="password" [(ngModel)]="password" (keyup.enter)="submit()" />

        <div style="height:18px"></div>
        <button (click)="submit()" [disabled]="loading() || !valid()" style="width:100%">
          {{ loading() ? 'Création…' : 'Créer mon compte' }}
        </button>
        @if (error()) { <div class="error">{{ error() }}</div> }
        <p class="muted" style="margin-top:16px">Déjà inscrit ? <a routerLink="/login">Se connecter</a></p>
      </div>
    </div>
  `,
})
export class SignupComponent {
  private auth = inject(AuthService);
  private router = inject(Router);
  username = ''; email = ''; firstName = ''; lastName = ''; password = '';
  loading = signal(false);
  error = signal('');

  valid(): boolean {
    return this.username.length > 0 && this.email.includes('@') && this.password.length >= 6;
  }

  submit(): void {
    this.error.set(''); this.loading.set(true);
    this.auth.register({
      username: this.username, email: this.email, password: this.password,
      firstName: this.firstName, lastName: this.lastName,
    }).subscribe({
      next: () => { this.loading.set(false); this.router.navigate(['/orders']); },
      error: (e) => {
        this.loading.set(false);
        this.error.set(e?.status === 409 ? 'Cet utilisateur existe déjà.' : 'Échec de la création du compte.');
      },
    });
  }
}
