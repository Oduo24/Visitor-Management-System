import { apiClient } from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  VisitorLookup,
  CreateVisitorPayload,
} from "../types/lookups";
 
 
export async function createVisitor(
  payload: CreateVisitorPayload
): Promise<VisitorLookup> {
 
  const response = await apiClient.post<
    ApiResponse<VisitorLookup>
  >(
    "/visitors",
    payload
  );
 
  return response.data.data;
}