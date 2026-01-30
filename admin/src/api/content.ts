import request from '@/utils/request';
import { Message, PaginatedResponse, PageParams } from '@/types';

// 留言
export const getMessages = (params?: PageParams): Promise<PaginatedResponse<Message>> => {
  return request.get('/api/admin/messages/', { params });
};

export const getMessage = (id: number): Promise<Message> => {
  return request.get(`/api/admin/messages/${id}/`);
};

export const replyMessage = (id: number, reply: string): Promise<Message> => {
  return request.post(`/api/admin/messages/${id}/reply/`, { reply });
};

export const deleteMessage = (id: number): Promise<void> => {
  return request.delete(`/api/admin/messages/${id}/`);
};
