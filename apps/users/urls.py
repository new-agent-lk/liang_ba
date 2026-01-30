# 用户认证路由
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/api/', views.register_api, name='register_api'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/api/', views.profile_api, name='profile_api'),
    path('logout/api/', views.logout_api, name='logout_api'),
]
