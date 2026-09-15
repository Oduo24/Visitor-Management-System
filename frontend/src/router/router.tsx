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
import { VisitDetailPage } from "../pages/visits/VisitDetailPage";
import { PrebookVisitPage } from "../pages/visits/PrebookVisitPage";
import { WalkinVisitPage } from "../pages/visits/WalkinVisitPage";
import { PublicInvitationPage } from "../pages/invitations/PublicInvitationPage";
import { VisitorPassPage } from "../pages/invitations/VisitorPassPage";
import { QrKioskPage } from "../pages/visits/QrKioskPage";
import { SiteListPage } from "../pages/sites/SiteListPage";
import { UserListPage } from "../pages/users/UserListPage";
 
 
export const router =
  createBrowserRouter([
    {
      path: "/login",
      element: <LoginPage />,
    },

    {
      path: "/invitations/:token",
      element: <PublicInvitationPage />,
    },

    {
      path: "/visitor-pass/:token",
      element: <VisitorPassPage />,
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

            {
              path: "/visits/prebook",
              element: (
                <PrebookVisitPage />
              ),
            },
            {
              path: "/visits/walk-in",
              element: (
                <WalkinVisitPage />
              ),
            },
            {
              path: "/visits/:visitId",
              element: (
                <VisitDetailPage />
              ),
            },
            {
              path: "/qr-kiosk",
              element: (
                <QrKioskPage />
              ),
            },
            {
              path: "/sites",
              element: (
                <SiteListPage />
              ),
            },
            {
              path: "/users",
              element: (
                <UserListPage />
              ),
            },
          ],
        },
      ],
    },
  ]);