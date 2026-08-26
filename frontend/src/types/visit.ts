export interface Visit {
  id: string;
 
  visitor_id: string;
  visitor_name: string | null;

  host_id: string;
  host_name: string | null;

  destination_id: string;
  destination_name: string | null;

  site_name: string | null;
  site_id: string;
 
  visit_type: string;
  status: string;
 
  purpose: string | null;
 
  expected_arrival: string | null;
  expected_departure: string | null;
 
  checked_in_at: string | null;
  checked_out_at: string | null;
 
  approved_by: string | null;
  approved_at: string | null;

  rejected_by: string | null;
  rejected_at: string | null;

  badge_number: string | null;
 
  visitor_code: string | null;
  visitor_code_generated_at: string | null;
 
  qr_token: string | null;
  qr_generated_at: string | null;
 
  notes: string | null;
 
  created_at: string;
  updated_at: string;
  }

  export interface PrebookVisitPayload {
  visitor_id: string;
  host_id: string;
  destination_id: string;
  site_id: string;
 
  expected_arrival: string;
  expected_departure?: string | null;
 
  purpose?: string | null;
  notes?: string | null;
}

export interface WalkinVisitPayload {
  visitor_id: string;
  host_id: string;
  site_id: string;
  destination_id: string;
 
  purpose?: string;
  notes?: string;
}
export interface VisitApprovalPayload {
  approved: boolean;
  notes?: string;
}