import request from '@/utils/request';
import { ResearchReport, PaginatedResponse, PageParams } from '@/types';

// 检测数据中是否包含新上传的文件（不是已有图片的URL）
const hasNewFiles = (data: any): boolean => {
  if (!data) return false;
  // 检查是否有 originFileObj（表示新上传的文件）
  const checkForNewFiles = (value: any): boolean => {
    if (!value) return false;
    if (Array.isArray(value)) {
      return value.some((item: any) => item?.originFileObj);
    }
    if (value?.originFileObj) return true;
    return false;
  };
  return (
    checkForNewFiles(data.detail_image) ||
    checkForNewFiles(data.equity_curve_image) ||
    checkForNewFiles(data.drawdown_image) ||
    checkForNewFiles(data.monthly_returns_image) ||
    checkForNewFiles(data.attachment)
  );
};

// 将数据转换为 FormData（用于文件上传）
const toFormData = (data: any): FormData => {
  const formData = new FormData();
  Object.keys(data).forEach((key) => {
    const value = data[key];
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        // 只处理新上传的文件（包含 originFileObj 的）
        value.forEach((item: any) => {
          if (item?.originFileObj) {
            formData.append(key, item.originFileObj);
          }
        });
      } else if (value?.originFileObj) {
        // 单个文件对象
        formData.append(key, value.originFileObj);
      }
    }
  });
  return formData;
};

export const getReports = (params?: PageParams): Promise<PaginatedResponse<ResearchReport>> => {
  return request.get('/api/reports/reports/', { params });
};

export const getReport = (id: number): Promise<ResearchReport> => {
  return request.get(`/api/reports/reports/${id}/`);
};

export const createReport = (data: Partial<ResearchReport>): Promise<ResearchReport> => {
  if (hasNewFiles(data)) {
    return request.post('/api/reports/reports/', toFormData(data), {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }
  return request.post('/api/reports/reports/', data);
};

export const updateReport = (id: number, data: Partial<ResearchReport>): Promise<ResearchReport> => {
  if (hasNewFiles(data)) {
    return request.patch(`/api/reports/reports/${id}/`, toFormData(data), {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }
  // 没有新文件时使用 PATCH 请求进行部分更新
  // 如果 detail_image 是 null，保留它用于删除图片
  // 其他文件字段（URL 字符串）需要移除
  const { equity_curve_image, drawdown_image, monthly_returns_image, attachment, ...cleanData } = data;
  return request.patch(`/api/reports/reports/${id}/`, cleanData);
};

export const deleteReport = (id: number): Promise<void> => {
  return request.delete(`/api/reports/reports/${id}/`);
};

export const submitReport = (id: number): Promise<ResearchReport> => {
  return request.post(`/api/reports/reports/${id}/submit/`);
};

export const reviewReport = (id: number, data: { status: string; review_notes?: string }): Promise<ResearchReport> => {
  return request.post(`/api/reports/reports/${id}/review/`, data);
};

export const publishReport = (id: number): Promise<ResearchReport> => {
  return request.post(`/api/reports/reports/${id}/publish/`);
};

export const unpublishReport = (id: number): Promise<ResearchReport> => {
  return request.post(`/api/reports/reports/${id}/unpublish/`);
};

export const updateReportStatus = (id: number, data: { status: string }): Promise<ResearchReport> => {
  return request.patch(`/api/reports/reports/${id}/`, data);
};
