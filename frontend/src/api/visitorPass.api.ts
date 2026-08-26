import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  VisitorPass,
} from "../types/visitorPass";
 
 
export async function getVisitorPass(
  token: string
): Promise<VisitorPass> {
 
  const response =
    await apiClient.get<
      ApiResponse<VisitorPass>
    >(
      `/visits/access-pass/${
        encodeURIComponent(
          token
        )
      }`
    );
 
  return response.data.data;
}