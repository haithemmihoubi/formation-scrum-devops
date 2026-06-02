import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { CurrentUser, TokenResponse } from './models';

const ACCESS = 'qb_access';
const REFRESH = 'qb_refresh';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = environment.apiUrl;

  /** Utilisateur courant exposé en signal (réactif pour l'UI). */
  readonly user = signal<CurrentUser | null>(this.decode(this.accessToken));
  readonly isLoggedIn = computed(() => this.user() !== null);
  readonly isAdmin = computed(() => this.user()?.roles.includes('ROLE_ADMIN') ?? false);

  constructor(private http: HttpClient) {}

  get accessToken(): string | null {
    return localStorage.getItem(ACCESS);
  }
  get refreshToken(): string | null {
    return localStorage.getItem(REFRESH);
  }

  login(username: string, password: string): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(`${this.api}/auth/login`, { username, password })
      .pipe(tap((res) => this.store(res)));
  }

  refresh(): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(`${this.api}/auth/refresh`, { refreshToken: this.refreshToken })
      .pipe(tap((res) => this.store(res)));
  }

  logout(): void {
    localStorage.removeItem(ACCESS);
    localStorage.removeItem(REFRESH);
    this.user.set(null);
  }

  hasRole(role: string): boolean {
    return this.user()?.roles.includes(role) ?? false;
  }

  private store(res: TokenResponse): void {
    localStorage.setItem(ACCESS, res.accessToken);
    localStorage.setItem(REFRESH, res.refreshToken);
    this.user.set(this.decode(res.accessToken));
  }

  /** Décode le payload du JWT (lisible, non sensible) pour récupérer username + rôles. */
  private decode(token: string | null): CurrentUser | null {
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return { username: payload.sub, roles: payload.roles ?? [] };
    } catch {
      return null;
    }
  }
}
