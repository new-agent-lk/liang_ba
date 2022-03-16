from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path('', views.GenericStockMarketView.as_view(), name='stock_market_api'),
]
