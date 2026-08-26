export interface VisitorPass {
  visit_id: string;
 
  visitor_name: string;
 
  company: string | null;
 
  vehicle_registration:
    string | null;
 
  visitor_code: string;
 
  host: string;
 
  site: string;
 
  destination: string | null;
 
  visit_type: string;
 
  status: string;
 
  purpose: string | null;
 
  expected_arrival:
    string | null;
 
  expected_departure:
    string | null;
 
  qr_token: string;
 
  pass_generated_at:
    string | null;
}