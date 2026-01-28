from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """自定义用户管理"""
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name', 'department', 'position', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'gender', 'department', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'employee_id']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'gender', 'birthday')
        }),
        (_('工作信息'), {
            'fields': ('department', 'position', 'employee_id')
        }),
        (_('权限'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('重要日期'), {
            'fields': ('last_login', 'date_joined'),
        }),
        (_('其他信息'), {
            'fields': ('last_login_ip', 'login_count', 'bio', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'created_at', 'updated_at', 'login_count', 'last_login_ip']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理"""
    list_display = ['user', 'city', 'province', 'language', 'timezone', 'theme']
    list_filter = ['city', 'province', 'language', 'timezone', 'theme']
    search_fields = ['user__username', 'user__email', 'address', 'city']
    
    fieldsets = (
        (_('联系信息'), {
            'fields': ('address', 'city', 'province', 'postal_code')
        }),
        (_('社交媒体'), {
            'fields': ('wechat', 'qq', 'linkedin')
        }),
        (_('偏好设置'), {
            'fields': ('language', 'timezone', 'theme')
        }),
        (_('通知设置'), {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications')
        }),
    )