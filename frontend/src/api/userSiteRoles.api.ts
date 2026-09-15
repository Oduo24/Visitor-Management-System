import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  UserSiteRole,
  CreateUserSiteRolePayload,
} from "../types/access";
 
 
export async function getUserSiteRoles():
  Promise<UserSiteRole[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<UserSiteRole[]>
    >(
      "/user-site-roles"
    );
 
  return response.data.data;
}
 
 
export async function createUserSiteRole(
  payload: CreateUserSiteRolePayload
): Promise<UserSiteRole> {
 
  const response =
    await apiClient.post<
      ApiResponse<UserSiteRole>
    >(
      "/user-site-roles",
      payload
    );
 
  return response.data.data;
}
 
 
export async function deleteUserSiteRole(
  assignmentId: string
): Promise<void> {
 
  await apiClient.delete(
    `/user-site-roles/${assignmentId}`
  );
}