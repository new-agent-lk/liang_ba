from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path('history', views.GenericStockMarketView.as_view(), name='stock_market_api'),
    re_path('stock-detail', views.GenericStockMarketView.as_view(), name='stock_market_api'),
]
