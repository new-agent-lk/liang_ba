from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.db import models
from django.utils import timezone

from apps.reports.models import ResearchReport
from apps.reports.serializers import (
    ResearchReportSerializer,
    ResearchReportCreateSerializer,
    ResearchReportReviewSerializer,
    ResearchReportListSerializer,
)
from apps.reports.permissions import IsResearcherOrReadOnly, CanReviewReport


class ResearchReportViewSet(viewsets.ModelViewSet):
    """
    研究报告管理视图集
    """
    queryset = ResearchReport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsResearcherOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchReportListSerializer
        elif self.action == 'create':
            return ResearchReportCreateSerializer
        return ResearchReportSerializer

    def get_queryset(self):
        queryset = ResearchReport.objects.select_related('author', 'reviewer')

        # 超级管理员和部门负责人可以看到所有报告
        user = self.request.user
        is_admin = user.is_superuser or (
            hasattr(user, 'profile') and user.profile.position and '负责人' in user.profile.position
        )

        if not is_admin:
            # 普通用户只能看到自己的报告或已发布的公开报告
            queryset = queryset.filter(
                models.Q(author=user) | models.Q(is_public=True, status='published')
            )

        # 筛选状态
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 筛选是否公开
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')

        # 搜索标题
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(strategy_name__icontains=search) |
                models.Q(tags__icontains=search)
            )

        # 筛选策略类型
        strategy_type = self.request.query_params.get('strategy_type')
        if strategy_type:
            queryset = queryset.filter(strategy_type=strategy_type)

        return queryset.order_by('-is_top', '-published_at', '-created_at')

    def perform_create(self, serializer):
        report = serializer.save()
        # 草稿提交后自动设为待审核
        if self.request.data.get('submit_for_review'):
            report.status = 'pending'
            report.save()

    def perform_update(self, serializer):
        report = serializer.instance
        # 检查是否要删除图片（前端传 null 表示删除）
        if 'detail_image' in serializer.validated_data and serializer.validated_data['detail_image'] is None:
            # 删除现有图片文件
            if report.detail_image:
                report.detail_image.delete(save=False)
        serializer.save()

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """提交审核"""
        report = self.get_object()
        if report.author != request.user:
            return Response({'detail': '只能提交自己的报告'}, status=status.HTTP_403_FORBIDDEN)
        if report.status != 'draft':
            return Response({'detail': '只有草稿状态的报告可以提交审核'}, status=status.HTTP_400_BAD_REQUEST)

        report.status = 'pending'
        report.save()
        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """审核报告"""
        report = self.get_object()

        # 检查权限
        user = request.user
        is_admin = user.is_superuser or (
            hasattr(user, 'profile') and user.profile.position and '负责人' in user.profile.position
        )
        if not is_admin:
            return Response({'detail': '没有审核权限'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResearchReportReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review_status = serializer.validated_data['status']
        review_notes = serializer.validated_data.get('review_notes', '')

        if review_status == 'approved':
            report.approve(user, review_notes)
        else:
            report.reject(user, review_notes)

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布报告"""
        report = self.get_object()

        # 检查权限
        user = request.user
        is_admin = user.is_superuser or (
            hasattr(user, 'profile') and user.profile.position and '负责人' in user.profile.position
        )
        if not is_admin:
            return Response({'detail': '没有发布权限'}, status=status.HTTP_403_FORBIDDEN)
        if report.status != 'approved':
            return Response({'detail': '只有已通过审核的报告才能发布'}, status=status.HTTP_400_BAD_REQUEST)

        report.is_public = True
        report.status = 'published'
        report.published_at = timezone.now()
        report.save()

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """取消发布"""
        report = self.get_object()

        # 检查权限
        user = request.user
        is_admin = user.is_superuser or (
            hasattr(user, 'profile') and user.profile.position and '负责人' in user.profile.position
        )
        if not is_admin:
            return Response({'detail': '没有权限'}, status=status.HTTP_403_FORBIDDEN)

        report.is_public = False
        report.status = 'approved'  # 取消发布后状态变回已通过
        report.save()

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=['post'])
    def toggle_top(self, request, pk=None):
        """置顶/取消置顶"""
        report = self.get_object()

        # 检查权限
        user = request.user
        is_admin = user.is_superuser or (
            hasattr(user, 'profile') and user.profile.position and '负责人' in user.profile.position
        )
        if not is_admin:
            return Response({'detail': '没有权限'}, status=status.HTTP_403_FORBIDDEN)

        report.is_top = not report.is_top
        report.save()

        return Response({'is_top': report.is_top})

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        """增加阅读量"""
        report = self.get_object()
        report.view_count += 1
        report.save()
        return Response({'view_count': report.view_count})
