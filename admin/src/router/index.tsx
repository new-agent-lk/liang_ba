import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import AdminLayout from '@/components/Layout/AdminLayout';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import Users from '@/pages/System/Users';
import Settings from '@/pages/System/Settings';
import Logs from '@/pages/System/Logs';
import CompanyInfo from '@/pages/Content/CompanyInfo';
import Resumes from '@/pages/Content/Resumes';
import Jobs from '@/pages/Content/Jobs';
import ImportExport from '@/pages/Data/ImportExport';
import Reports from '@/pages/Research/Reports';
import FactorHubIndex from '@/pages/FactorHub';
import FactorData from '@/pages/FactorHub/Data';
import FactorList from '@/pages/FactorHub/Factors';
import FactorAnalysis from '@/pages/FactorHub/Analysis';
import FactorBacktest from '@/pages/FactorHub/Backtest';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const token = localStorage.getItem('admin_access_token');

  if (!isAuthenticated && !token) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'system/users',
        element: <Users />,
      },
      {
        path: 'system/logs',
        element: <Logs />,
      },
      {
        path: 'system/settings',
        element: <Settings />,
      },
      {
        path: 'content/company-info',
        element: <CompanyInfo />,
      },
      {
        path: 'content/resumes',
        element: <Resumes />,
      },
      {
        path: 'content/jobs',
        element: <Jobs />,
      },
      {
        path: 'data/import-export',
        element: <ImportExport />,
      },
      {
        path: 'research/reports',
        element: <Reports />,
      },
      {
        path: 'factor-hub',
        children: [
          { index: true, element: <FactorHubIndex /> },
          { path: 'data', element: <FactorData /> },
          { path: 'factors', element: <FactorList /> },
          { path: 'analysis', element: <FactorAnalysis /> },
          { path: 'backtest', element: <FactorBacktest /> },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/dashboard" replace />,
  },
]);

export default router;
