// User types
export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  is_staff: boolean;
  is_superuser: boolean;
  date_joined: string;
  last_login?: string;
}

export interface LoginParams {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

// Common pagination
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PageParams {
  page?: number;
  page_size?: number;
}

// Dashboard stats
export interface DashboardStats {
  total_users: number;
  total_products: number;
  total_news: number;
  total_cases: number;
  total_messages: number;
  recent_activities: Activity[];
}

export interface Activity {
  id: string;
  type: string;
  content: string;
  created_at: string;
}

// Product types
export interface Product {
  id: number;
  name: string;
  category?: number;
  category_name?: string;
  tag?: number[];
  tag_names?: string[];
  img?: string;
  img_url?: string;
  add_time: string;
  click_nums: number;
  info: string;
}

export interface ProductCategory {
  id: number;
  name: string;
}

// News types
export interface News {
  id: number;
  title: string;
  category: string;
  category_display?: string;
  img?: string;
  img_url?: string;
  add_time: string;
  click_nums: number;
  digest?: string;
  info: string;
  fav_nums: number;
  oppose_nums: number;
}

// Case types
export interface Case {
  id: number;
  title: string;
  category: string;
  category_display?: string;
  img?: string;
  img_url?: string;
  add_time: string;
  click_nums: number;
  digest?: string;
  info: string;
  fav_nums: number;
  oppose_nums: number;
}

// Carousel types
export interface Carousel {
  id: number;
  title: string;
  img?: string;
  img_url?: string;
  link?: string;
}

// Message types
export interface Message {
  id: number;
  name: string;
  phone: string;
  email: string;
  msg: string;
  is_handle: boolean;
  reply?: string;
}

// Stock data types
export interface StockData {
  id: number;
  stock_code: string;
  stock_name: string;
  now_price: number;
  open_price: number;
  close_price: number;
  high_price: number;
  low_price: number;
  turnover_of_shares: number;
  trading_volume: number;
  current_time: string;
}

export interface StockStats {
  total_records: number;
  latest_date: string;
  market_trend: 'up' | 'down' | 'stable';
}

// API Error
export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}
