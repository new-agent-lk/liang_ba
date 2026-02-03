from rest_framework import serializers


class StockListSerializer(serializers.Serializer):
    """股票列表序列化器"""
    symbol = serializers.CharField()
    name = serializers.CharField()


class DataFetchSerializer(serializers.Serializer):
    """数据获取序列化器"""
    symbols = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="股票代码列表，不传则使用股票池"
    )
    stock_pool = serializers.ChoiceField(
        choices=['hs300', 'zz500', 'cyb', 'custom'],
        default='hs300',
        help_text="股票池"
    )
    start_date = serializers.DateField(default='2020-01-01')
    end_date = serializers.DateField(default='2023-12-31')
    adjust = serializers.ChoiceField(
        choices=['qfq', 'hfq', 'none'],
        default='qfq',
        help_text="复权类型"
    )


class FactorSerializer(serializers.Serializer):
    """因子序列化器"""
    name = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()


class FactorComputeSerializer(serializers.Serializer):
    """因子计算序列化器"""
    factor_names = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="因子名称列表"
    )
    symbol = serializers.CharField(required=False, help_text="股票代码")


class ICAnalysisSerializer(serializers.Serializer):
    """IC分析序列化器"""
    factor_name = serializers.CharField(help_text="因子名称")
    method = serializers.ChoiceField(
        choices=['spearman', 'pearson'],
        default='spearman',
        help_text="IC计算方法"
    )
    window = serializers.IntegerField(required=False, min_value=1, help_text="滚动窗口")


class DecileAnalysisSerializer(serializers.Serializer):
    """分层回测序列化器"""
    factor_name = serializers.CharField(help_text="因子名称")
    n_deciles = serializers.IntegerField(default=10, min_value=3, max_value=10)


class BacktestSerializer(serializers.Serializer):
    """回测序列化器"""
    factor_name = serializers.CharField(help_text="因子名称")
    initial_capital = serializers.FloatField(default=1000000)
    rebalance_freq = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'],
        default='weekly'
    )
    long_quantile = serializers.IntegerField(default=3)
    short_quantile = serializers.IntegerField(default=8)


class MarketDataSerializer(serializers.Serializer):
    """市场数据序列化器"""
    symbol = serializers.CharField()
    date = serializers.DateField()
    open = serializers.FloatField()
    close = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    return_1d = serializers.FloatField()


class ICResultSerializer(serializers.Serializer):
    """IC结果序列化器"""
    ic_series = serializers.ListField()
    ic_mean = serializers.FloatField()
    ic_std = serializers.FloatField()
    ir = serializers.FloatField()
    ic_win_rate = serializers.FloatField()
    sample_count = serializers.IntegerField()


class BacktestResultSerializer(serializers.Serializer):
    """回测结果序列化器"""
    portfolio_values = serializers.ListField()
    total_return = serializers.FloatField()
    annual_return = serializers.FloatField()
    sharpe_ratio = serializers.FloatField()
    max_drawdown = serializers.FloatField()
    win_rate = serializers.FloatField()
    final_value = serializers.FloatField()
