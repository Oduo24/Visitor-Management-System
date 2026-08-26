import { apiClient } from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Visit,
  PrebookVisitPayload,
  WalkinVisitPayload,
  VisitApprovalPayload,
} from "../types/visit";
 
 
export async function getVisits(): Promise<
  Visit[]
> {
 
  const response = await apiClient.get<
    ApiResponse<Visit[]>
  >(
    "/visits"
  );
 
  return response.data.data;
}
 
 
export async function getVisitById(
  visitId: string
): Promise<Visit> {
 
  const response = await apiClient.get<
    ApiResponse<Visit>
  >(
    `/visits/${visitId}`
  );
 
  return response.data.data;
}

export async function createPrebookVisit(
  payload: PrebookVisitPayload
): Promise<Visit> {
 
  const response = await apiClient.post<
    ApiResponse<Visit>
  >(
    "/prebook-visits",
    payload
  );
 
  return response.data.data;
}

export async function createWalkinVisit(
  payload: WalkinVisitPayload
): Promise<Visit> {
 
  const response = await apiClient.post<
    ApiResponse<Visit>
  >(
    "/walkin-visits",
    payload
  );
 
  return response.data.data;
}

export async function updateVisitApproval(
  visitId: string,
  payload: VisitApprovalPayload
): Promise<void> {
 
  await apiClient.patch(
    `/visits/${visitId}/approval`,
    payload
  );
}

export async function issueVisitBadge(
  visitId: string
): Promise<void> {
 
  await apiClient.post(
    `/visits/${visitId}/badge`
  );
}

export async function generateVisitQR(
  visitId: string
): Promise<void> {
 
  await apiClient.post(
    `/visits/${visitId}/qr`
  );
}

export async function checkInVisit(
  visitId: string
): Promise<void> {
 
  await apiClient.post(
    `/visits/${visitId}/check-in`
  );
}

export async function checkOutVisit(
  visitId: string
): Promise<void> {
 
  await apiClient.post(
    `/visits/${visitId}/check-out`
  );
}