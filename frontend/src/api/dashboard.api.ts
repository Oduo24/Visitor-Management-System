import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  VisitDashboard,
  DashboardFilters,
} from "../types/dashboard";
 
 
export async function getVisitDashboard(
  filters: DashboardFilters
): Promise<VisitDashboard> {
 
  const params =
    new URLSearchParams();
 
 
  if (filters.site_id) {
    params.set(
      "site_id",
      filters.site_id
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
      ApiResponse<VisitDashboard>
    >(
      `/visits/dashboard${
        query
          ? `?${query}`
          : ""
      }`
    );
 
 
  return response.data.data;
}