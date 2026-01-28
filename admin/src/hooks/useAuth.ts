import { useCallback } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { login as loginApi, logout as logoutApi, getCurrentUser } from '@/api/auth';
import { LoginParams, LoginResponse, User } from '@/types';
import { message } from 'antd';

interface LoginResult {
  success: boolean;
  error?: unknown;
}

interface CheckAuthResult {
  isAuthenticated: boolean;
  user?: User;
}

export const useAuth = () => {
  const { user, token, isAuthenticated, setUser, setToken, logout: clearAuth } = useAuthStore();

  const login = useCallback(
    async (data: LoginParams): Promise<LoginResult> => {
      try {
        const response: LoginResponse = await loginApi(data);
        const { token: authToken, user: userData } = response;
        setToken(authToken);
        setUser(userData);
        localStorage.setItem('admin_token', authToken);
        message.success('登录成功');
        return { success: true };
      } catch (error) {
        return { success: false, error };
      }
    },
    [setToken, setUser]
  );

  const logout = useCallback(async () => {
    try {
      await logoutApi();
    } catch (error) {
      console.error('Logout API failed:', error);
    } finally {
      clearAuth();
      localStorage.removeItem('admin_token');
      window.location.href = '/login';
      message.success('已退出登录');
    }
  }, [clearAuth]);

  const checkAuth = useCallback(async (): Promise<CheckAuthResult> => {
    if (token && !user) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        return { isAuthenticated: true, user: userData };
      } catch (error) {
        clearAuth();
        localStorage.removeItem('admin_token');
        return { isAuthenticated: false };
      }
    }
    return { isAuthenticated, user: user || undefined };
  }, [token, user, isAuthenticated, setUser, clearAuth]);

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  };
};
