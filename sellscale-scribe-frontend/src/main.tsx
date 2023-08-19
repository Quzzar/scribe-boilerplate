import ReactDOM from 'react-dom/client';
import App from './components/App';
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import RestrictedRoute from './auth/RestrictedRoute';
import { RecoilRoot } from 'recoil';
import LandingPage from './components/pages/LandingPage';
import SetupPage from './components/pages/SetupPage';

const queryClient = new QueryClient();

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <></>,
    children: [
      {
        path: "",
        element: <LandingPage />,
      },
      {
        path: "setup",
        element: <RestrictedRoute page={<SetupPage />} />,
      },
      {
        path: "project/:projectId?",
        element: <RestrictedRoute page={<></>} />,
        loader: async ({ params }: { params: any }) => {
          return { projectId: params.projectId };
        },
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <RecoilRoot>
      <RouterProvider router={router} />
    </RecoilRoot>
  </QueryClientProvider>
)
