import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Visit,
} from "../types/visit";
 
 
export interface VisitActivityFilters {
  site_id?: string;
  status?: string;
  visit_type?: string;
 
  start_date?: string;
  end_date?: string;
}
 
 
export async function getVisitActivityReport(
  filters: VisitActivityFilters
): Promise<Visit[]> {
 
  const params =
    new URLSearchParams();
 
 
  if (filters.site_id) {
    params.set(
      "site_id",
      filters.site_id
    );
  }
 
  if (filters.status) {
    params.set(
      "status",
      filters.status
    );
  }
 
  if (filters.visit_type) {
    params.set(
      "visit_type",
      filters.visit_type
    );
  }
 
  if (filters.start_date) {
    params.set(
      "start_date",
      filters.start_date
    );
  }
 
  if (filters.end_date) {
    params.set(
      "end_date",
      filters.end_date
    );
  }
 
 
  const query =
    params.toString();
 
 
  const response =
    await apiClient.get<
      ApiResponse<Visit[]>
    >(
      `/visits/reports/activity${
        query
          ? `?${query}`
          : ""
      }`
    );
 
 
  return response.data.data;
}