import { API_URL } from "../constants/data";
import { SetterOrUpdater } from "recoil";

export function isLoggedIn(){
  return !!(localStorage.getItem('user-token')
    && localStorage.getItem('user-data'));
}

export function getUserTokens(){
  return {
    accessToken: localStorage.getItem('user-token'),
    refreshToken: localStorage.getItem('refresh-token'),
  }
}

export function login(email: string, setUserData: SetterOrUpdater<any>){

  setUserData({ email: email });
  localStorage.setItem('user-data', JSON.stringify({ email: email }));

}

export async function authorize(accessToken: string, refreshToken: string, setUserData: SetterOrUpdater<any>){

  localStorage.setItem('user-token', accessToken);
  localStorage.setItem('refresh-token', refreshToken);

  const info = await getUserInfo();
  if(!info){ logout(); }

  setUserData(info);
  localStorage.setItem('user-data', JSON.stringify(info));

}

export function logout(noCheck = false){

  const logoutProcess = () => {
    localStorage.removeItem('user-token');
    localStorage.removeItem('refresh-token');
    localStorage.removeItem('user-data');
    window.location.href = '/';
  }

  if(noCheck){
    logoutProcess();
  } else {
    // Check to confirm that the token is invalid
    getUserInfo().then((info) => {
      if(!info){
        logoutProcess();
      }
    });
  }
}

/**
 * Syncs the local storage with the server user data
 * @param userToken 
 * @returns 
 */
export async function syncLocalStorage(setUserData: SetterOrUpdater<any>){
  if(!isLoggedIn()){ return; }

  const info = await getUserInfo();
  if(!info){ logout(); }
  localStorage.setItem('user-data', JSON.stringify(info));
  setUserData(info);

}

export async function getUserInfo() {
  
  const { accessToken, refreshToken } = getUserTokens();
  if(!accessToken || !refreshToken){ return null; }

  const response = await fetch(
    `${API_URL}/user/`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
  if (response.status === 401) {
    return null;
  }
  const res = await response.json();
  if (!res || !res.data) {
    return null;
  }

  return res.data;
}


export async function refreshAuth() {

  const { refreshToken } = getUserTokens();
  if(!refreshToken){ return null; }

  const response = await fetch(
    `${API_URL}/user/refresh_token`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh_token: refreshToken,
      }),
    }
  );
  if (response.status === 401) {
    return null;
  }
  const res = await response.json();
  if (!res || !res.data) {
    return null;
  }

  localStorage.setItem('user-token', res.data.access_token);
  localStorage.setItem('refresh-token', res.data.refresh_token);

}
