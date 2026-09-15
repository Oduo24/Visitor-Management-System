export interface Organization {
  id: string;
 
  name: string;
  code: string;
 
  email: string | null;
  phone: string | null;
  website: string | null;
  logo_url: string | null;
  description: string | null;
 
  is_active: boolean;
 
  created_at: string;
  updated_at: string;
}