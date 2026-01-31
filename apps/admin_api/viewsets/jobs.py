from rest_framework import viewsets

from apps.admin_api.serializers import JobPositionSerializer
from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import JobPosition


class JobPositionViewSet(viewsets.ModelViewSet):
    """
    职位管理视图集
    """
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = JobPosition.objects.all()

        # 筛选状态 (is_active)
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')

        # 筛选职位类别
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # 筛选招聘类型
        recruitment_type = self.request.query_params.get('recruitment_type')
        if recruitment_type:
            queryset = queryset.filter(recruitment_type=recruitment_type)

        return queryset.order_by('sort_order', '-created_at')
