"""
预置因子库
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable
from abc import ABC, abstractmethod

from .logger import logger
from .config import PRESET_FACTORS


class BaseFactor(ABC):
    """因子基类"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算因子值"""
        pass


class TrendFactor(BaseFactor):
    """趋势类因子"""

    def __init__(self, name: str, description: str, ma_period: int):
        super().__init__(name, description)
        self.ma_period = ma_period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算移动平均因子"""
        return data['close'].rolling(self.ma_period).mean()


class MomentumFactor(BaseFactor):
    """动量类因子"""

    def __init__(self, name: str, description: str, period: int = 12):
        super().__init__(name, description)
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算动量因子"""
        return data['close'].pct_change(self.period)


class RSI(BaseFactor):
    """相对强弱指标"""

    def __init__(self, name: str = "RSI", description: str = "相对强弱指标", period: int = 14):
        super().__init__(name, description)
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算RSI"""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi


class MACD(BaseFactor):
    """MACD指标"""

    def __init__(self, name: str = "MACD", description: str = "MACD指标",
                 fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__(name, description)
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算MACD"""
        ema_fast = data['close'].ewm(span=self.fast, adjust=False).mean()
        ema_slow = data['close'].ewm(span=self.slow, adjust=False).mean()
        dif = ema_fast - ema_slow
        dea = dif.ewm(span=self.signal, adjust=False).mean()
        macd = 2 * (dif - dea)
        return macd


class BollingerBand(BaseFactor):
    """布林带"""

    def __init__(self, name: str = "BOLL", description: str = "布林带",
                 period: int = 20, std_dev: int = 2):
        super().__init__(name, description)
        self.period = period
        self.std_dev = std_dev

    def calculate(self, data: pd.DataFrame, band: str = "mid") -> pd.Series:
        """计算布林带"""
        ma = data['close'].rolling(self.period).mean()
        std = data['close'].rolling(self.period).std()

        if band == "upper":
            return ma + self.std_dev * std
        elif band == "lower":
            return ma - self.std_dev * std
        else:
            return ma


class ATR(BaseFactor):
    """真实波动幅度均值"""

    def __init__(self, name: str = "ATR", description: str = "真实波动幅度均值", period: int = 14):
        super().__init__(name, description)
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算ATR"""
        high_low = data['high'] - data['low']
        high_close = abs(data['high'] - data['close'].shift())
        low_close = abs(data['low'] - data['close'].shift())

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=self.period).mean()
        return atr


class VolumeFactor(BaseFactor):
    """成交量因子"""

    def __init__(self, name: str = "VOL", description: str = "成交量因子"):
        super().__init__(name, description)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算成交量因子"""
        volume_ma = data['volume'].rolling(20).mean()
        return (data['volume'] - volume_ma) / volume_ma


class ROC(BaseFactor):
    """变动率指标"""

    def __init__(self, name: str = "ROC", description: str = "变动率指标", period: int = 12):
        super().__init__(name, description)
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算ROC"""
        return (data['close'] - data['close'].shift(self.period)) / data['close'].shift(self.period) * 100


class WilliamsR(BaseFactor):
    """威廉指标"""

    def __init__(self, name: str = "Williams%R", description: str = "威廉指标", period: int = 14):
        super().__init__(name, description)
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算Williams %R"""
        highest_high = data['high'].rolling(window=self.period).max()
        lowest_low = data['low'].rolling(window=self.period).min()
        williams_r = -100 * (highest_high - data['close']) / (highest_high - lowest_low)
        return williams_r


class FactorLibrary:
    """因子库"""

    def __init__(self):
        self.logger = logger
        self.factors = PRESET_FACTORS.copy()

    def list_factors(self, category: str = None) -> List[Dict]:
        """列出因子"""
        if category:
            return [v for k, v in self.factors.items() if v['category'] == category]
        return list(self.factors.values())

    def get_factor_categories(self) -> List[str]:
        """获取因子分类"""
        categories = set()
        for f in self.factors.values():
            categories.add(f['category'])
        return sorted(list(categories))

    def get_factor(self, factor_name: str) -> Optional[BaseFactor]:
        """获取因子计算器"""
        factor_map = {
            'ma5': lambda: TrendFactor('MA5', '5日移动平均', 5),
            'ma10': lambda: TrendFactor('MA10', '10日移动平均', 10),
            'ma20': lambda: TrendFactor('MA20', '20日移动平均', 20),
            'ma60': lambda: TrendFactor('MA60', '60日移动平均', 60),
            'rsi': lambda: RSI('RSI', '相对强弱指标', 14),
            'macd': lambda: MACD('MACD', 'MACD指标'),
            'boll_upper': lambda: BollingerBand('BOLL_UPPER', '布林线上轨').calculate(data, 'upper'),
            'boll_lower': lambda: BollingerBand('BOLL_LOWER', '布林线下轨').calculate(data, 'lower'),
            'atr': lambda: ATR('ATR', '真实波动幅度均值', 14),
            'volume_ratio': lambda: VolumeFactor('VR', '量比'),
            'momentum_1m': lambda: MomentumFactor('MOM_1M', '1个月动量', 20),
            'momentum_3m': lambda: MomentumFactor('MOM_3M', '3个月动量', 60),
            'momentum_6m': lambda: MomentumFactor('MOM_6M', '6个月动量', 120),
            'momentum_12m': lambda: MomentumFactor('MOM_12M', '12个月动量', 240),
            'roc': lambda: ROC('ROC', '变动率指标', 12),
            'williams_r': lambda: WilliamsR('Williams%R', '威廉指标', 14),
        }

        if factor_name in factor_map:
            return factor_map[factor_name]()
        return None

    def calculate_factor(self, factor_name: str, data: pd.DataFrame) -> pd.Series:
        """计算因子值"""
        factor = self.get_factor(factor_name)
        if factor is None:
            self.logger.warning(f"因子 {factor_name} 不存在")
            return pd.Series(dtype=float)

        return factor.calculate(data)
