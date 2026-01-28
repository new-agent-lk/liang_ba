import request from '@/utils/request';
import { Product, ProductCategory, News, Case, Carousel, Message, PaginatedResponse, PageParams } from '@/types';

// 产品分类
export const getProductCategories = (): Promise<ProductCategory[]> => {
  return request.get('/admin/product-categories/');
};

export const createProductCategory = (data: Partial<ProductCategory>): Promise<ProductCategory> => {
  return request.post('/admin/product-categories/', data);
};

// 产品
export const getProducts = (params?: PageParams): Promise<PaginatedResponse<Product>> => {
  return request.get('/admin/products/', { params });
};

export const getProduct = (id: number): Promise<Product> => {
  return request.get(`/admin/products/${id}/`);
};

export const createProduct = (data: FormData): Promise<Product> => {
  return request.post('/admin/products/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const updateProduct = (id: number, data: FormData): Promise<Product> => {
  return request.put(`/admin/products/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteProduct = (id: number): Promise<void> => {
  return request.delete(`/admin/products/${id}/`);
};

// 新闻
export const getNewsList = (params?: PageParams): Promise<PaginatedResponse<News>> => {
  return request.get('/admin/news/', { params });
};

export const getNews = (id: number): Promise<News> => {
  return request.get(`/admin/news/${id}/`);
};

export const createNews = (data: FormData): Promise<News> => {
  return request.post('/admin/news/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const updateNews = (id: number, data: FormData): Promise<News> => {
  return request.put(`/admin/news/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteNews = (id: number): Promise<void> => {
  return request.delete(`/admin/news/${id}/`);
};

// 案例
export const getCases = (params?: PageParams): Promise<PaginatedResponse<Case>> => {
  return request.get('/admin/cases/', { params });
};

export const getCase = (id: number): Promise<Case> => {
  return request.get(`/admin/cases/${id}/`);
};

export const createCase = (data: FormData): Promise<Case> => {
  return request.post('/admin/cases/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const updateCase = (id: number, data: FormData): Promise<Case> => {
  return request.put(`/admin/cases/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteCase = (id: number): Promise<void> => {
  return request.delete(`/admin/cases/${id}/`);
};

// 轮播图
export const getCarousels = (params?: PageParams): Promise<PaginatedResponse<Carousel>> => {
  return request.get('/admin/carousels/', { params });
};

export const getCarousel = (id: number): Promise<Carousel> => {
  return request.get(`/admin/carousels/${id}/`);
};

export const createCarousel = (data: FormData): Promise<Carousel> => {
  return request.post('/admin/carousels/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const updateCarousel = (id: number, data: FormData): Promise<Carousel> => {
  return request.put(`/admin/carousels/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteCarousel = (id: number): Promise<void> => {
  return request.delete(`/admin/carousels/${id}/`);
};

// 留言
export const getMessages = (params?: PageParams): Promise<PaginatedResponse<Message>> => {
  return request.get('/admin/messages/', { params });
};

export const getMessage = (id: number): Promise<Message> => {
  return request.get(`/admin/messages/${id}/`);
};

export const replyMessage = (id: number, reply: string): Promise<Message> => {
  return request.post(`/admin/messages/${id}/reply/`, { reply });
};

export const deleteMessage = (id: number): Promise<void> => {
  return request.delete(`/admin/messages/${id}/`);
};
