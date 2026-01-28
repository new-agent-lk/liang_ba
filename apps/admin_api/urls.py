from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    UserViewSet,
    ProductViewSet,
    NewsViewSet,
    CaseViewSet,
    CarouselViewSet,
    MessageViewSet,
    StockDataViewSet,
    ProductCategoryViewSet,
    DashboardStatsView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'carousels', CarouselViewSet, basename='carousel')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'stock-data', StockDataViewSet, basename='stock-data')
router.register(r'product-categories', ProductCategoryViewSet, basename='product-category')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='admin-login'),
    path('auth/logout/', LoginView.as_view(), name='admin-logout'),
    path('auth/me/', LoginView.as_view(), name='admin-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
