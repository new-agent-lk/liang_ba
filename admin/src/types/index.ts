// User types
export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  avatar?: string;
  avatar_url?: string;
  is_staff: boolean;
  is_superuser: boolean;
  is_active: boolean;
  date_joined: string;
  last_login?: string;
  profile?: UserProfile;
}

export interface UserProfile {
  phone?: string;
  avatar?: string;
  avatar_url?: string;
  gender?: 'M' | 'F' | 'O';
  birthday?: string;
  department?: string;
  position?: string;
  employee_id?: string;
  address?: string;
  city?: string;
  province?: string;
  postal_code?: string;
  wechat?: string;
  qq?: string;
  linkedin?: string;
  bio?: string;
  notes?: string;
  login_count?: number;
  last_login_ip?: string;
  language?: string;
  timezone_str?: string;
  theme?: 'light' | 'dark' | 'auto';
  email_notifications?: boolean;
  sms_notifications?: boolean;
  push_notifications?: boolean;
  created_at?: string;
  updated_at?: string;
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

// Resume types
export interface Resume {
  id: number;
  user: number;
  user_username?: string;
  name: string;
  phone: string;
  email: string;
  age?: number;
  job_category: string;
  job_category_display?: string;
  expected_salary?: string;
  education: string;
  education_display?: string;
  school?: string;
  major?: string;
  work_experience?: string;
  skills?: string;
  self_introduction?: string;
  resume_file?: string;
  resume_file_url?: string;
  status: 'pending' | 'reviewing' | 'approved' | 'rejected';
  status_display?: string;
  review_notes?: string;
  reviewed_by?: number;
  reviewed_at?: string;
  created_at: string;
  updated_at: string;
}

// Job Position types
export interface JobPosition {
  id: number;
  title: string;
  department: string;
  job_category: string;
  job_category_display?: string;
  location: string;
  salary_min?: string;
  salary_max?: string;
  salary_display?: string;
  description: string;
  requirements: string;
  responsibilities?: string;
  experience?: string;
  education_required?: string;
  education_required_display?: string;
  headcount: number;
  status: 'draft' | 'active' | 'paused' | 'closed';
  status_display?: string;
  sort_order: number;
  publish_date?: string;
  expiry_date?: string;
  created_at: string;
  updated_at: string;
}

// Job category choices
export const JOB_CATEGORY_CHOICES = [
  { value: 'quant_dev', label: '量化开发' },
  { value: 'data_engineer', label: '数据工程师' },
  { value: 'risk_manager', label: '风控专员' },
  { value: 'researcher', label: '研究员' },
  { value: 'it_support', label: 'IT支持' },
  { value: 'other', label: '其他' },
];

// Education choices
export const EDUCATION_CHOICES = [
  { value: 'high_school', label: '高中' },
  { value: 'associate', label: '大专' },
  { value: 'bachelor', label: '本科' },
  { value: 'master', label: '硕士' },
  { value: 'doctor', label: '博士' },
];

// Resume status choices
export const RESUME_STATUS_CHOICES = [
  { value: 'pending', label: '待审核', color: 'orange' },
  { value: 'reviewing', label: '审核中', color: 'blue' },
  { value: 'approved', label: '已通过', color: 'green' },
  { value: 'rejected', label: '已拒绝', color: 'red' },
];

// Job status choices
export const JOB_STATUS_CHOICES = [
  { value: 'draft', label: '草稿', color: 'default' },
  { value: 'active', label: '招聘中', color: 'processing' },
  { value: 'paused', label: '暂停招聘', color: 'warning' },
  { value: 'closed', label: '已关闭', color: 'error' },
];
