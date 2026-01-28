import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import AdminLayout from '@/components/Layout/AdminLayout';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import Users from '@/pages/System/Users';
import Settings from '@/pages/System/Settings';
import Products from '@/pages/Content/Products';
import NewsManagement from '@/pages/Content/News';
import Cases from '@/pages/Content/Cases';
import Carousels from '@/pages/Content/Carousels';
import Messages from '@/pages/Content/Messages';
import StockData from '@/pages/Data/StockData';
import ImportExport from '@/pages/Data/ImportExport';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const token = localStorage.getItem('admin_token');

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
        path: 'system/settings',
        element: <Settings />,
      },
      {
        path: 'content/products',
        element: <Products />,
      },
      {
        path: 'content/news',
        element: <NewsManagement />,
      },
      {
        path: 'content/cases',
        element: <Cases />,
      },
      {
        path: 'content/carousels',
        element: <Carousels />,
      },
      {
        path: 'content/messages',
        element: <Messages />,
      },
      {
        path: 'data/stock-data',
        element: <StockData />,
      },
      {
        path: 'data/import-export',
        element: <ImportExport />,
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/dashboard" replace />,
  },
]);

export default router;
