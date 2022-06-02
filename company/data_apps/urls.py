from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from . import views
from data_apps.view_set.generic_stock_market_data import GenericStockMarketDataViewSet

router = SimpleRouter()
router.register('generic-stock-market-data', GenericStockMarketDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path('history', views.GenericHistoryStockMarketView.as_view(), name='history_api'),
    re_path('stock-detail', views.GenericStockMarketView.as_view(), name='stock_detail_api'),
    path('current/<str:stock_code>/', views.CurrentStockCodeView.as_view())
    path('tensc/', views.TenStockDataView.as_view())
]



