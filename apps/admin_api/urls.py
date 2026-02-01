from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .viewsets.public import LoginView, UserInfoView
from .viewsets.users import UserViewSet
from .viewsets.company import CompanyInfoView
from .viewsets.dashboard import DashboardStatsView
from .viewsets.resumes import ResumeViewSet
from .viewsets.jobs import JobPositionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'jobs', JobPositionViewSet, basename='job')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='admin-login'),
    path('auth/logout/', LoginView.as_view(), name='admin-logout'),
    path('auth/me/', UserInfoView.as_view(), name='admin-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
