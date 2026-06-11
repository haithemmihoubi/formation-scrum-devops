import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth.service';

/**
 * Ajoute le Bearer token. En cas de 401, tente UN refresh puis rejoue la
 * requête ; si le refresh échoue, déconnecte et redirige vers /login.
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const isAuthEndpoint = req.url.includes('/auth/');
  const token = auth.accessToken;
  const authReq = token && !isAuthEndpoint
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401 && !isAuthEndpoint && auth.refreshTokenValue) {
        return auth.refresh().pipe(
          switchMap(() =>
            next(req.clone({ setHeaders: { Authorization: `Bearer ${auth.accessToken}` } }))),
          catchError((e) => {
            auth.logout();
            router.navigate(['/login']);
            return throwError(() => e);
          })
        );
      }
      if (err.status === 401 && !isAuthEndpoint) {
        auth.logout();
        router.navigate(['/login']);
      }
      return throwError(() => err);
    })
  );
};
