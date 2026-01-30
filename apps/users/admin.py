from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Resume, UserCategory


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """简历管理后台"""
    list_display = ['name', 'job_category', 'phone', 'email', 'status', 'created_at']
    list_filter = ['status', 'job_category', 'education', 'created_at']
    search_fields = ['name', 'phone', 'email', 'school']
    readonly_fields = ['user', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'name', 'phone', 'email', 'age')
        }),
        ('求职信息', {
            'fields': ('job_category', 'expected_salary')
        }),
        ('教育背景', {
            'fields': ('education', 'school', 'major')
        }),
        ('专业信息', {
            'fields': ('work_experience', 'skills', 'self_introduction')
        }),
        ('简历文件', {
            'fields': ('resume_file',)
        }),
        ('审核信息', {
            'fields': ('status', 'review_notes', 'reviewed_by', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_resumes', 'reject_resumes']

    def approve_resumes(self, request, queryset):
        """批量通过简历"""
        queryset.update(status='approved', reviewed_by=request.user, reviewed_at=timezone.now())
    approve_resumes.short_description = '批量通过选中简历'

    def reject_resumes(self, request, queryset):
        """批量拒绝简历"""
        queryset.update(status='rejected', reviewed_by=request.user, reviewed_at=timezone.now())
    reject_resumes.short_description = '批量拒绝选中简历'


@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    """用户类别管理后台"""
    list_display = ['user', 'category', 'company', 'position', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__username', 'user__email', 'company']
