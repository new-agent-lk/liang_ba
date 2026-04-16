import { ConsoleCapability } from "@/types";

// 路由常量
export const ROUTES = {
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  // 系统管理
  PROFILE: "/system/profile",
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
  REPORTS_WRITE: "/research/reports/write",
  REPORTS_MANAGE: "/research/reports/manage",
  // 量化因子
  FACTOR_HUB: "/factor-hub",
  FACTOR_DATA: "/factor-hub/data",
  FACTOR_LIST: "/factor-hub/factors",
  FACTOR_ANALYSIS: "/factor-hub/analysis",
  FACTOR_BACKTEST: "/factor-hub/backtest",
};

interface MenuConfigItem {
  key: string;
  icon?: string;
  label: string;
  requiredCapabilities?: ConsoleCapability[];
  children?: MenuConfigItem[];
}

// 菜单配置
export const MENU_CONFIG: MenuConfigItem[] = [
  {
    key: ROUTES.DASHBOARD,
    icon: "DashboardOutlined",
    label: "仪表盘",
    requiredCapabilities: ["dashboard.view"],
  },
  {
    key: ROUTES.PROFILE,
    icon: "UserOutlined",
    label: "个人中心",
    requiredCapabilities: ["profile.manage"],
  },
  {
    key: "system",
    icon: "SettingOutlined",
    label: "系统管理",
    requiredCapabilities: [
      "system.users.manage",
      "logs.view",
      "system.settings.manage",
    ],
    children: [
      {
        key: ROUTES.USERS,
        icon: "UserOutlined",
        label: "用户管理",
        requiredCapabilities: ["system.users.manage"],
      },
      {
        key: ROUTES.LOGS,
        icon: "FileSearchOutlined",
        label: "日志管理",
        requiredCapabilities: ["logs.view"],
      },
      {
        key: ROUTES.SETTINGS,
        icon: "ToolOutlined",
        label: "系统设置",
        requiredCapabilities: ["system.settings.manage"],
      },
    ],
  },
  {
    key: "content",
    icon: "FileTextOutlined",
    label: "内容管理",
    requiredCapabilities: ["content.manage"],
    children: [
      {
        key: ROUTES.COMPANY_INFO,
        icon: "HomeOutlined",
        label: "公司信息",
        requiredCapabilities: ["content.manage"],
      },
      {
        key: ROUTES.RESUMES,
        icon: "FileTextOutlined",
        label: "简历管理",
        requiredCapabilities: ["content.manage"],
      },
      {
        key: ROUTES.JOBS,
        icon: "TeamOutlined",
        label: "职位管理",
        requiredCapabilities: ["content.manage"],
      },
    ],
  },
  {
    key: "research",
    icon: "ReadOutlined",
    label: "研究报告",
    requiredCapabilities: ["reports.access"],
    children: [
      {
        key: ROUTES.REPORTS_WRITE,
        icon: "FormOutlined",
        label: "报告撰写",
        requiredCapabilities: ["reports.access"],
      },
      {
        key: ROUTES.REPORTS_MANAGE,
        icon: "FileSearchOutlined",
        label: "报告管理",
        requiredCapabilities: ["reports.access"],
      },
    ],
  },
  {
    key: "data",
    icon: "LineChartOutlined",
    label: "数据管理",
    requiredCapabilities: ["data.import_export.manage"],
    children: [
      {
        key: ROUTES.IMPORT_EXPORT,
        icon: "ImportOutlined",
        label: "导入导出",
        requiredCapabilities: ["data.import_export.manage"],
      },
    ],
  },
  {
    key: "factor-hub",
    icon: "StockOutlined",
    label: "量化因子",
    requiredCapabilities: ["factorhub.manage"],
    children: [
      {
        key: ROUTES.FACTOR_HUB,
        icon: "HomeOutlined",
        label: "概览",
        requiredCapabilities: ["factorhub.manage"],
      },
      {
        key: ROUTES.FACTOR_DATA,
        icon: "DatabaseOutlined",
        label: "数据管理",
        requiredCapabilities: ["factorhub.manage"],
      },
      {
        key: ROUTES.FACTOR_LIST,
        icon: "SettingOutlined",
        label: "因子管理",
        requiredCapabilities: ["factorhub.manage"],
      },
      {
        key: ROUTES.FACTOR_ANALYSIS,
        icon: "LineChartOutlined",
        label: "因子分析",
        requiredCapabilities: ["factorhub.manage"],
      },
      {
        key: ROUTES.FACTOR_BACKTEST,
        icon: "BarChartOutlined",
        label: "策略回测",
        requiredCapabilities: ["factorhub.manage"],
      },
    ],
  },
];

// 分页默认配置
export const DEFAULT_PAGE_SIZE = 10;

export const PAGE_SIZE_OPTIONS = ["10", "20", "50", "100"];
