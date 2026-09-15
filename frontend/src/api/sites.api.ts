import {
  apiClient,
} from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  Site,
  CreateSitePayload,
  UpdateSitePayload,
} from "../types/site";
 
 
export async function getSites():
  Promise<Site[]> {
 
  const response =
    await apiClient.get<
      ApiResponse<Site[]>
    >(
      "/sites"
    );
 
  return response.data.data;
}
 
 
export async function getSiteById(
  siteId: string
): Promise<Site> {
 
  const response =
    await apiClient.get<
      ApiResponse<Site>
    >(
      `/sites/${siteId}`
    );
 
  return response.data.data;
}
 
 
export async function createSite(
  payload: CreateSitePayload
): Promise<Site> {
 
  const response =
    await apiClient.post<
      ApiResponse<Site>
    >(
      "/sites",
      payload
    );
 
  return response.data.data;
}
 
 
export async function updateSite(
  siteId: string,
  payload: UpdateSitePayload
): Promise<Site> {
 
  const response =
    await apiClient.put<
      ApiResponse<Site>
    >(
      `/sites/${siteId}`,
      payload
    );
 
  return response.data.data;
}
 
 
export async function deleteSite(
  siteId: string
): Promise<void> {
 
  await apiClient.delete(
    `/sites/${siteId}`
  );
}