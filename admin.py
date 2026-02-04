"""
Django Admin Configuration for Logging Module

Provides admin interface for log viewing and management.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect
from django.http import JsonResponse

from apps.admin_api.models.system_log import (
    SystemLogIndex,
    LogRotationConfig,
    LogViewerAccessLog,
)
from utils.logging.reader import get_log_reader
from utils.logging.rotation import get_rotation_manager


@admin.register(SystemLogIndex)
class SystemLogIndexAdmin(admin.ModelAdmin):
    """Admin for indexed log entries"""

    list_display = [
        'timestamp', 'level_colored', 'logger_short',
        'message_preview', 'trace_id_link', 'user_id'
    ]
    list_filter = ['level', 'log_type', 'timestamp', 'logger']
    search_fields = ['message', 'trace_id', 'request_id', 'logger']
    date_hierarchy = 'timestamp'
    show_full_result_count = False

    fieldsets = (
        ('Log Information', {
            'fields': ('timestamp', 'level', 'log_type')
        }),
        ('Content', {
            'fields': ('logger', 'message')
        }),
        ('Context', {
            'fields': ('trace_id', 'request_id', 'user_id', 'client_ip')
        }),
        ('Metadata', {
            'fields': ('file_offset', 'line_number', 'indexed', 'extra_data'),
            'classes': ('collapse',)
        }),
    )

    def level_colored(self, obj):
        """Display level with color"""
        colors = {
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'darkred',
        }
        color = colors.get(obj.level, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.level)
    level_colored.short_description = 'Level'
    level_colored.admin_order_field = 'level'

    def logger_short(self, obj):
        """Shorten logger name"""
        parts = obj.logger.split('.')
        return parts[-1] if parts else obj.logger
    logger_short.short_description = 'Logger'

    def message_preview(self, obj):
        """Show message preview"""
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'

    def trace_id_link(self, obj):
        """Link to trace filter"""
        if obj.trace_id and obj.trace_id != '-':
            url = f"?trace_id={obj.trace_id}"
            return format_html('<a href="{}">{}</a>', url, obj.trace_id[:16])
        return '-'
    trace_id_link.short_description = 'Trace ID'


@admin.register(LogRotationConfig)
class LogRotationConfigAdmin(admin.ModelAdmin):
    """Admin for log rotation configuration"""

    list_display = [
        'log_type', 'max_size_mb', 'max_files',
        'max_age_days', 'compress_old', 'enabled',
        'last_rotated', 'is_manually_paused'
    ]
    list_filter = ['enabled', 'is_manually_paused', 'compress_old']

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of config"""
        return False

    def has_add_permission(self, request):
        """Only allow adding if no config exists"""
        return LogRotationConfig.objects.count() == 0


@admin.register(LogViewerAccessLog)
class LogViewerAccessLogAdmin(admin.ModelAdmin):
    """Admin for log viewer access audit"""

    list_display = [
        'create_time', 'username', 'action_colored',
        'log_type', 'ip_address'
    ]
    list_filter = ['action', 'log_type', 'create_time']
    date_hierarchy = 'create_time'
    show_full_result_count = False

    def action_colored(self, obj):
        """Color code actions"""
        colors = {
            'view': 'blue',
            'export': 'green',
            'rotate': 'orange',
        }
        color = colors.get(obj.action, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.action)
    action_colored.short_description = 'Action'


class LogAdminSite(admin.AdminSite):
    """Custom admin site for logging module"""

    site_header = 'System Logs Administration'
    site_title = 'Logs Admin'
    index_title = 'Log Management'

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path('logs/file-viewer/', self.admin_view(self.file_viewer), name='log-file-viewer'),
            path('logs/file-viewer/<str:log_type>/', self.admin_view(self.file_viewer), name='log-file-viewer-type'),
            path('logs/rotation-dashboard/', self.admin_view(self.rotation_dashboard), name='log-rotation-dashboard'),
            path('api/logs/rotate/<str:log_type>/', self.admin_view(self.api_rotate_log), name='log-api-rotate'),
        ]

        return custom_urls + urls

    def file_viewer(self, request, log_type='app'):
        """File-based log viewer page"""
        # Get query parameters
        level = request.GET.get('level', '')
        trace_id = request.GET.get('trace_id', '')
        search = request.GET.get('search', '')
        start_time = request.GET.get('start_time', '')
        end_time = request.GET.get('end_time', '')
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))

        # Read logs
        reader = get_log_reader()
        result = reader.read_logs(
            log_type=log_type,
            offset=offset,
            limit=limit,
            level=level if level else None,
            trace_id=trace_id if trace_id else None,
            search=search if search else None,
        )

        context = {
            'log_type': log_type,
            'available_logs': ['app', 'error', 'security', 'performance', 'django'],
            'entries': result['entries'],
            'total': result['total'],
            'offset': result['offset'],
            'limit': result['limit'],
            'has_more': result['has_more'],
            'level_filter': level,
            'trace_id_filter': trace_id,
            'search_filter': search,
            'start_time_filter': start_time,
            'end_time_filter': end_time,
            'next_offset': offset + limit,
            'prev_offset': max(0, offset - limit),
            'params': request.GET.urlencode(),
            **self.each_context(request),
        }
        return render(request, 'admin/logging/log_list.html', context)

    def rotation_dashboard(self, request):
        """Rotation management dashboard"""
        manager = get_rotation_manager()

        statuses = {}
        for log_type in ['app', 'error', 'security', 'performance', 'django']:
            statuses[log_type] = manager.get_rotation_status(log_type)

        context = {
            'statuses': statuses,
            **self.each_context(request),
        }
        return render(request, 'admin/logging/rotation_config.html', context)

    def api_rotate_log(self, request, log_type):
        """API endpoint for manual rotation"""
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        manager = get_rotation_manager()
        result = manager.manual_rotate(log_type)

        return JsonResponse(result)


# Create admin site instance
log_admin_site = LogAdminSite(name='log_admin')

# Register models with custom admin site
log_admin_site.register(SystemLogIndex, SystemLogIndexAdmin)
log_admin_site.register(LogRotationConfig, LogRotationConfigAdmin)
log_admin_site.register(LogViewerAccessLog, LogViewerAccessLogAdmin)


# Also register models with default admin site for easy access
admin.site.register(SystemLogIndex, SystemLogIndexAdmin)
admin.site.register(LogRotationConfig, LogRotationConfigAdmin)
admin.site.register(LogViewerAccessLog, LogViewerAccessLogAdmin)
