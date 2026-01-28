import request from '@/utils/request';
import { CompanyInfo } from '@/types';

export const getCompanyInfo = (): Promise<CompanyInfo> => {
  return request.get('/api/admin/company-info/');
};

export const updateCompanyInfo = (data: FormData): Promise<CompanyInfo> => {
  return request.put('/api/admin/company-info/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
