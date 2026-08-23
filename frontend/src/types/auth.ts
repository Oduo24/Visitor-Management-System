export interface AuthUser {
  id: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  permissions?: string[];
}
 
export interface LoginPayload {
  email: string;
  password: string;
}
 
export interface LoginResult {
  access_token: string;
  user?: AuthUser;
}
 
export interface ApiResponse<T> {
  success: boolean;
  data: T;
}