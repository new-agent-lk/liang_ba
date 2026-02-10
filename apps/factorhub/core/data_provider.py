"""
AKShare数据获取模块
"""

from datetime import datetime
from typing import Dict, List, Optional

import akshare as ak
import pandas as pd

from .config import CACHE_DIR
from .helpers import load_from_cache, normalize_stock_code, save_to_cache
from .logger import logger


class AKShareDataProvider:
    """AKShare数据提供者"""

    def __init__(self):
        self.logger = logger
        self.cache_enabled = True
        self.default_cache_max_age_days = 7
        self.max_missing_days = 3  # 最大容忍缺失天数，超过则获取新数据

    def clear_cache(self, older_than_days: int = None):
        """清理缓存文件"""
        if older_than_days is None:
            older_than_days = self.default_cache_max_age_days

        if not CACHE_DIR.exists():
            return

        cache_files = list(CACHE_DIR.glob("daily_*"))  # Files without .pkl extension
        cleaned_count = 0

        for cache_file in cache_files:
            try:
                file_age_days = (
                    datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
                ).days
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

        cache_files = list(CACHE_DIR.glob("daily_*"))  # Files without .pkl extension
        total_size = sum(f.stat().st_size for f in cache_files if f.exists())

        return {
            "total_files": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(CACHE_DIR),
        }

    def get_stock_list(self, market: str = "all") -> pd.DataFrame:
        """获取股票列表"""
        # 模拟数据 - 当akshare不可用时使用
        mock_stocks = [
            {"symbol": "600000", "name": "浦发银行"},
            {"symbol": "600016", "name": "民生银行"},
            {"symbol": "600019", "name": "宝钢股份"},
            {"symbol": "600028", "name": "中国石化"},
            {"symbol": "600030", "name": "中信证券"},
            {"symbol": "600036", "name": "招商银行"},
            {"symbol": "600048", "name": "保利发展"},
            {"symbol": "600050", "name": "中国联通"},
            {"symbol": "600051", "name": "宁波联合"},
            {"symbol": "600060", "name": "海欣股份"},
            {"symbol": "000001", "name": "平安银行"},
            {"symbol": "000002", "name": "万 科Ａ"},
            {"symbol": "000003", "name": "PT金田"},
            {"symbol": "000004", "name": "国华网安"},
            {"symbol": "000005", "name": "世纪星"},
            {"symbol": "300001", "name": "特锐德"},
            {"symbol": "300002", "name": "神州泰岳"},
            {"symbol": "300003", "name": "乐普医疗"},
            {"symbol": "300004", "name": "荃银高科"},
            {"symbol": "300005", "name": "探路者"},
        ]

        try:
            all_stocks = ak.stock_info_a_code_name()

            if market == "all":
                stock_list = all_stocks
            elif market == "SH":
                stock_list = all_stocks[all_stocks["code"].str.startswith("6")]
            elif market == "SZ":
                stock_list = all_stocks[all_stocks["code"].str.startswith(("0", "3"))]
            else:
                raise ValueError(f"不支持的market参数: {market}")

            stock_list = stock_list.copy()
            stock_list["code"] = stock_list["code"].apply(normalize_stock_code)
            stock_list = stock_list.rename(columns={"code": "symbol", "name": "name"})

            self.logger.info(f"获取到{len(stock_list)}只{market}股票")
            return stock_list

        except Exception as e:
            self.logger.warning(f"获取股票列表失败，使用模拟数据: {str(e)}")
            return pd.DataFrame(mock_stocks)

    def get_stock_pool(self, pool_code: str = "hs300") -> List[str]:
        """获取股票池"""
        # 使用固定的股票池数据
        stock_pools = {
            "hs300": [
                "600000",
                "600016",
                "600019",
                "600028",
                "600030",
                "600036",
                "600048",
                "600050",
                "600051",
                "600060",
                "600064",
                "600066",
                "600067",
                "600069",
                "600073",
                "600078",
                "600079",
                "600084",
                "600085",
                "600089",
                "600094",
                "600095",
                "600096",
                "600097",
                "600098",
                "600099",
                "600100",
                "600101",
                "600104",
                "600105",
                "600106",
                "600107",
                "600108",
                "600110",
                "600111",
                "600112",
                "600114",
                "600115",
                "600116",
                "600118",
                "600119",
                "600120",
                "600122",
                "600123",
                "600125",
                "600126",
                "600127",
                "600128",
                "600129",
                "600130",
                "600131",
                "600132",
                "600133",
                "600135",
                "600136",
                "600137",
                "600138",
                "600139",
                "600141",
                "600142",
                "600143",
                "600145",
                "600146",
                "600147",
                "600148",
                "600149",
                "600150",
                "600151",
                "600152",
                "600153",
                "600154",
                "600155",
                "600156",
                "600157",
                "600158",
                "600159",
                "600160",
                "600161",
                "600162",
                "600163",
                "600165",
                "600166",
                "600167",
                "600168",
                "600169",
                "600170",
                "600171",
                "600172",
                "600173",
                "600175",
                "600176",
                "600177",
                "600178",
                "600179",
                "600180",
                "600181",
                "600182",
                "600183",
                "600184",
                "600185",
                "600186",
                "600187",
                "600188",
                "600189",
                "600190",
            ],
            "zz500": [
                "000001",
                "000002",
                "000003",
                "000004",
                "000005",
                "000006",
                "000007",
                "000008",
                "000009",
                "000010",
                "000011",
                "000012",
                "000013",
                "000014",
                "000015",
                "000016",
                "000017",
                "000018",
                "000019",
                "000020",
                "000021",
                "000022",
                "000023",
                "000024",
                "000025",
                "000026",
                "000027",
                "000028",
                "000029",
                "000030",
                "000031",
                "000032",
                "000033",
                "000034",
                "000035",
                "000036",
                "000037",
                "000038",
                "000039",
                "000040",
                "000041",
                "000042",
                "000043",
                "000044",
                "000045",
                "000046",
                "000047",
                "000048",
                "000049",
                "000050",
                "000051",
                "000052",
                "000053",
                "000054",
                "000055",
                "000056",
            ],
            "cyb": [
                "300001",
                "300002",
                "300003",
                "300004",
                "300005",
                "300006",
                "300007",
                "300008",
                "300009",
                "300010",
                "300011",
                "300012",
                "300013",
                "300014",
                "300015",
                "300016",
                "300017",
                "300018",
                "300019",
                "300020",
                "300021",
                "300022",
                "300023",
                "300024",
                "300025",
                "300026",
                "300027",
                "300028",
                "300029",
                "300030",
                "300031",
                "300032",
                "300033",
                "300034",
                "300035",
                "300036",
                "300037",
                "300038",
                "300039",
                "300040",
                "300041",
                "300042",
                "300043",
                "300044",
                "300045",
                "300046",
                "300047",
                "300048",
                "300049",
                "300050",
                "300051",
                "300052",
                "300053",
                "300054",
                "300055",
                "300056",
            ],
        }

        return stock_pools.get(pool_code, stock_pools.get("hs300", []))[:50]

    def get_daily_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        adjust: str = "qfq",
        network_requested: bool = False,
    ) -> pd.DataFrame:
        """
        获取单只股票历史数据

        Args:
            symbol: 股票代码
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            adjust: 复权类型
            network_requested: 是否进行了网络请求（用于控制sleep）
        """
        try:
            symbol = normalize_stock_code(symbol)
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)

            # 查找可用的缓存文件（优先使用完全匹配，否则选择重叠最多的）
            if self.cache_enabled:
                cache_files = list(CACHE_DIR.glob(f"daily_{symbol}_*_{adjust}"))
                cached_df = None
                best_cache_file = None
                best_overlap = 0

                for cache_file in cache_files:
                    try:
                        temp_df = load_from_cache(cache_file.name, str(CACHE_DIR))
                        if temp_df is not None and not temp_df.empty:
                            # 检查缓存日期范围
                            cache_dates = pd.to_datetime(temp_df["date"])
                            cache_start = cache_dates.min()
                            cache_end = cache_dates.max()

                            # 如果缓存完全覆盖请求范围，直接使用
                            if cache_start <= start_dt and cache_end >= end_dt:
                                self.logger.debug(f"使用完全匹配缓存 {symbol}: {cache_file.name}")
                                return temp_df.copy()

                            # 计算与请求范围的重叠
                            overlap_start = max(cache_start, start_dt)
                            overlap_end = min(cache_end, end_dt)
                            overlap_days = (
                                (overlap_end - overlap_start).days + 1
                                if overlap_end >= overlap_start
                                else 0
                            )

                            # 优先选择重叠最多的缓存
                            if overlap_days > best_overlap:
                                best_overlap = overlap_days
                                cached_df = temp_df.copy()
                                best_cache_file = cache_file
                    except Exception as e:
                        self.logger.warning(f"加载缓存文件失败 {cache_file.name}: {str(e)[:50]}")

                # 如果有缓存数据，获取缺失的部分并合并
                if cached_df is not None and not cached_df.empty:
                    cached_dates = pd.to_datetime(cached_df["date"])
                    cache_start = cached_dates.min()
                    cache_end = cached_dates.max()

                    # 计算缺失天数
                    missing_before = (cache_start - start_dt).days if cache_start > start_dt else 0
                    missing_after = (end_dt - cache_end).days if cache_end < end_dt else 0
                    total_missing = missing_before + missing_after

                    # 如果缺失天数在容忍范围内，直接返回缓存数据
                    if total_missing <= self.max_missing_days:
                        self.logger.debug(f"使用缓存 {symbol}: 缺失{total_missing}天，在容忍范围内")
                        result = cached_df[
                            (cached_df["date"] >= start_dt) & (cached_df["date"] <= end_dt)
                        ]
                        return result.copy()

                    # 缺失天数超过容忍范围，需要获取新数据
                    new_data_needed = False
                    fetch_start = start_dt
                    fetch_end = end_dt

                    if cache_start > start_dt:
                        fetch_start = cache_start
                        new_data_needed = True
                    if cache_end < end_dt:
                        fetch_end = cache_end
                        new_data_needed = True

                    if new_data_needed:
                        self.logger.debug(
                            f"缓存部分命中 {symbol}: 缓存[{cache_start.date()}-{cache_end.date()}], 缺失{total_missing}天"
                        )
                        # 获取缺失的数据
                        missing_df = self._fetch_and_process(
                            symbol,
                            fetch_start.strftime("%Y-%m-%d"),
                            fetch_end.strftime("%Y-%m-%d"),
                            adjust,
                        )

                        if not missing_df.empty:
                            # 合并缓存和新数据
                            merged_df = pd.concat([cached_df, missing_df], ignore_index=True)
                            # 去重并按日期排序
                            merged_df = merged_df.drop_duplicates(subset=["symbol", "date"])
                            merged_df["date"] = pd.to_datetime(merged_df["date"])
                            merged_df = merged_df.sort_values("date").reset_index(drop=True)

                            # 更新缓存
                            cache_key = f"daily_{symbol}_{merged_df['date'].min().strftime('%Y-%m-%d')}_{merged_df['date'].max().strftime('%Y-%m-%d')}_{adjust}"
                            save_to_cache(merged_df, cache_key, str(CACHE_DIR))

                            # 返回请求范围内的数据
                            result = merged_df[
                                (merged_df["date"] >= start_dt) & (merged_df["date"] <= end_dt)
                            ]
                            return result
                    else:
                        # 缓存已覆盖全部范围
                        return cached_df.copy()

            # 没有缓存或需要获取新数据
            result = self._fetch_and_process(symbol, start_date, end_date, adjust)
            # 标记进行了网络请求
            if result is not None and not result.empty:
                result.attrs["network_requested"] = True
            return result

        except Exception as e:
            self.logger.error(f"获取 {symbol} 数据失败: {str(e)}")
            return pd.DataFrame()

    def _fetch_and_process(
        self, symbol: str, start_date: str, end_date: str, adjust: str
    ) -> pd.DataFrame:
        """获取并处理股票数据"""
        try:
            suffix = "SZ" if symbol.startswith(("0", "3")) else "SH"
            full_symbol = suffix.lower() + symbol

            df = ak.stock_zh_a_daily(symbol=full_symbol)

            if df.empty:
                return pd.DataFrame()

            # 过滤日期范围
            df["date"] = pd.to_datetime(df["date"])
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            if df.empty:
                return pd.DataFrame()

            # 计算涨跌幅
            df["pct_change"] = df["close"].pct_change() * 100
            df["change"] = df["close"].diff()

            # 添加symbol列
            df["symbol"] = symbol

            # 移除无法JSON序列化的字段
            if "outstanding_share" in df.columns:
                df = df.drop(columns=["outstanding_share"])

            # 计算收益率
            df["return_1d"] = df["close"].pct_change()
            df["return_5d"] = df["close"].pct_change(5)

            # 保存缓存
            if self.cache_enabled:
                cache_key = f"daily_{symbol}_{df['date'].min().strftime('%Y-%m-%d')}_{df['date'].max().strftime('%Y-%m-%d')}_{adjust}"
                save_to_cache(df, cache_key, str(CACHE_DIR))

            self.logger.debug(f"获取 {symbol} {len(df)} 条数据")
            return df

        except Exception as e:
            self.logger.error(f"获取 {symbol} 数据失败: {str(e)}")
            return pd.DataFrame()

    def get_multiple_stocks_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        adjust: str = "qfq",
        progress_callback=None,
    ) -> pd.DataFrame:
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

            df = df.rename(
                columns={
                    "date": "date",
                    "open": "open",
                    "close": "close",
                    "high": "high",
                    "low": "low",
                    "volume": "volume",
                }
            )

            df["return_1d"] = df["close"].pct_change()
            return df

        except Exception as e:
            self.logger.error(f"获取指数 {index_code} 失败: {str(e)}")
            return pd.DataFrame()

    def get_factor_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """获取技术指标数据"""
        try:
            suffix = ".SZ" if symbol.startswith(("0", "3")) else ".SH"
            full_symbol = symbol + suffix

            df = ak.stock_zh_a_indicator(symbol=full_symbol)
            return df

        except Exception as e:
            self.logger.error(f"获取 {symbol} 指标数据失败: {str(e)}")
            return None
