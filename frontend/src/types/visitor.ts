export interface Visitor {
  id: string;
 
  first_name: string;
  middle_name: string | null;
  last_name: string;
 
  gender: string | null;
  date_of_birth: string | null;
 
  phone: string;
  email: string | null;
 
  company: string | null;
  address: string | null;
  nationality: string | null;
 
  id_number: string | null;
  passport_number: string | null;
 
  vehicle_registration: string | null;
 
  photo_url: string | null;
 
  is_blacklisted: boolean;
 
  notes: string | null;
 
  created_at?: string;
  updated_at?: string;
}
 
export interface CreateVisitorPayload {
  first_name: string;
  middle_name?: string | null;
  last_name: string;
 
  gender?: "Male" | "Female" | "Other" | null;
 
  date_of_birth?: string | null;
 
  phone: string;
  email?: string | null;
 
  company?: string | null;
  address?: string | null;
  nationality?: string | null;
 
  id_number?: string | null;
  passport_number?: string | null;
 
  vehicle_registration?: string | null;
 
  photo_url?: string | null;
 
  is_blacklisted?: boolean;
 
  notes?: string | null;
}
 
export type UpdateVisitorPayload =
  Partial<CreateVisitorPayload>;