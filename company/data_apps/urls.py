from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from . import views
from data_apps.view_set.generic_stock_market_data import GenericStockMarketDataViewSet

router = SimpleRouter()
router.register('generic-stock-market-data', GenericStockMarketDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path('history', views.GenericStockMarketView.as_view(), name='stock_market_api'),
    re_path('stock-detail', views.GenericStockMarketView.as_view(), name='stock_market_api'),

]



