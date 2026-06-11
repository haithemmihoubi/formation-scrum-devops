import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AdminSummary, Order } from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private api = environment.apiUrl;
  constructor(private http: HttpClient) {}

  myOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.api}/orders`);
  }
  createOrder(item: string, price: number): Observable<Order> {
    return this.http.post<Order>(`${this.api}/orders`, { item, price });
  }
  deleteOrder(id: number): Observable<void> {
    return this.http.delete<void>(`${this.api}/orders/${id}`);
  }
  adminSummary(): Observable<AdminSummary> {
    return this.http.get<AdminSummary>(`${this.api}/admin/summary`);
  }
}
