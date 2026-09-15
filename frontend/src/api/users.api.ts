import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  User,
  CreateUserPayload,
  UpdateUserPayload,
} from "../types/user";
 
 
export async function getUsers():
  Promise<User[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<User[]>
    >(
      "/users"
    );
 
  return response.data.data;
}
 
 
export async function getUserById(
  userId: string
): Promise<User> {
 
  const response =
    await apiClient.get<
      ApiResponse<User>
    >(
      `/users/${userId}`
    );
 
  return response.data.data;
}
 
 
export async function createUser(
  payload: CreateUserPayload
): Promise<User> {
 
  const response =
    await apiClient.post<
      ApiResponse<User>
    >(
      "/users",
      payload
    );
 
  return response.data.data;
}
 
 
export async function updateUser(
  userId: string,
  payload: UpdateUserPayload
): Promise<User> {
 
  const response =
    await apiClient.put<
      ApiResponse<User>
    >(
      `/users/${userId}`,
      payload
    );
 
  return response.data.data;
}
 
 
export async function deleteUser(
  userId: string
): Promise<void> {
 
  await apiClient.delete(
    `/users/${userId}`
  );
}