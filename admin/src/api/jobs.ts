import request from '@/utils/request';
import { Resume, JobPosition, PaginatedResponse, PageParams, RESUME_STATUS_CHOICES, JOB_STATUS_CHOICES } from '@/types';

// 简历 API
export const getResumes = (params?: PageParams): Promise<PaginatedResponse<Resume>> => {
  return request.get('/admin/resumes/', { params });
};

export const getResume = (id: number): Promise<Resume> => {
  return request.get(`/admin/resumes/${id}/`);
};

export const createResume = (data: Partial<Resume>): Promise<Resume> => {
  return request.post('/admin/resumes/', data);
};

export const updateResume = (id: number, data: Partial<Resume>): Promise<Resume> => {
  return request.put(`/admin/resumes/${id}/`, data);
};

export const deleteResume = (id: number): Promise<void> => {
  return request.delete(`/admin/resumes/${id}/`);
};

export const reviewResume = (id: number, data: { status: string; review_notes?: string }): Promise<Resume> => {
  return request.post(`/admin/resumes/${id}/review/`, data);
};

// 职位 API
export const getJobs = (params?: PageParams): Promise<PaginatedResponse<JobPosition>> => {
  return request.get('/admin/jobs/', { params });
};

export const getJob = (id: number): Promise<JobPosition> => {
  return request.get(`/admin/jobs/${id}/`);
};

export const createJob = (data: Partial<JobPosition>): Promise<JobPosition> => {
  return request.post('/admin/jobs/', data);
};

export const updateJob = (id: number, data: Partial<JobPosition>): Promise<JobPosition> => {
  return request.put(`/admin/jobs/${id}/`, data);
};

export const deleteJob = (id: number): Promise<void> => {
  return request.delete(`/admin/jobs/${id}/`);
};

// 获取选项列表的工具函数
export const getResumeStatusLabel = (value: string): string => {
  const found = RESUME_STATUS_CHOICES.find((item) => item.value === value);
  return found?.label || value;
};

export const getJobStatusLabel = (value: string): string => {
  const found = JOB_STATUS_CHOICES.find((item) => item.value === value);
  return found?.label || value;
};
