export interface Role {
  id: string;
  organization_id: string;
 
  name: string;
  code: string;
 
  description: string | null;
  is_active: boolean;
 
  created_at: string;
  updated_at: string;
}
 
 
export interface Department {
  id: string;
  organization_id: string;
 
  name: string;
  code: string;
 
  description: string | null;
  is_active: boolean;
 
  created_at: string;
  updated_at: string;
}
 
 
export interface UserSiteRole {
  id: string;
 
  user_id: string;
  site_id: string;
  role_id: string;
 
  created_at: string;
  updated_at: string;
}
 
 
export interface CreateUserSiteRolePayload {
  user_id: string;
  site_id: string;
  role_id: string;
}