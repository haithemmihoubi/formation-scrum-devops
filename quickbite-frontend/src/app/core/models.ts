export interface TokenResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
}

export interface CurrentUser {
  username: string;
  roles: string[];
}

export interface Order {
  id: number;
  item: string;
  price: number;
  owner: string;
}

export interface AdminUser {
  id: number;
  username: string;
  roles: string[];
}
