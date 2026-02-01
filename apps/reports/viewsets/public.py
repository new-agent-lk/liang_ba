from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.db import models

from apps.reports.models import ResearchReport
from apps.reports.serializers import ResearchReportSerializer, ResearchReportListSerializer


class PublicReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    公开报告API（前台页面使用）
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ResearchReportListSerializer

    def get_queryset(self):
        # 只返回已发布且公开的报告
        queryset = ResearchReport.objects.filter(
            is_public=True,
            status='published'
        ).select_related('author').order_by('-is_top', '-published_at')

        # 筛选策略类型
        strategy_type = self.request.query_params.get('strategy_type')
        if strategy_type:
            queryset = queryset.filter(strategy_type=strategy_type)

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(strategy_name__icontains=search) |
                models.Q(tags__icontains=search)
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ResearchReportSerializer
        return ResearchReportListSerializer

    def retrieve(self, request, *args, **kwargs):
        # 增加阅读量
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """最新报告"""
        reports = self.get_queryset()[:10]
        serializer = ResearchReportListSerializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top(self, request):
        """置顶报告"""
        reports = self.get_queryset().filter(is_top=True)[:5]
        serializer = ResearchReportListSerializer(reports, many=True)
        return Response(serializer.data)
