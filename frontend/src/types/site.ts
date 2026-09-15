export interface Site {
  id: string;
 
  organization_id: string;
 
  name: string;
  code: string;
 
  address: string | null;
  city: string | null;
  country: string | null;
 
  timezone: string;
 
  phone: string | null;
  email: string | null;
 
  is_active: boolean;
 
  created_at: string;
  updated_at: string;
}
 
 
export interface CreateSitePayload {
  organization_id: string;
 
  name: string;
  code: string;
 
  address?: string | null;
  city?: string | null;
  country?: string | null;
 
  timezone?: string;
 
  phone?: string | null;
  email?: string | null;
 
  is_active?: boolean;
}
 
 
export type UpdateSitePayload =
  Partial<CreateSitePayload>;