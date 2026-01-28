import request from '@/utils/request';
import { LoginParams, LoginResponse, User } from '@/types';

export const login = (data: LoginParams): Promise<LoginResponse> => {
  return request.post('/admin/auth/login/', data);
};

export const logout = (): Promise<void> => {
  return request.post('/admin/auth/logout/');
};

export const getCurrentUser = (): Promise<User> => {
  return request.get('/admin/auth/me/');
};
