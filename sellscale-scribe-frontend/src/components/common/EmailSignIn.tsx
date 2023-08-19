import { Stack, TextInput, Button, Text } from "@mantine/core";
import { API_URL } from "../../constants/data";
import { useRecoilState, useRecoilValue } from "recoil";
import { useState } from "react";
import { postRequest } from "../../utils/requests";
import { userDataState } from "../../atoms/userAtoms";
import { login } from "../../auth/core";

export default function EmailSignIn() {

  const [userData, setUserData] = useRecoilState(userDataState);
  const [email, setEmail] = useState("");
  const [emailSent, setEmailSent] = useState(false);

  const signIn = async () => {
    const result = await postRequest(`user/signin`, {
      email: email,
    });
    if(result){
      login(email, setUserData);
      setEmailSent(true);
    }
  }

  return (
    <>
      {emailSent ? (
        <Text>Login link has been sent to your email. You may close this tab.</Text>
      ) : (
        <Stack>
          <TextInput
            placeholder="Work email"
            value={email}
            onChange={(event) => setEmail(event.currentTarget.value)}
          />
          <Button onClick={signIn}>
            Sign up
          </Button>
        </Stack>
      )}
    </>
  );

}

