from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import UserCategory


@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    """用户类别管理后台"""
    list_display = ['user', 'category', 'company', 'position', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__username', 'user__email', 'company']
