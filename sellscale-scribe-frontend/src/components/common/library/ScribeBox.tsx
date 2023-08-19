import { Paper } from "@mantine/core";


export default function ScribeBox(props: {children: React.ReactNode}) {
  return (
    <Paper shadow="xs" p="md"
      sx={{
        backgroundColor: '#1A1B1E'+75,// 75% opacity
        backdropFilter: 'blur(4px)', // blur the background
      }}
    >
      {props.children}
    </Paper>
  );
}
