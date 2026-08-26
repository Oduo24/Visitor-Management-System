import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  VisitInvitationDetails,
  VisitInvitationUpdatePayload,
  VisitInvitationCompleteResult,
} from "../types/invitation";
 
 
export async function getVisitInvitation(
  token: string
): Promise<VisitInvitationDetails> {
 
  const response = await apiClient.get<
    ApiResponse<VisitInvitationDetails>
  >(
    `/visits/invitations/${
      encodeURIComponent(token)
    }`
  );
 
  return response.data.data;
}
 
 
export async function completeVisitInvitation(
  token: string,
  payload: VisitInvitationUpdatePayload
): Promise<VisitInvitationCompleteResult> {
 
  const response = await apiClient.patch<
    ApiResponse<VisitInvitationCompleteResult>
  >(
    `/visits/invitations/${
      encodeURIComponent(token)
    }`,
    payload
  );
 
  return response.data.data;
}
 
 
export async function createVisitInvitation(
  visitId: string
): Promise<void> {
 
  await apiClient.post(
    `/visits/${visitId}/invitation`
  );
}