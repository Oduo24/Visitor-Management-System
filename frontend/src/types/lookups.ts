export interface VisitorLookup {
  id: string;
  first_name: string;
  middle_name?: string | null;
  last_name: string;
  email?: string | null;
  phone?: string | null;
}
 
export interface HostLookup {
  id: string;
  first_name: string;
  last_name: string;
  email?: string | null;
}
 
export interface SiteLookup {
  id: string;
  name: string;
  code?: string;
}
 
export interface DestinationLookup {
  id: string;
  name: string;
  code?: string;
}

export interface CreateVisitorPayload {
  first_name: string;
  last_name: string;
 
  email?: string | null;
  phone?: string;
  company?: string | null;
 
  nationality?: string | null;
  id_number?: string | null;
  passport_number?: string | null;
  vehicle_registration?: string | null;
}