import {
  createBrowserRouter,
  Navigate,
} from "react-router-dom";
 
import { ProtectedRoute } from "../auth/ProtectedRoute";
 
import { AppLayout } from "../components/layout/AppLayout";
 
import { LoginPage } from "../pages/LoginPage";
 
import { DashboardPage } from "../pages/DashboardPage";
 
import { VisitListPage } from "../pages/visits/VisitListPage";
 
import { VisitorListPage } from "../pages/visitors/VisitorListPage";
 
 
export const router =
  createBrowserRouter([
    {
      path: "/login",
      element: <LoginPage />,
    },
 
    {
      element: (
        <ProtectedRoute />
      ),
 
      children: [
        {
          element: (
            <AppLayout />
          ),
 
          children: [
            {
              index: true,
              element: (
                <Navigate
                  to="/dashboard"
                  replace
                />
              ),
            },
 
            {
              path: "/dashboard",
              element: (
                <DashboardPage />
              ),
            },
 
            {
              path: "/visits",
              element: (
                <VisitListPage />
              ),
            },
 
            {
              path: "/visitors",
              element: (
                <VisitorListPage />
              ),
            },
          ],
        },
      ],
    },
  ]);