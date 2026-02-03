"""
AKShare数据获取模块
"""
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import time
import os

from .logger import logger
from .config import CACHE_DIR, DEFAULT_CONFIG
from .helpers import normalize_stock_code, save_to_cache, load_from_cache


class AKShareDataProvider:
    """AKShare数据提供者"""

    def __init__(self):
        self.logger = logger
        self.cache_enabled = True
        self.default_cache_max_age_days = 7

    def clear_cache(self, older_than_days: int = None):
        """清理缓存文件"""
        if older_than_days is None:
            older_than_days = self.default_cache_max_age_days

        if not CACHE_DIR.exists():
            return

        cache_files = list(CACHE_DIR.glob("daily_*.pkl"))
        cleaned_count = 0

        for cache_file in cache_files:
            try:
                file_age_days = (datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)).days
                if file_age_days > older_than_days:
                    cache_file.unlink()
                    cleaned_count += 1
            except Exception as e:
                self.logger.warning(f"删除缓存文件失败 {cache_file.name}: {str(e)}")

        if cleaned_count > 0:
            self.logger.info(f"清理了 {cleaned_count} 个过期缓存文件")

    def get_cache_info(self) -> Dict:
        """获取缓存信息"""
        if not CACHE_DIR.exists():
            return {"total_files": 0, "total_size_mb": 0}

        cache_files = list(CACHE_DIR.glob("daily_*.pkl"))
        total_size = sum(f.stat().st_size for f in cache_files if f.exists())

        return {
            "total_files": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(CACHE_DIR)
        }

    def get_stock_list(self, market: str = "all") -> pd.DataFrame:
        """获取股票列表"""
        try:
            all_stocks = ak.stock_info_a_code_name()

            if market == "all":
                stock_list = all_stocks
            elif market == "SH":
                stock_list = all_stocks[all_stocks['code'].str.startswith('6')]
            elif market == "SZ":
                stock_list = all_stocks[all_stocks['code'].str.startswith(('0', '3'))]
            else:
                raise ValueError(f"不支持的market参数: {market}")

            stock_list = stock_list.copy()
            stock_list['code'] = stock_list['code'].apply(normalize_stock_code)
            stock_list = stock_list.rename(columns={
                'code': 'symbol',
                'name': 'name'
            })

            self.logger.info(f"获取到{len(stock_list)}只{market}股票")
            return stock_list

        except Exception as e:
            self.logger.error(f"获取股票列表失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_pool(self, pool_code: str = "hs300") -> List[str]:
        """获取股票池"""
        try:
            if pool_code == "hs300":
                df = ak.stock_hs300_cons()
            elif pool_code == "zz500":
                df = ak.stock_zz500_cons()
            elif pool_code == "cyb":
                df = ak.stock_cyb_cons()
            else:
                return []

            if '代码' in df.columns:
                symbols = df['代码'].str.replace('.SH', '').str.replace('.SZ', '').tolist()
            else:
                symbols = df.iloc[:, 0].tolist()

            return [normalize_stock_code(s) for s in symbols]

        except Exception as e:
            self.logger.error(f"获取股票池失败: {str(e)}")
            return []

    def get_daily_data(self,
                       symbol: str,
                       start_date: str,
                       end_date: str,
                       adjust: str = "qfq") -> pd.DataFrame:
        """
        获取单只股票历史数据

        Args:
            symbol: 股票代码
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            adjust: 复权类型 qfq(前复权)/hfq(后复权)/None(不复权)
        """
        try:
            symbol = normalize_stock_code(symbol)

            # 检查缓存
            cache_key = f"daily_{symbol}_{start_date}_{end_date}_{adjust}"
            if self.cache_enabled:
                cached_data = load_from_cache(cache_key, str(CACHE_DIR))
                if cached_data is not None:
                    self.logger.debug(f"从缓存加载 {symbol}")
                    return cached_data

            # 转换日期格式
            start_str = start_date.replace('-', '')
            end_str = end_date.replace('-', '')

            # 获取数据
            suffix = ".SZ" if symbol.startswith(('0', '3')) else ".SH"
            full_symbol = symbol + suffix

            if adjust == "qfq":
                df = ak.stock_zh_a_hist(
                    symbol=full_symbol,
                    period="daily",
                    start_date=start_str,
                    end_date=end_str,
                    adjust="qfq"
                )
            elif adjust == "hfq":
                df = ak.stock_zh_a_hist(
                    symbol=full_symbol,
                    period="daily",
                    start_date=start_str,
                    end_date=end_str,
                    adjust="hfq"
                )
            else:
                df = ak.stock_zh_a_hist(
                    symbol=full_symbol,
                    period="daily",
                    start_date=start_str,
                    end_date=end_str,
                    adjust=""
                )

            if df.empty:
                return pd.DataFrame()

            # 标准化列名
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '涨跌幅': 'pct_change',
                '涨跌额': 'change',
                '换手率': 'turnover'
            })

            df['symbol'] = symbol
            df['date'] = pd.to_datetime(df['date'])

            # 计算收益率
            df['return_1d'] = df['close'].pct_change()
            df['return_5d'] = df['close'].pct_change(5)

            # 保存缓存
            if self.cache_enabled:
                save_to_cache(df, cache_key, str(CACHE_DIR))

            self.logger.debug(f"获取 {symbol} {len(df)} 条数据")
            return df

        except Exception as e:
            self.logger.error(f"获取 {symbol} 数据失败: {str(e)}")
            return pd.DataFrame()

    def get_multiple_stocks_data(self,
                                  symbols: List[str],
                                  start_date: str,
                                  end_date: str,
                                  adjust: str = "qfq",
                                  progress_callback=None) -> pd.DataFrame:
        """获取多只股票数据"""
        all_data = []

        for i, symbol in enumerate(symbols):
            try:
                df = self.get_daily_data(symbol, start_date, end_date, adjust)
                if not df.empty:
                    all_data.append(df)

                if progress_callback:
                    progress = (i + 1) / len(symbols)
                    progress_callback(progress, symbol)

            except Exception as e:
                self.logger.warning(f"获取 {symbol} 数据失败: {str(e)}")
                if progress_callback:
                    progress_callback((i + 1) / len(symbols), symbol)

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()

    def get_market_index(self, index_code: str = "000300") -> pd.DataFrame:
        """获取市场指数数据"""
        try:
            if index_code == "000300":
                df = ak.stock_zh_index_daily(symbol="sh000300")
            elif index_code == "000905":
                df = ak.stock_zh_index_daily(symbol="sh000905")
            elif index_code == "000001":
                df = ak.stock_zh_index_daily(symbol="sh000001")
            else:
                return pd.DataFrame()

            df = df.rename(columns={
                'date': 'date',
                'open': 'open',
                'close': 'close',
                'high': 'high',
                'low': 'low',
                'volume': 'volume'
            })

            df['return_1d'] = df['close'].pct_change()
            return df

        except Exception as e:
            self.logger.error(f"获取指数 {index_code} 失败: {str(e)}")
            return pd.DataFrame()

    def get_factor_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """获取技术指标数据"""
        try:
            suffix = ".SZ" if symbol.startswith(('0', '3')) else ".SH"
            full_symbol = symbol + suffix

            df = ak.stock_zh_a_indicator(symbol=full_symbol)
            return df

        except Exception as e:
            self.logger.error(f"获取 {symbol} 指标数据失败: {str(e)}")
            return None
