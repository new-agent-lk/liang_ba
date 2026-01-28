// User types
export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  phone?: string;
  avatar?: string;
  avatar_url?: string;
  gender?: 'M' | 'F' | 'O';
  birthday?: string;
  department?: string;
  position?: string;
  employee_id?: string;
  is_staff: boolean;
  is_superuser: boolean;
  is_active: boolean;
  date_joined: string;
  last_login?: string;
  created_at?: string;
  updated_at?: string;
  login_count?: number;
  last_login_ip?: string;
  bio?: string;
  notes?: string;
  profile?: UserProfile;
}

export interface UserProfile {
  address?: string;
  city?: string;
  province?: string;
  postal_code?: string;
  wechat?: string;
  qq?: string;
  linkedin?: string;
  language?: string;
  timezone?: string;
  theme?: 'light' | 'dark' | 'auto';
  email_notifications?: boolean;
  sms_notifications?: boolean;
  push_notifications?: boolean;
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

// API Error
export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}
