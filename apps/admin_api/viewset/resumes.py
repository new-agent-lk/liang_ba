from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django.utils import timezone

from apps.admin_api.serializers import ResumeSerializer, ResumeReviewSerializer
from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import Resume


class ResumeViewSet(viewsets.ModelViewSet):
    """
    简历管理视图集
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Resume.objects.select_related('position').all()

        # 筛选状态
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # 筛选职位类别
        job_category = self.request.query_params.get('job_category')
        if job_category:
            queryset = queryset.filter(job_category=job_category)

        # 搜索姓名或邮箱
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(email__icontains=search)
            )

        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def review(self, request, _pk=None):
        """审核简历"""
        resume = self.get_object()
        serializer = ResumeReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resume.status = serializer.validated_data['status']
        resume.notes = serializer.validated_data.get('review_notes', '')
        resume.reviewed_by = request.user.username
        resume.reviewed_at = timezone.now()
        resume.save()

        return Response(ResumeSerializer(resume).data)
