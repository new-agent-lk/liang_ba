"""
因子分析器
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from .logger import logger
from .helpers import calculate_ic, calculate_ir, calculate_ic_win_rate, format_number


class FactorAnalyzer:
    """因子分析器"""

    def __init__(self):
        self.logger = logger

    def calculate_ic_analysis(self,
                              factor_data: pd.DataFrame,
                              factor_name: str,
                              return_col: str = 'return_1d',
                              method: str = 'spearman',
                              window: int = None) -> Dict:
        """计算IC分析"""
        try:
            if factor_name not in factor_data.columns:
                return {"error": f"因子{factor_name}不存在"}

            if return_col not in factor_data.columns:
                return {"error": f"收益率列{return_col}不存在"}

            # 按日期分组计算IC
            ic_results = []
            dates = factor_data['date'].unique()

            for date in dates:
                date_data = factor_data[factor_data['date'] == date]
                if len(date_data) < 5:
                    continue

                factor_values = date_data[factor_name]
                return_values = date_data[return_col]

                valid_mask = ~(pd.isna(factor_values) | pd.isna(return_values))
                if valid_mask.sum() < 3:
                    continue

                factor_clean = factor_values[valid_mask]
                return_clean = return_values[valid_mask]

                if method == 'spearman':
                    ic, p_value = stats.spearmanr(factor_clean, return_clean)
                elif method == 'pearson':
                    ic, p_value = stats.pearsonr(factor_clean, return_clean)
                else:
                    raise ValueError("method must be 'spearman' or 'pearson'")

                if not np.isnan(ic):
                    ic_results.append({
                        'date': str(date),
                        'ic': ic,
                        'p_value': p_value,
                        'count': valid_mask.sum()
                    })

            if not ic_results:
                return {"error": "没有有效的IC计算结果"}

            ic_df = pd.DataFrame(ic_results)
            ic_series = ic_df['ic']

            ic_mean = ic_series.mean()
            ic_std = ic_series.std()
            ir = calculate_ir(ic_series)
            ic_win_rate = calculate_ic_win_rate(ic_series)
            ic_abs_mean = np.abs(ic_series).mean()

            # 滚动IC分析
            rolling_stats = {}
            if window and len(ic_series) >= window:
                rolling_mean = ic_series.rolling(window).mean()
                rolling_std = ic_series.rolling(window).std()
                rolling_ir = rolling_mean / rolling_std

                rolling_stats = {
                    'rolling_mean_last': rolling_mean.iloc[-1] if len(rolling_mean) > 0 else 0,
                    'rolling_std_last': rolling_std.iloc[-1] if len(rolling_std) > 0 else 0,
                    'rolling_ir_last': rolling_ir.iloc[-1] if len(rolling_ir) > 0 else 0
                }

            t_stat, t_p_value = stats.ttest_1samp(ic_series, 0)

            return {
                'ic_series': ic_df.to_dict('records'),
                'ic_mean': ic_mean,
                'ic_std': ic_std,
                'ir': ir,
                'ic_win_rate': ic_win_rate,
                'ic_abs_mean': ic_abs_mean,
                't_statistic': t_stat,
                't_p_value': t_p_value,
                'sample_count': len(ic_results),
                **rolling_stats
            }

        except Exception as e:
            self.logger.error(f"IC分析失败: {str(e)}")
            return {"error": str(e)}

    def calculate_decile_analysis(self,
                                   factor_data: pd.DataFrame,
                                   factor_name: str,
                                   return_col: str = 'return_1d',
                                   n_deciles: int = 10) -> Dict:
        """计算分层回测分析"""
        try:
            if factor_name not in factor_data.columns:
                return {"error": f"因子{factor_name}不存在"}

            # 移除缺失值
            valid_data = factor_data.dropna(subset=[factor_name, return_col])
            if len(valid_data) < 100:
                return {"error": "数据量不足"}

            # 按日期分层
            decile_returns = []
            decile_counts = []

            for date in valid_data['date'].unique():
                date_data = valid_data[valid_data['date'] == date].copy()
                if len(date_data) < n_deciles:
                    continue

                # 分层
                date_data['decile'] = pd.qcut(
                    date_data[factor_name],
                    q=n_deciles,
                    labels=False,
                    duplicates='drop'
                )

                # 计算每层收益
                for decile in range(n_deciles):
                    decile_data = date_data[date_data['decile'] == decile]
                    if len(decile_data) > 0:
                        mean_return = decile_data[return_col].mean()
                        decile_returns.append({
                            'date': str(date),
                            'decile': decile + 1,
                            'return': mean_return
                        })
                        decile_counts.append({
                            'decile': decile + 1,
                            'count': len(decile_data)
                        })

            if not decile_returns:
                return {"error": "没有有效的分层结果"}

            decile_df = pd.DataFrame(decile_returns)
            counts_df = pd.DataFrame(decile_counts).drop_duplicates('decile')

            # 计算每层平均收益
            avg_returns = decile_df.groupby('decile')['return'].agg(['mean', 'std', 'count'])
            avg_returns.columns = ['mean_return', 'std_return', 'count']

            # 计算多空组合
            long_short = avg_returns.loc[n_deciles] - avg_returns.loc[1]

            # 计算换手率
            turnover_rate = 1.0 / n_deciles

            return {
                'decile_returns': decile_df.to_dict('records'),
                'avg_returns': avg_returns.reset_index().to_dict('records'),
                'long_short_return': long_short['mean_return'],
                'long_short_std': long_short['std_return'],
                'counts': counts_df.to_dict('records'),
                'turnover_rate': turnover_rate
            }

        except Exception as e:
            self.logger.error(f"分层分析失败: {str(e)}")
            return {"error": str(e)}

    def calculate_correlation_matrix(self,
                                      factor_data: pd.DataFrame,
                                      factor_names: List[str]) -> Dict:
        """计算因子相关性矩阵"""
        try:
            # 选择因子列
            cols = ['date', 'symbol'] + factor_names
            available_cols = [c for c in cols if c in factor_data.columns]

            if len(available_cols) < 3:
                return {"error": "因子数量不足"}

            # 计算截面相关性
            valid_data = factor_data[available_cols].dropna()
            if len(valid_data) < 100:
                return {"error": "数据量不足"}

            # 计算相关系数矩阵
            corr_matrix = valid_data[factor_names].corr()

            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'factors': factor_names
            }

        except Exception as e:
            self.logger.error(f"相关性分析失败: {str(e)}")
            return {"error": str(e)}
