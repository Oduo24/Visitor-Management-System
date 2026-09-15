import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Organization,
} from "../types/organization";
 
 
export async function getOrganizations():
  Promise<Organization[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<Organization[]>
    >(
      "/organizations"
    );
 
  return response.data.data;
}