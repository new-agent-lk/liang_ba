"""
因子计算引擎
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

from .logger import logger
from .factor_lib import FactorLibrary


class FactorCalculator:
    """因子计算引擎"""

    def __init__(self, max_workers: int = 4):
        self.logger = logger
        self.max_workers = max_workers
        self.factor_library = FactorLibrary()

    def calculate_single_factor(self,
                                data: pd.DataFrame,
                                factor_name: str,
                                groupby_col: str = 'symbol') -> pd.DataFrame:
        """计算单个因子"""
        try:
            result = data.groupby(groupby_col).apply(
                lambda x: self.factor_library.calculate_factor(factor_name, x)
            )

            if isinstance(result, pd.Series):
                result = result.reset_index()
                result.columns = [groupby_col, 'date', factor_name]
            else:
                result = result.reset_index()
                result.columns = [groupby_col, 'date', factor_name]

            return result

        except Exception as e:
            self.logger.error(f"计算因子 {factor_name} 失败: {str(e)}")
            return pd.DataFrame()

    def calculate_factors(self,
                          data: pd.DataFrame,
                          factor_names: List[str],
                          groupby_col: str = 'symbol',
                          parallel: bool = True) -> pd.DataFrame:
        """批量计算因子"""
        if not factor_names:
            return data

        if parallel and len(factor_names) > 1:
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(factor_names))) as executor:
                futures = []
                for factor_name in factor_names:
                    future = executor.submit(
                        self.calculate_single_factor,
                        data.copy(),
                        factor_name,
                        groupby_col
                    )
                    futures.append((factor_name, future))

                results = []
                for factor_name, future in futures:
                    try:
                        result = future.result()
                        if not result.empty:
                            results.append(result)
                    except Exception as e:
                        self.logger.error(f"计算 {factor_name} 失败: {str(e)}")

            if results:
                # 合并结果
                final_result = data.copy()
                for result in results:
                    factor_name = result.columns[-1]
                    final_result = final_result.merge(result, on=[groupby_col, 'date'], how='left')
                return final_result
            return data

        else:
            # 顺序计算
            result = data.copy()
            for factor_name in factor_names:
                factor_data = self.calculate_single_factor(data, factor_name, groupby_col)
                if not factor_data.empty:
                    factor_name_col = factor_data.columns[-1]
                    result = result.merge(factor_data, on=[groupby_col, 'date'], how='left')

            return result

    def calculate_all_technical_factors(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算所有常用技术因子"""
        factors = [
            'ma5', 'ma10', 'ma20', 'ma60',
            'rsi', 'atr',
            'volume_ratio',
            'momentum_1m', 'momentum_3m',
            'roc', 'williams_r'
        ]
        return self.calculate_factors(data, factors)
