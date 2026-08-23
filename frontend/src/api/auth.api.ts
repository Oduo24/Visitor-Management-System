import { apiClient } from "./client";
 
import type {
  ApiResponse,
  LoginPayload,
  LoginResult,
} from "../types/auth";
 
 
export async function loginRequest(
  payload: LoginPayload
): Promise<LoginResult> {
 
  const response = await apiClient.post<
    ApiResponse<LoginResult>
  >(
    "/auth/login",
    payload
  );
 
  return response.data.data;
}