import { apiClient } from "./client";
 
import type {
  ApiResponse,
} from "../types/auth";
 
import type {
  VisitorLookup,
  HostLookup,
  SiteLookup,
  DestinationLookup,
} from "../types/lookups";
 
 
export async function getVisitors(): Promise<
  VisitorLookup[]
> {
  const response = await apiClient.get<
    ApiResponse<VisitorLookup[]>
  >("/visitors");
 
  return response.data.data;
}
 
 
export async function getHosts(): Promise<
  HostLookup[]
> {
  const response = await apiClient.get<
    ApiResponse<HostLookup[]>
  >("/hosts");
 
  return response.data.data;
}
 
 
export async function getSites(): Promise<
  SiteLookup[]
> {
  const response = await apiClient.get<
    ApiResponse<SiteLookup[]>
  >("/sites");
 
  return response.data.data;
}
 
 
export async function getDestinations(): Promise<
  DestinationLookup[]
> {
  const response = await apiClient.get<
    ApiResponse<DestinationLookup[]>
  >("/destinations");
 
  return response.data.data;
}