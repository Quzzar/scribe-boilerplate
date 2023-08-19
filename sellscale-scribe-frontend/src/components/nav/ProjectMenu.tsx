import { Box, Button, Center, LoadingOverlay, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { API_URL } from "../../constants/data";
import { useRecoilValue } from "recoil";
import { getRequest } from "../../utils/requests";
import ScribeBox from "../common/library/ScribeBox";
import { ProjectOption } from "./ProjectOption";
import { IconPlus } from "@tabler/icons-react";

export default function ProjectMenu() {
  const { data, isFetching, refetch } = useQuery({
    queryKey: [`get-all-projects`, {}],
    queryFn: async ({ queryKey }) => {
      // @ts-ignore
      // eslint-disable-next-line
      const [_key, {}] = queryKey;

      const result = await getRequest(`project/`);
      return result as Project[];
    },
    refetchOnWindowFocus: false,
    enabled: true,
  });

  console.log(data);

  return (
    <ScribeBox>
      <Box maw={300} h={"80vh"} sx={{ position: 'relative' }}>
        {data ? (
          <Stack spacing={5}>
          <ScrollArea h={"70vh"}>
            <Stack spacing={8}>
              {data.map((project, index) => (
                <ProjectOption key={index} name={project.name} />
              ))}
            </Stack>
          </ScrollArea>
          <Center>
            <Button leftIcon={<IconPlus size='0.9rem' />} variant="light" color="green" radius="md">
              New Project
            </Button>
          </Center>
          </Stack>
        ) : (
          <LoadingOverlay visible={isFetching} />
        )}
      </Box>
    </ScribeBox>
  );
}
