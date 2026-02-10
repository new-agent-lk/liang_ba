from django.urls import path

from .views import (
    AnalysisExecuteView,
    BacktestView,
    CacheInfoView,
    DataFetchView,
    DecileAnalysisView,
    FactorComputeView,
    FactorListView,
    ICAnalysisView,
    StatsView,
    StockListView,
    StockPoolView,
)

app_name = "factorhub"

urlpatterns = [
    # 统计信息
    path("stats/", StatsView.as_view(), name="stats"),
    # 股票数据
    path("stocks/", StockListView.as_view(), name="stock-list"),
    path("stock-pool/", StockPoolView.as_view(), name="stock-pool"),
    # 数据获取
    path("data/", DataFetchView.as_view(), name="data-fetch"),
    path("cache/", CacheInfoView.as_view(), name="cache-info"),
    path("cache/clear/", CacheInfoView.as_view(), name="cache-clear"),
    # 因子管理
    path("factors/", FactorListView.as_view(), name="factor-list"),
    path("factors/compute/", FactorComputeView.as_view(), name="factor-compute"),
    # 因子分析
    path("analysis/ic/", ICAnalysisView.as_view(), name="ic-analysis"),
    path("analysis/decile/", DecileAnalysisView.as_view(), name="decile-analysis"),
    # 回测
    path("backtest/", BacktestView.as_view(), name="backtest"),
    path("analysis/execute/", AnalysisExecuteView.as_view(), name="analysis-execute"),
]
