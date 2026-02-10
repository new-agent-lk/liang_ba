"""
全局配置
"""

from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "Data" / "factorhub"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 缓存目录
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 因子目录
FACTORS_DIR = DATA_DIR / "factors"
FACTORS_DIR.mkdir(parents=True, exist_ok=True)

# 结果目录
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 默认配置
DEFAULT_CONFIG = {
    "data": {
        "default_market": "all",
        "default_pool": "hs300",
        "default_frequency": "daily",
        "default_adjust": "qfq",
    },
    "factor": {
        "default_window": 20,
        "max_workers": 4,
    },
    "analysis": {
        "ic_window": 252,
        "decile_n": 10,
    },
    "backtest": {
        "initial_capital": 1000000,
        "commission": 0.0003,
        "slippage": 0.001,
        "benchmark": "000300",
    },
}

# 预置因子列表
PRESET_FACTORS = {
    # 技术指标类
    "ma5": {"name": "MA5", "category": "technical", "description": "5日简单移动平均"},
    "ma10": {"name": "MA10", "category": "technical", "description": "10日简单移动平均"},
    "ma20": {"name": "MA20", "category": "technical", "description": "20日简单移动平均"},
    "ma60": {"name": "MA60", "category": "technical", "description": "60日简单移动平均"},
    "ema5": {"name": "EMA5", "category": "technical", "description": "5日指数移动平均"},
    "ema10": {"name": "EMA10", "category": "technical", "description": "10日指数移动平均"},
    "ema20": {"name": "EMA20", "category": "technical", "description": "20日指数移动平均"},
    "rsi": {"name": "RSI", "category": "technical", "description": "相对强弱指标"},
    "macd": {"name": "MACD", "category": "technical", "description": "指数平滑异同移动平均线"},
    "boll_upper": {"name": "BOLL_UPPER", "category": "technical", "description": "布林线上轨"},
    "boll_lower": {"name": "BOLL_LOWER", "category": "technical", "description": "布林线下轨"},
    "atr": {"name": "ATR", "category": "technical", "description": "真实波动幅度均值"},
    "obv": {"name": "OBV", "category": "technical", "description": "能量潮"},
    # 动量类
    "momentum_1m": {"name": "MOM_1M", "category": "momentum", "description": "1个月动量"},
    "momentum_3m": {"name": "MOM_3M", "category": "momentum", "description": "3个月动量"},
    "momentum_6m": {"name": "MOM_6M", "category": "momentum", "description": "6个月动量"},
    "momentum_12m": {"name": "MOM_12M", "category": "momentum", "description": "12个月动量"},
    "roc": {"name": "ROC", "category": "momentum", "description": "变动率指标"},
    "williams_r": {"name": "Williams%R", "category": "momentum", "description": "威廉指标"},
    # 波动率类
    "volatility_20": {"name": "VOL_20", "category": "volatility", "description": "20日波动率"},
    "volatility_60": {"name": "VOL_60", "category": "volatility", "description": "60日波动率"},
    # 成交量类
    "volume_ratio": {"name": "VR", "category": "volume", "description": "量比"},
    "volume_ma5": {"name": "VOL_MA5", "category": "volume", "description": "5日均量"},
    "volume_ma20": {"name": "VOL_MA20", "category": "volume", "description": "20日均量"},
    # 估值类 (需要基本面数据)
    "pe": {"name": "PE", "category": "valuation", "description": "市盈率"},
    "pb": {"name": "PB", "category": "valuation", "description": "市净率"},
    "ps": {"name": "PS", "category": "valuation", "description": "市销率"},
    "pcf": {"name": "PCF", "category": "valuation", "description": "现金流倍率"},
}
