import React, { useEffect, useState } from "react";
import { ConfigProvider, Spin } from "antd";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import router from "./router";
import { useAuth } from "@/hooks/useAuth";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

const AppContent: React.FC = () => {
  const { checkAuth } = useAuth();
  const [authChecking, setAuthChecking] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const result = await checkAuth();
      setAuthChecking(false);

      // If not authenticated and not on login page, redirect to login
      if (
        !result.isAuthenticated &&
        !window.location.pathname.includes("/login")
      ) {
        window.location.href = "/login";
      }
    };
    initAuth();
  }, [checkAuth]);

  if (authChecking) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return <RouterProvider router={router} />;
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: "#1677ff",
            borderRadius: 6,
          },
        }}
      >
        <AppContent />
      </ConfigProvider>
    </QueryClientProvider>
  );
};

export default App;
