/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { isLoggedIn } from "./core";

export default function RestrictedRoute(props: { page: React.ReactNode }) {
  const navigate = useNavigate();
  //const userData = useRecoilValue(userDataState);

  useEffect(() => {
    setTimeout(() => {
      if (!isLoggedIn()) {
        //navigateToPage(navigate, "/login");
      }
      // else if(userData && !userData.onboarded){
      //   navigateToPage(navigate, '/onboarding');
      // }
    });
  }, []);

  if (isLoggedIn()) {
    return <>{props.page}</>;
  } else {
    return <></>;
  }
}
