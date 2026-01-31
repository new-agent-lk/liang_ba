from rest_framework import views
from rest_framework.response import Response

from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import GetMessages
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardStatsView(views.APIView):
    """
    仪表盘统计数据
    """
    permission_classes = [IsAdminUser]

    def get(self, _request):
        stats = {
            'total_users': User.objects.count(),
            'total_messages': GetMessages.objects.count(),
            'recent_activities': self.get_recent_activities(),
        }
        return Response(stats)

    def get_recent_activities(self):
        """获取最近活动"""
        activities = []

        # 最近收到的留言
        recent_messages = GetMessages.objects.order_by('-add_time')[:10]
        for m in recent_messages:
            activities.append({
                'id': f'message_{m.id}',
                'type': 'message',
                'content': f'收到来自 {m.name} 的留言',
                'created_at': m.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 按时间排序并返回前10条
        activities.sort(key=lambda x: x['created_at'], reverse=True)
        return activities[:10]
