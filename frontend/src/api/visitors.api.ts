import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Visitor,
  CreateVisitorPayload,
  UpdateVisitorPayload,
} from "../types/visitor";
 
 
export async function getVisitors():
  Promise<Visitor[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<Visitor[]>
    >(
      "/visitors"
    );
 
  return response.data.data;
}
 
 
export async function getVisitorById(
  visitorId: string
): Promise<Visitor> {
 
  const response =
    await apiClient.get<
      ApiResponse<Visitor>
    >(
      `/visitors/${visitorId}`
    );
 
  return response.data.data;
}
 
 
export async function createVisitor(
  payload: CreateVisitorPayload
): Promise<Visitor> {
 
  const response =
    await apiClient.post<
      ApiResponse<Visitor>
    >(
      "/visitors",
      payload
    );
 
  return response.data.data;
}
 
 
export async function updateVisitor(
  visitorId: string,
  payload: UpdateVisitorPayload
): Promise<Visitor> {
 
  const response =
    await apiClient.put<
      ApiResponse<Visitor>
    >(
      `/visitors/${visitorId}`,
      payload
    );
 
  return response.data.data;
}
 
 
export async function deleteVisitor(
  visitorId: string
): Promise<void> {
 
  await apiClient.delete(
    `/visitors/${visitorId}`
  );
}