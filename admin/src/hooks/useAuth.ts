import { useCallback } from "react";
import { useAuthStore } from "@/store/useAuthStore";
import {
  login as loginApi,
  logout as logoutApi,
  getCurrentUser,
} from "@/api/auth";
import { LoginParams, LoginResponse, User } from "@/types";
import { message } from "antd";

// Token 存储键名
const ACCESS_TOKEN_KEY = "admin_access_token";
const REFRESH_TOKEN_KEY = "admin_refresh_token";

interface LoginResult {
  success: boolean;
  error?: unknown;
}

interface CheckAuthResult {
  isAuthenticated: boolean;
  user?: User;
}

export const useAuth = () => {
  const {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    setUser,
    setTokens,
    logout: clearAuth,
  } = useAuthStore();

  const login = useCallback(
    async (data: LoginParams): Promise<LoginResult> => {
      try {
        const response: LoginResponse = await loginApi(data);
        const { access, refresh, user: userData } = response;

        // 更新 store
        setTokens(access, refresh);
        setUser(userData);

        // 同时存储到 localStorage（用于 request.ts 拦截器）
        localStorage.setItem(ACCESS_TOKEN_KEY, access);
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh);

        message.success("登录成功");
        return { success: true };
      } catch (error) {
        return { success: false, error };
      }
    },
    [setTokens, setUser],
  );

  const logout = useCallback(async () => {
    try {
      await logoutApi();
    } catch (error) {
      console.error("Logout API failed:", error);
    } finally {
      // 清除 store
      clearAuth();

      // 清除 localStorage
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      localStorage.removeItem("admin_user");

      // 跳转登录页
      window.location.href = "/login";
      message.success("已退出登录");
    }
  }, [clearAuth]);

  const checkAuth = useCallback(async (): Promise<CheckAuthResult> => {
    if (accessToken && !user) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        return { isAuthenticated: true, user: userData };
      } catch (error) {
        // Token 无效，清除认证信息
        clearAuth();
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        return { isAuthenticated: false };
      }
    }
    return { isAuthenticated, user: user || undefined };
  }, [accessToken, user, isAuthenticated, setUser, clearAuth]);

  const refreshUserInfo = useCallback(async (): Promise<User | null> => {
    if (!accessToken) {
      return null;
    }

    try {
      const userData = await getCurrentUser();
      setUser(userData);
      return userData;
    } catch (error) {
      console.error("Failed to refresh user info:", error);
      return null;
    }
  }, [accessToken, setUser]);

  return {
    user,
    token: accessToken, // 保持向后兼容
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    logout,
    checkAuth,
    refreshUserInfo,
  };
};
