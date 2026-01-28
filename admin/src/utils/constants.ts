// 路由常量
export const ROUTES = {
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  // 系统管理
  USERS: '/system/users',
  SETTINGS: '/system/settings',
  // 内容管理
  PRODUCTS: '/content/products',
  NEWS: '/content/news',
  CASES: '/content/cases',
  CAROUSELS: '/content/carousels',
  MESSAGES: '/content/messages',
  // 数据管理
  STOCK_DATA: '/data/stock-data',
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
      { key: '/content/products', icon: 'AppstoreOutlined', label: '产品管理' },
      { key: '/content/news', icon: 'ReadOutlined', label: '新闻管理' },
      { key: '/content/cases', icon: 'FolderOpenOutlined', label: '案例管理' },
      { key: '/content/carousels', icon: 'PictureOutlined', label: '轮播图管理' },
      { key: '/content/messages', icon: 'MessageOutlined', label: '留言管理' },
    ],
  },
  {
    key: 'data',
    icon: 'LineChartOutlined',
    label: '数据管理',
    children: [
      { key: '/data/stock-data', icon: 'StockOutlined', label: '股票数据' },
      { key: '/data/import-export', icon: 'ImportOutlined', label: '导入导出' },
    ],
  },
];

// 分页默认配置
export const DEFAULT_PAGE_SIZE = 10;

export const PAGE_SIZE_OPTIONS = ['10', '20', '50', '100'];
