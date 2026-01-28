import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import { login as loginApi, logout as logoutApi, getCurrentUser } from '@/api/auth';
import { LoginParams } from '@/types';
import { message } from 'antd';

export const useAuth = () => {
  const navigate = useNavigate();
  const { user, token, isAuthenticated, setUser, setToken, logout: clearAuth } = useAuthStore();

  const login = useCallback(
    async (data: LoginParams) => {
      try {
        const response = await loginApi(data);
        const { token: authToken, user: userData } = response;
        setToken(authToken);
        setUser(userData);
        localStorage.setItem('admin_token', authToken);
        message.success('登录成功');
        navigate('/dashboard');
        return { success: true };
      } catch (error) {
        return { success: false, error };
      }
    },
    [navigate, setToken, setUser]
  );

  const logout = useCallback(async () => {
    try {
      await logoutApi();
    } catch (error) {
      console.error('Logout API failed:', error);
    } finally {
      clearAuth();
      localStorage.removeItem('admin_token');
      navigate('/login');
      message.success('已退出登录');
    }
  }, [clearAuth, navigate]);

  const checkAuth = useCallback(async () => {
    if (token && !user) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        return true;
      } catch (error) {
        clearAuth();
        localStorage.removeItem('admin_token');
        return false;
      }
    }
    return isAuthenticated;
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
