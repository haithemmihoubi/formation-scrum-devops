// Réponse token de la façade (passe-plat Keycloak : snake_case)
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in?: number;
  token_type?: string;
}

export interface CurrentUser {
  username: string;
  roles: string[];   // ex. ['admin','client'] depuis realm_access.roles
}

export interface Order {
  id: number;
  item: string;
  price: number;
  owner: string;
}

export interface AdminSummary {
  totalOrders: number;
  totalRevenue: number;
}
