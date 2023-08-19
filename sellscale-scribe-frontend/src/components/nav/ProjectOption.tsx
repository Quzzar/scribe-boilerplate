import { Button } from "@mantine/core";
import { IconSettings } from "@tabler/icons-react";


export function ProjectOption(props: {name: string}) {

  return (
    <Button.Group>
      <Button fullWidth variant="default">{props.name}</Button>
      <Button variant="default"><IconSettings size={'0.9rem'} /></Button>
    </Button.Group>
  );

}

