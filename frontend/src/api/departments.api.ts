import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Department,
} from "../types/access";
 
 
export async function getDepartments():
  Promise<Department[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<Department[]>
    >(
      "/departments"
    );
 
  return response.data.data;
}