"""
Log Viewer ViewSet

API endpoints for viewing and managing system logs.
"""
from rest_framework import views, status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.admin_api.permissions import IsAdminUser, IsSuperUser
from apps.admin_api.serializers.log import (
    LogListQuerySerializer,
    LogListResponseSerializer,
    LogStatsSerializer,
    LogRotationConfigSerializer,
    LogRotationStatusSerializer,
    LogRotationActionSerializer,
    LogViewerAccessLogSerializer,
)
from apps.admin_api.models.system_log import (
    LogRotationConfig,
    LogViewerAccessLog,
)

from utils.logging.reader import get_log_reader
from utils.logging.rotation import get_rotation_manager

import logging

logger = logging.getLogger('app.admin.logs')
User = get_user_model()


class LogListView(views.APIView):
    """
    API endpoint for viewing system logs

    GET /api/admin/logs/

    Query Parameters:
        - log_type: Type of log (app, error, security, performance, django)
        - level: Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - trace_id: Filter by trace_id
        - user_id: Filter by user_id
        - search: Full-text search in message
        - start_time: Filter by start time (ISO format)
        - end_time: Filter by end time (ISO format)
        - offset: Pagination offset (default: 0)
        - limit: Page size (default: 100, max: 500)
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Validate query params
        query_serializer = LogListQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(
                {'error': 'Invalid query parameters', 'details': query_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        params = query_serializer.validated_data

        # Get log reader and read logs
        reader = get_log_reader()

        try:
            result = reader.read_logs(
                log_type=params['log_type'],
                offset=params.get('offset', 0),
                limit=params.get('limit', 100),
                level=params.get('level'),
                trace_id=params.get('trace_id'),
                search=params.get('search'),
                start_time=params.get('start_time'),
                end_time=params.get('end_time'),
            )
        except Exception as e:
            logger.exception("Failed to read logs")
            return Response(
                {'error': 'Failed to read logs', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Log access
        self._log_access(request, params, result)

        # Serialize response
        response_serializer = LogListResponseSerializer(result)
        return Response(response_serializer.data)

    def _log_access(self, request, params, result):
        """Log log viewer access for audit"""
        try:
            LogViewerAccessLog.objects.create(
                user_id=request.user.id,
                username=request.user.username,
                action='view',
                log_type=params.get('log_type'),
                filters_applied={
                    'level': params.get('level'),
                    'trace_id': params.get('trace_id'),
                    'search': params.get('search'),
                },
                ip_address=self._get_client_ip(request),
                user_agent=request.headers.get('User-Agent', '')[:255],
            )
        except Exception:
            pass  # Don't fail on audit logging

    def _get_client_ip(self, request):
        """Get client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')


class LogStatsView(views.APIView):
    """
    API endpoint for log statistics

    GET /api/admin/logs/stats/
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_type = request.query_params.get('log_type', 'app')

        reader = get_log_reader()
        stats = reader.get_log_stats(log_type)

        serializer = LogStatsSerializer(stats)
        return Response(serializer.data)


class LogRotationConfigView(views.APIView):
    """
    API endpoints for log rotation configuration

    GET /api/admin/logs/rotation/config/
    POST /api/admin/logs/rotation/config/
    """
    permission_classes = [IsSuperUser]

    def get(self, request):
        """Get rotation configurations"""
        configs = LogRotationConfig.objects.all()
        serializer = LogRotationConfigSerializer(configs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create or update rotation configuration"""
        log_type = request.data.get('log_type')
        if not log_type:
            return Response(
                {'error': 'log_type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        config, created = LogRotationConfig.objects.update_or_create(
            log_type=log_type,
            defaults={
                'max_size_mb': request.data.get('max_size_mb', 10),
                'max_files': request.data.get('max_files', 10),
                'max_age_days': request.data.get('max_age_days', 30),
                'compress_old': request.data.get('compress_old', True),
                'enabled': request.data.get('enabled', True),
            }
        )

        serializer = LogRotationConfigSerializer(config)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class LogRotationActionView(views.APIView):
    """
    API endpoints for log rotation actions

    POST /api/admin/logs/rotation/action/
    GET /api/admin/logs/rotation/status/?log_type=app
    """
    permission_classes = [IsSuperUser]

    def post(self, request):
        """Perform rotation action"""
        serializer = LogRotationActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid request', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        action = data['action']
        log_type = data.get('log_type')

        manager = get_rotation_manager()

        if action == 'rotate':
            result = manager.manual_rotate(log_type)
            # Update last_rotated time
            LogRotationConfig.objects.filter(log_type=log_type).update(
                last_rotated=timezone.now()
            )
            return Response(result)

        elif action == 'pause':
            LogRotationConfig.objects.filter(log_type=log_type).update(
                is_manually_paused=True
            )
            return Response({'status': 'paused'})

        elif action == 'resume':
            LogRotationConfig.objects.filter(log_type=log_type).update(
                is_manually_paused=False
            )
            return Response({'status': 'resumed'})

        return Response(
            {'error': 'Unknown action'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        """Get rotation status"""
        log_type = request.query_params.get('log_type', 'app')

        manager = get_rotation_manager()
        status_info = manager.get_rotation_status(log_type)

        serializer = LogRotationStatusSerializer(status_info)
        return Response(serializer.data)


class LogRotationArchivedFilesView(views.APIView):
    """
    API endpoint for viewing archived log files

    GET /api/admin/logs/rotation/files/?log_type=app
    DELETE /api/admin/logs/rotation/files/?log_type=app&filename=xxx
    """
    permission_classes = [IsSuperUser]

    def get(self, request):
        """List archived files"""
        log_type = request.query_params.get('log_type', 'app')

        manager = get_rotation_manager()
        status_info = manager.get_rotation_status(log_type)

        return Response({
            'archived_files': status_info.get('archived_files', []),
            'total_count': status_info.get('archived_files_count', 0),
        })

    def delete(self, request):
        """Delete archived file"""
        log_type = request.query_params.get('log_type')
        filename = request.query_params.get('filename')

        if not log_type or not filename:
            return Response(
                {'error': 'log_type and filename required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from pathlib import Path

        logs_dir = Path('/home/ubuntu/liang_ba/logs')
        file_path = logs_dir / filename

        if not file_path.exists():
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            file_path.unlink()
            return Response({'status': 'deleted'})
        except Exception as e:
            return Response(
                {'error': f'Failed to delete: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogViewerAccessLogView(views.APIView):
    """
    API endpoint for log viewer audit logs

    GET /api/admin/logs/access-logs/
    """
    permission_classes = [IsSuperUser]

    def get(self, request):
        """Get access logs with filtering"""
        logs = LogViewerAccessLog.objects.all()

        # Filter by user
        user_id = request.query_params.get('user_id')
        if user_id:
            logs = logs.filter(user_id=user_id)

        # Filter by action
        action = request.query_params.get('action')
        if action:
            logs = logs.filter(action=action)

        # Filter by log type
        log_type = request.query_params.get('log_type')
        if log_type:
            logs = logs.filter(log_type=log_type)

        # Pagination
        limit = min(int(request.query_params.get('limit', 100)), 500)
        offset = int(request.query_params.get('offset', 0))

        total = logs.count()
        logs = logs[offset:offset+limit]

        serializer = LogViewerAccessLogSerializer(logs, many=True)
        return Response({
            'logs': serializer.data,
            'total': total,
            'offset': offset,
            'limit': limit,
        })
