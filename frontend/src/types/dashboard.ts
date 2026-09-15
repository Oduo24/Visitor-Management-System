export interface VisitDashboard {
  total_visits: number;
 
  pending_approval: number;
  approved: number;
  checked_in: number;
  checked_out: number;
 
  status_breakdown: Record<
    string,
    number
  >;
 
  visit_type_breakdown: Record<
    string,
    number
  >;
}
 
 
export interface DashboardFilters {
  site_id?: string;
  visit_type?: string;
  start_date?: string;
  end_date?: string;
}