import { Stack, TextInput, Button } from "@mantine/core";
import { API_URL } from "../../constants/data";
import { useRecoilState, useRecoilValue } from "recoil";
import { useEffect, useState } from "react";
import EmailSignIn from "../common/EmailSignIn";
import { useLocation, useNavigate, useSearchParams } from "react-router-dom";
import { getRequest, postRequest } from "../../utils/requests";
import { userDataState } from "../../atoms/userAtoms";
import { authorize } from "../../auth/core";

export default function LandingPage() {

  const navigate = useNavigate();
  const [userData, setUserData] = useRecoilState(userDataState);
  const location = useLocation();

  const getParamsFromHash = () => {
    const hashParams = new URLSearchParams(location.hash.slice(1));
    return {
      access_token: hashParams.get('access_token'),
      refresh_token: hashParams.get('refresh_token'),
      expires_in: hashParams.get('expires_in'),
      type: hashParams.get('type'),
    };
  };

  
  useEffect(() => {
    const params = getParamsFromHash();
    (async () => {
      // Handle magic link login
      if(params.type === 'magiclink' && params.access_token && params.refresh_token){
        const result = await postRequest(`user/auth`, {
          access_token: params.access_token,
          refresh_token: params.refresh_token,
          expires_in: params.expires_in,
        });
        if(result){
          await authorize(result.access_token, result.refresh_token, setUserData);
          navigate(`/onboarding`);
        }
        return;
      }

      // If user is already logged in, navigate to project
      const projects = (await getRequest(`project/`)) as Project[] | null;
      if(projects){
        if(projects.length > 0){
          navigate(`/project/${projects[0].id}`);
        }
        return;
      }
    })();
  }, []);


  return (
    <EmailSignIn />
  )

}
