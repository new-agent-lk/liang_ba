# 用户认证路由
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/api/', views.login_api, name='login_api'),  # 登录 API
    path('auth/', views.auth_view, name='auth'),  # 统一登录注册页面
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/api/', views.register_api, name='register_api'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/api/', views.profile_api, name='profile_api'),
    path('logout/api/', views.logout_api, name='logout_api'),
]
