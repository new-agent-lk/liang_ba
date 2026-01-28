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
  total_messages: number;
  total_stock_data: number;
  recent_activities: Activity[];
}

export interface Activity {
  id: string;
  type: string;
  content: string;
  created_at: string;
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
  add_time?: string;
}

// Company Info types
export interface CompanyInfo {
  id: number;
  name: string;
  logo?: string;
  logo_url?: string;
  area?: number | null;
  area_name?: string | null;
  address: string;
  phone: string;
  fax: string;
  postcode: string;
  email: string;
  linkman: string;
  telephone: string;
  digest: string;
  info: string;
  honor: string;
  qrcode?: string;
  qrcode_url?: string;
  weichat: string;
  qq: string;
  record_nums: string;
  topimg?: string;
  topimg_url?: string;
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
