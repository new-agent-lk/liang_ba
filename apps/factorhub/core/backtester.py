"""
回测引擎
"""

import warnings
from typing import Dict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from .logger import logger


class Backtester:
    """回测引擎"""

    def __init__(
        self,
        initial_capital: float = 1000000,
        commission: float = 0.0003,
        slippage: float = 0.001,
        benchmark: str = "000300",
    ):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.benchmark = benchmark
        self.logger = logger
        self.reset()

    def reset(self):
        """重置回测状态"""
        self.current_capital = self.initial_capital
        self.positions = {}
        self.portfolio_value = []
        self.cash_history = []
        self.positions_history = []
        self.trades_history = []
        self.benchmark_data = []

    def load_price_data(self, data: pd.DataFrame, symbol: str, date) -> Dict:
        """获取股票价格数据"""
        symbol_data = data[data["symbol"] == symbol]
        price_data = symbol_data[symbol_data["date"] <= date].sort_values("date")

        if len(price_data) == 0:
            return {}

        latest = price_data.iloc[-1]
        return {
            "open": latest["open"],
            "close": latest["close"],
            "high": latest["high"],
            "low": latest["low"],
            "volume": latest["volume"],
        }

    def execute_trade(self, symbol: str, target_weight: float, current_price: float, date) -> Dict:
        """执行交易"""
        try:
            portfolio_value = self.current_capital + sum(
                self.positions.get(s, 0) * current_price for s in self.positions
            )
            target_value = target_weight * portfolio_value

            current_quantity = self.positions.get(symbol, 0)
            current_value = current_quantity * current_price

            value_diff = target_value - current_value
            if abs(value_diff) < self.initial_capital * 0.001:
                return {"symbol": symbol, "action": "hold", "quantity": 0, "cost": 0}

            if value_diff > 0:
                adjusted_price = current_price * (1 + self.slippage)
                transaction_cost = self.commission
            else:
                adjusted_price = current_price * (1 - self.slippage)
                transaction_cost = self.commission

            if value_diff > 0:
                trade_quantity = value_diff / (adjusted_price * (1 + transaction_cost))
                action = "buy"
            else:
                trade_quantity = abs(value_diff) / (adjusted_price * (1 - transaction_cost))
                action = "sell"

            trade_quantity = int(trade_quantity / 100) * 100

            if trade_quantity == 0:
                return {"symbol": symbol, "action": "hold", "quantity": 0, "cost": 0}

            cost = abs(trade_quantity * adjusted_price * (1 + transaction_cost))
            if action == "buy":
                self.current_capital -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + trade_quantity
            else:
                self.current_capital += cost
                self.positions[symbol] = max(0, self.positions.get(symbol, 0) - trade_quantity)
                if self.positions[symbol] == 0:
                    del self.positions[symbol]

            return {
                "symbol": symbol,
                "action": action,
                "quantity": trade_quantity,
                "price": adjusted_price,
                "cost": cost,
            }

        except Exception as e:
            self.logger.error(f"交易执行失败: {str(e)}")
            return {"symbol": symbol, "action": "error", "error": str(e)}

    def run_backtest(
        self,
        data: pd.DataFrame,
        factor_name: str,
        rebalance_freq: str = "weekly",
        long_quantile: int = 3,
        short_quantile: int = 8,
    ) -> Dict:
        """运行回测"""
        self.reset()

        try:
            dates = sorted(data["date"].unique())
            symbols = data["symbol"].unique()

            if len(dates) < 10 or len(symbols) < 10:
                return {"error": "数据量不足"}

            # 确定再平衡日期
            if rebalance_freq == "daily":
                rebalance_dates = dates[20:]
            elif rebalance_freq == "weekly":
                rebalance_dates = [d for i, d in enumerate(dates) if i % 5 == 0]
            elif rebalance_freq == "monthly":
                rebalance_dates = [d for i, d in enumerate(dates) if i % 20 == 0]
            else:
                rebalance_dates = dates[20:]

            # 回测循环
            portfolio_values = []
            for date in dates:
                if date in rebalance_dates:
                    # 计算因子分位数
                    date_data = data[data["date"] == date].copy()
                    if factor_name not in date_data.columns:
                        continue

                    date_data = date_data.dropna(subset=[factor_name])
                    if len(date_data) < 10:
                        continue

                    try:
                        date_data["quantile"] = pd.qcut(
                            date_data[factor_name], q=10, labels=False, duplicates="drop"
                        )
                    except:
                        continue

                    # 计算目标权重
                    long_symbols = date_data[date_data["quantile"] <= long_quantile][
                        "symbol"
                    ].tolist()
                    short_symbols = date_data[date_data["quantile"] >= short_quantile][
                        "symbol"
                    ].tolist()

                    n_long = max(1, len(long_symbols))
                    n_short = max(1, len(short_symbols))

                    for symbol in symbols:
                        price_data = self.load_price_data(data, symbol, date)
                        if not price_data:
                            continue

                        if symbol in long_symbols:
                            target_weight = 1.0 / n_long * 0.5
                        elif symbol in short_symbols:
                            target_weight = -1.0 / n_short * 0.5
                        else:
                            target_weight = 0

                        self.execute_trade(symbol, target_weight, price_data["close"], date)

                # 更新组合价值
                total_value = self.current_capital
                for symbol, quantity in self.positions.items():
                    price_data = self.load_price_data(data, symbol, date)
                    if price_data:
                        total_value += quantity * price_data["close"]

                portfolio_values.append({"date": str(date), "value": total_value})
                self.portfolio_value.append(total_value)

            # 计算绩效指标
            portfolio_values_df = pd.DataFrame(portfolio_values)
            if len(portfolio_values_df) < 2:
                return {"error": "回测数据不足"}

            returns = portfolio_values_df["value"].pct_change().dropna()

            total_return = (
                (portfolio_values_df["value"].iloc[-1] / self.initial_capital - 1)
                if self.initial_capital > 0
                else 0
            )
            annual_return = (
                total_return * 252 / len(portfolio_values_df) if len(portfolio_values_df) > 0 else 0
            )
            volatility = returns.std() * np.sqrt(252) if len(returns) > 0 else 0
            sharpe = annual_return / volatility if volatility > 0 else 0

            # 计算最大回撤
            cummax = portfolio_values_df["value"].cummax()
            drawdown = (portfolio_values_df["value"] - cummax) / cummax
            max_drawdown = drawdown.min()

            # 胜率
            positive_days = (returns > 0).sum()
            total_days = len(returns)
            win_rate = positive_days / total_days if total_days > 0 else 0

            return {
                "portfolio_values": portfolio_values_df.to_dict("records"),
                "total_return": total_return,
                "annual_return": annual_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_drawdown,
                "win_rate": win_rate,
                "final_value": portfolio_values_df["value"].iloc[-1],
                "initial_capital": self.initial_capital,
            }

        except Exception as e:
            self.logger.error(f"回测失败: {str(e)}")
            return {"error": str(e)}
