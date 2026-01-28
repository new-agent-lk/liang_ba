// 路由常量
export const ROUTES = {
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  // 系统管理
  USERS: '/system/users',
  SETTINGS: '/system/settings',
  // 内容管理
  COMPANY_INFO: '/content/company-info',
  MESSAGES: '/content/messages',
  // 数据管理
  IMPORT_EXPORT: '/data/import-export',
};

// 菜单配置
export const MENU_CONFIG = [
  {
    key: '/dashboard',
    icon: 'DashboardOutlined',
    label: '仪表盘',
  },
  {
    key: 'system',
    icon: 'SettingOutlined',
    label: '系统管理',
    children: [
      { key: '/system/users', icon: 'UserOutlined', label: '用户管理' },
      { key: '/system/settings', icon: 'ToolOutlined', label: '系统设置' },
    ],
  },
  {
    key: 'content',
    icon: 'FileTextOutlined',
    label: '内容管理',
    children: [
      { key: '/content/company-info', icon: 'HomeOutlined', label: '公司信息' },
      { key: '/content/messages', icon: 'MessageOutlined', label: '留言管理' },
    ],
  },
  {
    key: 'data',
    icon: 'LineChartOutlined',
    label: '数据管理',
    children: [
      { key: '/data/import-export', icon: 'ImportOutlined', label: '导入导出' },
    ],
  },
];

// 分页默认配置
export const DEFAULT_PAGE_SIZE = 10;

export const PAGE_SIZE_OPTIONS = ['10', '20', '50', '100'];
