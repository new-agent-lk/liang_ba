import request from '@/utils/request';

// 股票相关
export const getStockList = (market: string = 'all') => {
  return request.get(`/factorhub/stocks/`, { params: { market } });
};

export const getStockPool = (pool: string = 'hs300') => {
  return request.get(`/factorhub/stock-pool/`, { params: { pool } });
};

// 数据获取
export const fetchMarketData = (data: {
  symbols?: string[];
  stock_pool?: string;
  start_date: string;
  end_date: string;
  adjust?: string;
}) => {
  return request.post(`/factorhub/data/`, data);
};

// 缓存管理
export const getCacheInfo = () => {
  return request.get(`/factorhub/cache/`);
};

export const clearCache = () => {
  return request.delete(`/factorhub/cache/`);
};

// 因子列表
export const getFactorList = (category?: string) => {
  return request.get(`/factorhub/factors/`, { params: { category } });
};

// 因子计算
export const computeFactors = (data: {
  factor_names: string[];
  symbol?: string;
}) => {
  return request.post(`/factorhub/factors/compute/`, data);
};

// IC分析
export const analyzeIC = (data: {
  factor_name: string;
  method?: string;
  window?: number;
}) => {
  return request.post(`/factorhub/analysis/ic/`, data);
};

// 分层分析
export const analyzeDecile = (data: {
  factor_name: string;
  n_deciles?: number;
}) => {
  return request.post(`/factorhub/analysis/decile/`, data);
};

// 回测
export const runBacktest = (data: {
  factor_name: string;
  initial_capital?: number;
  rebalance_freq?: string;
  long_quantile?: number;
  short_quantile?: number;
}) => {
  return request.post(`/factorhub/backtest/`, data);
};

// 分析执行
export const executeAnalysis = (data: {
  action: 'ic' | 'decile' | 'backtest';
  [key: string]: any;
}) => {
  return request.post(`/factorhub/analysis/execute/`, data);
};
