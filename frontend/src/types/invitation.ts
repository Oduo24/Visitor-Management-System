export interface InvitationVisitor {
  first_name: string;
  middle_name: string | null;
  last_name: string;
 
  phone: string;
  email: string | null;
 
  id_number: string | null;
  passport_number: string | null;
  vehicle_registration: string | null;
}
 
 
export interface VisitInvitationDetails {
  visit_id: string;
 
  site: string;
  host: string;
 
  visit_type: string;
 
  expected_arrival: string | null;
 
  purpose: string | null;
 
  visitor: InvitationVisitor;
 
  expires_at: string;
}
 
 
export interface VisitInvitationUpdatePayload {
  first_name?: string;
 
  middle_name?: string | null;
 
  last_name?: string;
 
  phone?: string;
 
  email?: string | null;
 
  id_number?: string | null;
 
  passport_number?: string | null;
 
  vehicle_registration?: string | null;
}
 
 
export interface VisitInvitationCompleteResult {
  visit_id: string;
  completed: boolean;
}