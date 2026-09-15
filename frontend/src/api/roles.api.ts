import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Role,
} from "../types/access";
 
 
export async function getRoles():
  Promise<Role[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<Role[]>
    >(
      "/roles"
    );
 
  return response.data.data;
}