import request from '@/utils/request';
import { User, PaginatedResponse, PageParams } from '@/types';

export const getUsers = (params?: PageParams): Promise<PaginatedResponse<User>> => {
  return request.get('/api/admin/users/', { params });
};

export const getUser = (id: number): Promise<User> => {
  return request.get(`/api/admin/users/${id}/`);
};

export const createUser = (data: Partial<User>): Promise<User> => {
  return request.post('/api/admin/users/', data);
};

export const updateUser = (id: number, data: Partial<User>): Promise<User> => {
  return request.put(`/api/admin/users/${id}/`, data);
};

export const deleteUser = (id: number): Promise<void> => {
  return request.delete(`/api/admin/users/${id}/`);
};
