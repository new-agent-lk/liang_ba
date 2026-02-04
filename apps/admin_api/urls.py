from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .viewsets.public import LoginView, UserInfoView
from .viewsets.users import UserViewSet
from .viewsets.company import CompanyInfoView
from .viewsets.dashboard import DashboardStatsView
from .viewsets.resumes import ResumeViewSet
from .viewsets.jobs import JobPositionViewSet
from .viewsets.logs import (
    LogListView,
    LogStatsView,
    LogRotationConfigView,
    LogRotationActionView,
    LogRotationArchivedFilesView,
    LogViewerAccessLogView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'jobs', JobPositionViewSet, basename='job')

urlpatterns = [
    # Auth endpoints
    path('auth/login/', LoginView.as_view(), name='admin-login'),
    path('auth/logout/', LoginView.as_view(), name='admin-logout'),
    path('auth/me/', UserInfoView.as_view(), name='admin-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Company info
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),

    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),

    # Log viewing endpoints
    path('logs/', LogListView.as_view(), name='log-list'),
    path('logs/stats/', LogStatsView.as_view(), name='log-stats'),
    path('logs/access-logs/', LogViewerAccessLogView.as_view(), name='log-access-logs'),
    path('logs/rotation/config/', LogRotationConfigView.as_view(), name='log-rotation-config'),
    path('logs/rotation/action/', LogRotationActionView.as_view(), name='log-rotation-action'),
    path('logs/rotation/files/', LogRotationArchivedFilesView.as_view(), name='log-rotation-files'),

    # Router URLs
    path('', include(router.urls)),
]
