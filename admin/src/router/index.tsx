import { createBrowserRouter, Navigate } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";
import AdminLayout from "@/components/Layout/AdminLayout";
import { getDefaultRoute, hasCapability } from "@/utils/access";
import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import Profile from "@/pages/System/Profile";
import Users from "@/pages/System/Users";
import Settings from "@/pages/System/Settings";
import Logs from "@/pages/System/Logs";
import CompanyInfo from "@/pages/Content/CompanyInfo";
import Resumes from "@/pages/Content/Resumes";
import Jobs from "@/pages/Content/Jobs";
import ImportExport from "@/pages/Data/ImportExport";
import Reports from "@/pages/Research/Reports";
import FactorHubIndex from "@/pages/FactorHub";
import FactorData from "@/pages/FactorHub/Data";
import FactorList from "@/pages/FactorHub/Factors";
import FactorAnalysis from "@/pages/FactorHub/Analysis";
import FactorBacktest from "@/pages/FactorHub/Backtest";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user } = useAuthStore();
  const token = localStorage.getItem("admin_access_token");

  if (!isAuthenticated && !token) {
    return <Navigate to="/login" replace />;
  }

  if (user && !user.can_access_console) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const CapabilityRoute = ({
  children,
  capability,
}: {
  children: React.ReactNode;
  capability: Parameters<typeof hasCapability>[1];
}) => {
  const user = useAuthStore((state) => state.user);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!hasCapability(user, capability)) {
    return <Navigate to={getDefaultRoute(user)} replace />;
  }

  return <>{children}</>;
};

const DefaultRouteRedirect = () => {
  const user = useAuthStore((state) => state.user);
  return <Navigate to={getDefaultRoute(user)} replace />;
};

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <DefaultRouteRedirect />,
      },
      {
        path: "dashboard",
        element: (
          <CapabilityRoute capability="dashboard.view">
            <Dashboard />
          </CapabilityRoute>
        ),
      },
      {
        path: "system/profile",
        element: (
          <CapabilityRoute capability="profile.manage">
            <Profile />
          </CapabilityRoute>
        ),
      },
      {
        path: "system/users",
        element: (
          <CapabilityRoute capability="system.users.manage">
            <Users />
          </CapabilityRoute>
        ),
      },
      {
        path: "system/logs",
        element: (
          <CapabilityRoute capability="logs.view">
            <Logs />
          </CapabilityRoute>
        ),
      },
      {
        path: "system/settings",
        element: (
          <CapabilityRoute capability="system.settings.manage">
            <Settings />
          </CapabilityRoute>
        ),
      },
      {
        path: "content/company-info",
        element: (
          <CapabilityRoute capability="content.manage">
            <CompanyInfo />
          </CapabilityRoute>
        ),
      },
      {
        path: "content/resumes",
        element: (
          <CapabilityRoute capability="content.manage">
            <Resumes />
          </CapabilityRoute>
        ),
      },
      {
        path: "content/jobs",
        element: (
          <CapabilityRoute capability="content.manage">
            <Jobs />
          </CapabilityRoute>
        ),
      },
      {
        path: "data/import-export",
        element: (
          <CapabilityRoute capability="data.import_export.manage">
            <ImportExport />
          </CapabilityRoute>
        ),
      },
      {
        path: "research/reports",
        element: (
          <CapabilityRoute capability="reports.access">
            <Reports />
          </CapabilityRoute>
        ),
      },
      {
        path: "factor-hub",
        children: [
          {
            index: true,
            element: (
              <CapabilityRoute capability="factorhub.manage">
                <FactorHubIndex />
              </CapabilityRoute>
            ),
          },
          {
            path: "data",
            element: (
              <CapabilityRoute capability="factorhub.manage">
                <FactorData />
              </CapabilityRoute>
            ),
          },
          {
            path: "factors",
            element: (
              <CapabilityRoute capability="factorhub.manage">
                <FactorList />
              </CapabilityRoute>
            ),
          },
          {
            path: "analysis",
            element: (
              <CapabilityRoute capability="factorhub.manage">
                <FactorAnalysis />
              </CapabilityRoute>
            ),
          },
          {
            path: "backtest",
            element: (
              <CapabilityRoute capability="factorhub.manage">
                <FactorBacktest />
              </CapabilityRoute>
            ),
          },
        ],
      },
    ],
  },
  {
    path: "*",
    element: <DefaultRouteRedirect />,
  },
]);

export default router;
