from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.response import Response

from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import JobPosition, Resume

User = get_user_model()


class DashboardStatsView(views.APIView):
    """
    仪表盘统计数据
    """

    permission_classes = [IsAdminUser]

    def get(self, _request):
        stats = {
            "total_users": User.objects.count(),
            "total_jobs": JobPosition.objects.count(),
            "total_resumes": Resume.objects.count(),
            "recent_activities": self.get_recent_activities(),
        }
        return Response(stats)

    def get_recent_activities(self):
        """获取最近活动"""
        activities = []

        # 按时间排序并返回前10条
        activities.sort(key=lambda x: x["created_at"], reverse=True)
        return activities[:10]
