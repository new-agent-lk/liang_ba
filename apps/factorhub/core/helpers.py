"""
辅助函数集合
"""

from typing import Union

import pandas as pd


def format_number(num: Union[float, int], decimals: int = 4) -> str:
    """格式化数字"""
    if pd.isna(num):
        return "-"
    if abs(num) < 0.0001 and num != 0:
        return f"{num:.2e}"
    return f"{num:.{decimals}f}"


def format_percentage(num: Union[float, int], decimals: int = 2) -> str:
    """格式化百分比"""
    if pd.isna(num):
        return "-"
    return f"{num * 100:.{decimals}f}%"


def calculate_ic(ic_series: pd.Series) -> float:
    """计算IC均值"""
    return ic_series.mean()


def calculate_ir(ic_series: pd.Series) -> float:
    """计算IR (信息比率)"""
    ic_mean = ic_series.mean()
    ic_std = ic_series.std()
    if ic_std == 0:
        return 0
    return ic_mean / ic_std


def calculate_ic_win_rate(ic_series: pd.Series) -> float:
    """计算IC胜率 (正IC占比)"""
    positive_ic = (ic_series > 0).sum()
    total = len(ic_series)
    if total == 0:
        return 0
    return positive_ic / total


def validate_stock_code(code: str) -> bool:
    """验证股票代码格式"""
    if not code:
        return False
    code = str(code).strip()
    # 沪市: 6开头, 深市: 0/3开头
    if len(code) != 6:
        return False
    if not code.isdigit():
        return False
    if code[0] not in ["0", "3", "6"]:
        return False
    return True


def normalize_stock_code(code: str) -> str:
    """标准化股票代码"""
    code = str(code).strip()
    # 补齐6位
    while len(code) < 6:
        code = "0" + code
    return code[-6:]


def format_date(date_str: str, input_format: str = "%Y%m%d") -> str:
    """格式化日期"""
    try:
        from datetime import datetime

        if isinstance(date_str, str):
            dt = datetime.strptime(date_str, input_format)
            return dt.strftime("%Y-%m-%d")
        return str(date_str)
    except:
        return date_str


def save_to_cache(data, filename: str, cache_dir: str):
    """保存数据到缓存"""
    import os
    import pickle

    os.makedirs(cache_dir, exist_ok=True)
    filepath = os.path.join(cache_dir, filename)
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    return filepath


def load_from_cache(filename: str, cache_dir: str, max_age_days: int = 7):
    """从缓存加载数据"""
    import os
    import pickle
    from datetime import datetime, timedelta

    filepath = os.path.join(cache_dir, filename)
    if not os.path.exists(filepath):
        return None
    # 检查文件年龄
    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    if datetime.now() - file_time > timedelta(days=max_age_days):
        os.remove(filepath)
        return None
    with open(filepath, "rb") as f:
        return pickle.load(f)
