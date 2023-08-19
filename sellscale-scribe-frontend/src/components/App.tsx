import { Outlet, useLocation } from "react-router-dom";
import { useState } from "react";
import {
  AppShell,
  Navbar,
  Header,
  Footer,
  Aside,
  Text,
  MediaQuery,
  Burger,
  useMantineTheme,
  ColorSchemeProvider,
  MantineProvider,
  ColorScheme,
} from "@mantine/core";
import { LogoFull } from "./nav/Logo";
import { ModalsProvider } from "@mantine/modals";
import { Notifications } from "@mantine/notifications";
import BackgroundImg from "../assets/bg.jpg";
import ProjectMenu from "./nav/ProjectMenu";

export default function App() {
  const theme = useMantineTheme();
  const [opened, setOpened] = useState(false);

  const colorScheme: ColorScheme = "dark";

  const location = useLocation();
  const activeTab = location.pathname?.split("/")[1].trim();

  const showNav = activeTab !== "" && activeTab !== "setup";

  return (
    <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={() => {}}>
      <MantineProvider
        theme={{
          colorScheme: colorScheme,
          other: {
            primaryHeadingSize: 45,
            fontWeights: {
              bold: 700,
              extraBold: 900,
            },
          },
        }}
        withGlobalStyles
        withNormalizeCSS
      >
        <ModalsProvider
          modals={{}}
          modalProps={{
            closeOnClickOutside: false,
            size: "xl",
          }}
        >
          <Notifications position="top-right" />
          <AppShell
            styles={{
              root: {
                backgroundImage: `url(${BackgroundImg})`,
                backgroundRepeat: "no-repeat",
                backgroundSize: "cover",
              },
            }}
            navbarOffsetBreakpoint="sm"
            asideOffsetBreakpoint="sm"
            navbar={
              <Navbar
                px="md"
                pb="md"
                hiddenBreakpoint="sm"
                hidden={!opened}
                width={{ sm: 200, lg: 300 }}
                sx={{ border: 0, background: 0 }}
              >
                {showNav && <ProjectMenu />}
              </Navbar>
            }
            aside={
              <MediaQuery smallerThan="sm" styles={{ display: "none" }}>
                <Aside
                  p="md"
                  hiddenBreakpoint="sm"
                  width={{ sm: 200, lg: 300 }}
                  sx={{ border: 0, background: 0 }}
                >
                  {/* Aside content */}
                </Aside>
              </MediaQuery>
            }
            footer={
              <Footer height={60} p="md" sx={{ border: 0, background: 0 }}>
                {/* Footer content */}
              </Footer>
            }
            header={
              <Header
                height={{ base: 50, md: 70 }}
                p="md"
                sx={{ border: 0, background: 0 }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    height: "100%",
                  }}
                >
                  {showNav && (
                    <MediaQuery largerThan="sm" styles={{ display: "none" }}>
                      <Burger
                        opened={opened}
                        onClick={() => setOpened((o) => !o)}
                        size="sm"
                        color={theme.colors.gray[1]}
                        mr="xl"
                      />
                    </MediaQuery>
                  )}

                  <LogoFull size={28} />
                </div>
              </Header>
            }
          >
            {/* Outlet is where react-router will render child routes */}
            <Outlet />
          </AppShell>
        </ModalsProvider>
      </MantineProvider>
    </ColorSchemeProvider>
  );
}
