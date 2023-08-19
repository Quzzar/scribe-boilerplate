import { useNavigate } from "react-router-dom";
import { patchRequest, postRequest } from "../../utils/requests";
import ScribeBox from "../common/library/ScribeBox";
import {
  Stack,
  Title,
  Text,
  createStyles,
  rem,
  TextInput,
  Box,
  Button,
  Center,
  LoadingOverlay,
} from "@mantine/core";
import { IconArrowBigRightFilled } from "@tabler/icons-react";
import { useState } from "react";
import { syncLocalStorage } from "../../auth/core";
import { useRecoilState } from "recoil";
import { userDataState } from "../../atoms/userAtoms";

const useStyles = createStyles((theme) => ({
  root: {
    position: "relative",
  },

  input: {
    height: rem(54),
    paddingTop: rem(18),
  },

  label: {
    position: "absolute",
    pointerEvents: "none",
    fontSize: theme.fontSizes.sm,
    paddingLeft: theme.spacing.sm,
    paddingTop: `calc(${theme.spacing.sm} / 2)`,
    zIndex: 1,
  },
}));

export default function SetupPage() {
  const { classes } = useStyles();
  const navigate = useNavigate();

  const [userData, setUserData] = useRecoilState(userDataState);

  const [loading, setLoading] = useState(false);

  const [name, setName] = useState("");
  const [company, setCompany] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [buyer, setBuyer] = useState("");
  const [buyerReason, setBuyerReason] = useState("");
  const [funFacts, setFunFacts] = useState("");

  const complete = async () => {
    setLoading(true);
    // Update user
    const user = await patchRequest(`user/`, {
      name: name,
      role: jobTitle,
      company_name: company,
      what_you_do: jobDescription,
      buys_your_product: buyer,
      why_buy: buyerReason,
      fun_facts: funFacts,
    });
    if (!user) {
      return;
    }
    await syncLocalStorage(setUserData);

    // Create first project
    const project = await postRequest(`project/`, {
      name: "Starter Project",
      description: "",
      template_id: 1,
    });
    // Navigate to project
    if (project) {
      navigate(`/project/${project.id}`);
    }
  };

  return (
    <>
      <LoadingOverlay visible={loading} />
      <Stack>
        <Box>
          <Title color="white" ta="center">
            Personalization Setup
          </Title>
          <Text color="white" fz="sm" ta="center">
            Tell me a bit about your business and what you're selling!
          </Text>
          <Text color="white" fz="sm" fs="italic" ta="center">
            This will be used to create personalized messages.
          </Text>
        </Box>
        <ScribeBox>
          <Stack>
            <TextInput
              label="What's your name?"
              placeholder="Placeholder"
              classNames={classes}
              value={name}
              onChange={(event) => setName(event.currentTarget.value)}
            />

            <TextInput
              label="Your company?"
              placeholder="Placeholder"
              classNames={classes}
              value={company}
              onChange={(event) => setCompany(event.currentTarget.value)}
            />

            <TextInput
              label="What's your job title?"
              placeholder="Placeholder"
              classNames={classes}
              value={jobTitle}
              onChange={(event) => setJobTitle(event.currentTarget.value)}
            />

            <TextInput
              label="What do you do?"
              placeholder="Placeholder"
              classNames={classes}
              value={jobDescription}
              onChange={(event) => setJobDescription(event.currentTarget.value)}
            />

            <TextInput
              label="Who buys your product?"
              placeholder="Placeholder"
              classNames={classes}
              value={buyer}
              onChange={(event) => setBuyer(event.currentTarget.value)}
            />

            <TextInput
              label="Why do they buy it?"
              placeholder="Placeholder"
              classNames={classes}
              value={buyerReason}
              onChange={(event) => setBuyerReason(event.currentTarget.value)}
            />

            <TextInput
              label="3 fun facts that you share with your prospects"
              placeholder="Placeholder"
              classNames={classes}
              value={funFacts}
              onChange={(event) => setFunFacts(event.currentTarget.value)}
            />

            <Center>
              <Button
                variant="outline"
                color="green"
                rightIcon={<IconArrowBigRightFilled size="0.9rem" />}
                onClick={complete}
              >
                Complete Setup
              </Button>
            </Center>
          </Stack>
        </ScribeBox>
      </Stack>
    </>
  );
}
