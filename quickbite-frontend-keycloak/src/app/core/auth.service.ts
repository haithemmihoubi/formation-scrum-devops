import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { CurrentUser, TokenResponse } from './models';

const ACCESS = 'qbkc_access';
const REFRESH = 'qbkc_refresh';

export interface RegisterPayload {
  username: string; email: string; password: string;
  firstName?: string; lastName?: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = environment.apiUrl;

  readonly user = signal<CurrentUser | null>(this.decode(this.accessToken));
  readonly isLoggedIn = computed(() => this.user() !== null);
  readonly isAdmin = computed(() => this.user()?.roles.includes('admin') ?? false);

  constructor(private http: HttpClient) {}

  get accessToken(): string | null { return localStorage.getItem(ACCESS); }
  get refreshTokenValue(): string | null { return localStorage.getItem(REFRESH); }

  /** Signup via la façade (Keycloak Admin API côté backend), puis connexion. */
  register(p: RegisterPayload): Observable<unknown> {
    return new Observable((sub) => {
      this.http.post(`${this.api}/auth/register`, p).subscribe({
        next: () => this.login(p.username, p.password).subscribe({
          next: (r) => { sub.next(r); sub.complete(); },
          error: (e) => sub.error(e),
        }),
        error: (e) => sub.error(e),
      });
    });
  }

  login(username: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.api}/auth/login`, { username, password })
      .pipe(tap((res) => this.store(res)));
  }

  refresh(): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.api}/auth/refresh`, { refreshToken: this.refreshTokenValue })
      .pipe(tap((res) => this.store(res)));
  }

  logout(): void {
    const rt = this.refreshTokenValue;
    if (rt) {
      this.http.post(`${this.api}/auth/logout`, { refreshToken: rt }).subscribe({ error: () => {} });
    }
    localStorage.removeItem(ACCESS);
    localStorage.removeItem(REFRESH);
    this.user.set(null);
  }

  store(res: TokenResponse): void {
    localStorage.setItem(ACCESS, res.access_token);
    localStorage.setItem(REFRESH, res.refresh_token);
    this.user.set(this.decode(res.access_token));
  }

  /** Décode le JWT Keycloak : preferred_username + realm_access.roles. */
  private decode(token: string | null): CurrentUser | null {
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const roles: string[] = payload?.realm_access?.roles ?? [];
      return { username: payload.preferred_username ?? payload.sub, roles };
    } catch {
      return null;
    }
  }
}
