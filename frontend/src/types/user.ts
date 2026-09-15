export interface User {
  id: string;
 
  organization_id: string;
  department_id: string | null;
 
  first_name: string;
  last_name: string;
  full_name: string;
 
  email: string;
  phone: string | null;
 
  employee_number: string | null;
  job_title: string | null;
 
  profile_photo_url: string | null;
 
  last_login_at: string | null;
 
  is_active: boolean;
 
  created_at: string;
  updated_at: string;
}
 
 
export interface CreateUserPayload {
  organization_id: string;
  department_id?: string | null;
 
  first_name: string;
  last_name: string;
 
  email: string;
  phone?: string | null;
 
  employee_number?: string | null;
  job_title?: string | null;
 
  profile_photo_url?: string | null;
 
  password: string;
 
  is_active?: boolean;
}
 
 
export interface UpdateUserPayload {
  organization_id?: string;
  department_id?: string | null;
 
  first_name?: string;
  last_name?: string;
 
  email?: string;
  phone?: string | null;
 
  employee_number?: string | null;
  job_title?: string | null;
 
  profile_photo_url?: string | null;
 
  password?: string;
 
  is_active?: boolean;
}