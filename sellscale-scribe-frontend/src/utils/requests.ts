import { getUserTokens, refreshAuth } from "../auth/core";
import { API_URL } from "../constants/data";

const MAX_RETRIES = 3;

export async function getRequest(path: string): Promise<Record<string, any> | null> {
  return await internalGetRequest(path, 1);
}

async function internalGetRequest(path: string, count: number): Promise<Record<string, any> | null> {
  
  const { accessToken } = getUserTokens();

  const response = await fetch(
    `${API_URL}/${path}`,
    {
      method: "GET",
      headers: accessToken ? {
        Authorization: `Bearer ${accessToken}`,
      } : {},
    }
  );
  if(response.ok){
    return (await response.json()).data as Record<string, any>;
  } else {

    if(response.status === 401){
      if(count >= MAX_RETRIES) return null;
      await refreshAuth();
      return await internalGetRequest(path, count+1);
    }

    return null;
  }

}


export async function postRequest(path: string, body: Record<string, any>): Promise<Record<string, any> | null> {
  return await internalPostRequest('POST', path, body, 1);
}


export async function patchRequest(path: string, body: Record<string, any>): Promise<Record<string, any> | null> {
  return await internalPostRequest('PATCH', path, body, 1);
}


async function internalPostRequest(method: string, path: string, body: Record<string, any>, count: number): Promise<Record<string, any> | null> {
  
  const { accessToken } = getUserTokens();

  const response = await fetch(
    `${API_URL}/${path}`,
    {
      method: method,
      headers: accessToken ? {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      } : {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );
  if(response.ok){
    return (await response.json()).data as Record<string, any>;
  } else {

    if(response.status === 401){
      if(count >= MAX_RETRIES) return null;
      await refreshAuth();
      return await internalPostRequest(method, path, body, count+1);
    }

    return null;
  }

}
