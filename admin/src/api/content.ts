import request from '@/utils/request';
import { PaginatedResponse, PageParams } from '@/types';

// Company Info API
export const getCompanyInfo = () => {
  return request.get('/api/admin/company-info/');
};

export const updateCompanyInfo = (data: any) => {
  return request.put('/api/admin/company-info/', data);
};
