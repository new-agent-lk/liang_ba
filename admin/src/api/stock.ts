import request from '@/utils/request';
import { StockData, PaginatedResponse, PageParams, StockStats } from '@/types';

export const getStockData = (params?: PageParams): Promise<PaginatedResponse<StockData>> => {
  return request.get('/admin/stock-data/', { params });
};

export const getStockStats = (): Promise<StockStats> => {
  return request.get('/admin/stock-data/stats/');
};

export const importStockData = (data: FormData): Promise<{ success: number; failed: number; errors: string[] }> => {
  return request.post('/admin/stock-data/import/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const exportStockData = (params?: Record<string, string>): Promise<Blob> => {
  return request.get('/admin/stock-data/export/', {
    params,
    responseType: 'blob',
  });
};

export const deleteStockData = (ids: number[]): Promise<{ deleted: number }> => {
  return request.post('/admin/stock-data/bulk-delete/', { ids });
};

export const syncStockData = (): Promise<{ success: boolean; message: string }> => {
  return request.post('/admin/stock-data/sync/');
};
