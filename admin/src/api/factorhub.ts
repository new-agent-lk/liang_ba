import request from "@/utils/request";

// 统计信息
export const getStats = () => {
  return request.get(`/api/factorhub/stats/`);
};

// 股票相关
export const getStockList = (market: string = "all") => {
  return request.get(`/api/factorhub/stocks/`, { params: { market } });
};

export const getStockPool = (pool: string = "hs300") => {
  return request.get(`/api/factorhub/stock-pool/`, { params: { pool } });
};

// 数据获取
export const fetchMarketData = (data: {
  symbols?: string[];
  stock_pool?: string;
  start_date: string;
  end_date: string;
  adjust?: string;
}) => {
  return request.post(`/api/factorhub/data/`, data);
};

// 缓存管理
export const getCacheInfo = () => {
  return request.get(`/api/factorhub/cache/`);
};

export const clearCache = () => {
  return request.delete(`/api/factorhub/cache/`);
};

// 因子列表
export const getFactorList = (category?: string) => {
  return request.get(`/api/factorhub/factors/`, { params: { category } });
};

// 因子计算
export const computeFactors = (data: {
  factor_names: string[];
  symbol?: string;
}) => {
  return request.post(`/api/factorhub/factors/compute/`, data);
};

// IC分析
export const analyzeIC = (data: {
  factor_name: string;
  method?: string;
  window?: number;
}) => {
  return request.post(`/api/factorhub/analysis/ic/`, data);
};

// 分层分析
export const analyzeDecile = (data: {
  factor_name: string;
  n_deciles?: number;
}) => {
  return request.post(`/api/factorhub/analysis/decile/`, data);
};

// 回测
export const runBacktest = (data: {
  factor_name: string;
  initial_capital?: number;
  rebalance_freq?: string;
  long_quantile?: number;
  short_quantile?: number;
}) => {
  return request.post(`/api/factorhub/backtest/`, data);
};

// 分析执行
export const executeAnalysis = (data: {
  action: "ic" | "decile" | "backtest";
  [key: string]: any;
}) => {
  return request.post(`/api/factorhub/analysis/execute/`, data);
};
