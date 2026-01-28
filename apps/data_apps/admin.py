from django.contrib import admin
from data_apps.models import GenericStockMarketData, BlastStockMarketData


@admin.register(GenericStockMarketData)
class GenericStockMarketDataAdmin(admin.ModelAdmin):
    """配置后台股票市场历史数据"""
    list_display = ['id', 'stock_code', 'stock_name', 'now_price', 'current_time']
    list_filter = ['stock_code', 'current_time']
    search_fields = ['stock_code', 'stock_name']
    readonly_fields = ['stock_code', 'stock_name', 'current_time']
    list_per_page = 50


@admin.register(BlastStockMarketData)
class BlastStockMarketDataAdmin(admin.ModelAdmin):
    """配置后台股票指数"""
    list_display = ['id', 'stock_code', 'stock_name']
    search_fields = ['stock_code', 'stock_name']
