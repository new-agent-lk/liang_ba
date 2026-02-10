// 路由常量
export const ROUTES = {
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  // 系统管理
  USERS: "/system/users",
  SETTINGS: "/system/settings",
  LOGS: "/system/logs",
  // 内容管理
  COMPANY_INFO: "/content/company-info",
  RESUMES: "/content/resumes",
  JOBS: "/content/jobs",
  // 数据管理
  IMPORT_EXPORT: "/data/import-export",
  // 研究报告
  REPORTS: "/research/reports",
  // 量化因子
  FACTOR_HUB: "/factor-hub",
  FACTOR_DATA: "/factor-hub/data",
  FACTOR_LIST: "/factor-hub/factors",
  FACTOR_ANALYSIS: "/factor-hub/analysis",
  FACTOR_BACKTEST: "/factor-hub/backtest",
};

// 菜单配置
export const MENU_CONFIG = [
  {
    key: "/dashboard",
    icon: "DashboardOutlined",
    label: "仪表盘",
  },
  {
    key: "system",
    icon: "SettingOutlined",
    label: "系统管理",
    children: [
      { key: "/system/users", icon: "UserOutlined", label: "用户管理" },
      { key: "/system/logs", icon: "FileSearchOutlined", label: "日志管理" },
      { key: "/system/settings", icon: "ToolOutlined", label: "系统设置" },
    ],
  },
  {
    key: "content",
    icon: "FileTextOutlined",
    label: "内容管理",
    children: [
      { key: "/content/company-info", icon: "HomeOutlined", label: "公司信息" },
      { key: "/content/resumes", icon: "FileTextOutlined", label: "简历管理" },
      { key: "/content/jobs", icon: "TeamOutlined", label: "职位管理" },
    ],
  },
  {
    key: "research",
    icon: "ReadOutlined",
    label: "研究报告",
    children: [
      {
        key: "/research/reports",
        icon: "FileSearchOutlined",
        label: "报告管理",
      },
    ],
  },
  {
    key: "data",
    icon: "LineChartOutlined",
    label: "数据管理",
    children: [
      { key: "/data/import-export", icon: "ImportOutlined", label: "导入导出" },
    ],
  },
  {
    key: "factor-hub",
    icon: "StockOutlined",
    label: "量化因子",
    children: [
      { key: "/factor-hub", icon: "HomeOutlined", label: "概览" },
      { key: "/factor-hub/data", icon: "DatabaseOutlined", label: "数据管理" },
      {
        key: "/factor-hub/factors",
        icon: "SettingOutlined",
        label: "因子管理",
      },
      {
        key: "/factor-hub/analysis",
        icon: "LineChartOutlined",
        label: "因子分析",
      },
      {
        key: "/factor-hub/backtest",
        icon: "BarChartOutlined",
        label: "策略回测",
      },
    ],
  },
];

// 分页默认配置
export const DEFAULT_PAGE_SIZE = 10;

export const PAGE_SIZE_OPTIONS = ["10", "20", "50", "100"];
