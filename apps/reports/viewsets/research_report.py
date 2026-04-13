from django.db import models
from django.utils import timezone
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.reports.models import ResearchReport
from apps.reports.permissions import IsConsoleReportUser
from apps.reports.serializers import (
    ResearchReportCreateSerializer,
    ResearchReportListSerializer,
    ResearchReportReviewSerializer,
    ResearchReportSerializer,
)
from utils.authz import is_manager_user, is_researcher_user


class ResearchReportViewSet(viewsets.ModelViewSet):
    """
    研究报告管理视图集
    """

    queryset = ResearchReport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsConsoleReportUser]

    def get_serializer_class(self):
        if self.action == "list":
            return ResearchReportListSerializer
        elif self.action == "create":
            return ResearchReportCreateSerializer
        return ResearchReportSerializer

    def get_queryset(self):
        queryset = ResearchReport.objects.select_related("author", "reviewer")

        user = self.request.user
        if is_manager_user(user):
            queryset = queryset
        elif is_researcher_user(user):
            queryset = queryset.filter(author=user)
        else:
            queryset = queryset.none()

        # 筛选状态
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 筛选是否公开
        is_public = self.request.query_params.get("is_public")
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == "true")

        # 搜索标题
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search)
                | models.Q(strategy_name__icontains=search)
                | models.Q(tags__icontains=search)
            )

        # 筛选策略类型
        strategy_type = self.request.query_params.get("strategy_type")
        if strategy_type:
            queryset = queryset.filter(strategy_type=strategy_type)

        return queryset.order_by("-is_top", "-published_at", "-created_at")

    def _can_edit_report(self, user, report: ResearchReport) -> bool:
        if is_manager_user(user):
            return True
        return report.author_id == user.id and report.status in ["draft", "rejected"]

    def _can_delete_report(self, user, report: ResearchReport) -> bool:
        if is_manager_user(user):
            return report.status in ["draft", "rejected"]
        return report.author_id == user.id and report.status in ["draft", "rejected"]

    def _ensure_manager(self, user):
        if not is_manager_user(user):
            raise exceptions.PermissionDenied("没有权限执行此操作")

    def perform_create(self, serializer):
        report = serializer.save()
        # 草稿提交后自动设为待审核
        if self.request.data.get("submit_for_review"):
            report.status = "pending"
            report.save()

    def perform_update(self, serializer):
        report = serializer.instance
        if not self._can_edit_report(self.request.user, report):
            raise exceptions.PermissionDenied("没有权限编辑此报告")
        # 检查是否要删除图片（前端传 null 表示删除）
        if (
            "detail_image" in serializer.validated_data
            and serializer.validated_data["detail_image"] is None
        ):
            # 删除现有图片文件
            if report.detail_image:
                report.detail_image.delete(save=False)
        serializer.save()

    def perform_destroy(self, instance):
        if not self._can_delete_report(self.request.user, instance):
            raise exceptions.PermissionDenied("没有权限删除此报告")
        instance.delete()

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """提交审核"""
        report = self.get_object()
        if report.author != request.user:
            return Response({"detail": "只能提交自己的报告"}, status=status.HTTP_403_FORBIDDEN)
        if report.status not in ["draft", "rejected"]:
            return Response(
                {"detail": "只有草稿或已拒绝的报告可以提交审核"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report.status = "pending"
        report.save()
        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        """审核报告"""
        report = self.get_object()

        self._ensure_manager(request.user)
        if report.status != "pending":
            return Response(
                {"detail": "只有待审核报告可以审核"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ResearchReportReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review_status = serializer.validated_data["status"]
        review_notes = serializer.validated_data.get("review_notes", "")

        if review_status == "approved":
            report.approve(request.user, review_notes)
        else:
            report.reject(request.user, review_notes)

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        """发布报告"""
        report = self.get_object()

        self._ensure_manager(request.user)
        if report.status != "approved":
            return Response(
                {"detail": "只有已通过审核的报告才能发布"}, status=status.HTTP_400_BAD_REQUEST
            )

        report.is_public = True
        report.status = "published"
        report.published_at = timezone.now()
        report.save()

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        """取消发布"""
        report = self.get_object()

        self._ensure_manager(request.user)

        report.is_public = False
        report.status = "approved"  # 取消发布后状态变回已通过
        report.save()

        return Response(ResearchReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def toggle_top(self, request, pk=None):
        """置顶/取消置顶"""
        report = self.get_object()

        self._ensure_manager(request.user)

        report.is_top = not report.is_top
        report.save()

        return Response({"is_top": report.is_top})

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        """增加阅读量"""
        report = self.get_object()
        report.view_count += 1
        report.save()
        return Response({"view_count": report.view_count})
