from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from .serializers import (
    UserSerializer, UserCreateSerializer,
    CompanyInfoSerializer, CompanyInfoUpdateSerializer,
    MessageSerializer, MessageReplySerializer,
    StockDataSerializer,
)
from .permissions import IsAdminUser
from companyinfo.models import GetMessages, CompanyInfo
from data_apps.models import GenericStockMarketData


class LoginView(views.APIView):
    """
    登录认证视图
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.path.endswith('/login/'):
            return self.login(request)
        elif request.path.endswith('/logout/'):
            return self.logout(request)
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': '用户名和密码不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {'detail': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 检查用户是否为管理员
        if not user.is_staff:
            return Response(
                {'detail': '您没有权限访问后台管理系统'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 更新最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    def logout(self, request):
        # JWT 是无状态的，客户端只需删除 token
        return Response({'detail': '退出成功'})


class UserInfoView(views.APIView):
    """
    获取当前用户信息视图
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        获取当前登录用户的最新信息
        """
        # 从数据库重新获取用户信息，确保数据是最新的
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data)

    

class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.order_by('-date_joined')

    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        return Response(UserSerializer(request.user).data)


class CompanyInfoView(views.APIView):
    """
    公司信息视图
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        """获取公司信息"""
        company_info = CompanyInfo.objects.first()
        if not company_info:
            return Response({'detail': '公司信息不存在'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyInfoSerializer(company_info)
        return Response(serializer.data)

    def put(self, request):
        """更新公司信息"""
        company_info = CompanyInfo.objects.first()
        if not company_info:
            # 如果不存在，创建新的
            serializer = CompanyInfoUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = CompanyInfoUpdateSerializer(company_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    留言管理视图集
    """
    queryset = GetMessages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = GetMessages.objects.all()
        is_handle = self.request.query_params.get('is_handle')
        if is_handle is not None:
            queryset = queryset.filter(is_handle=is_handle.lower() == 'true')
        return queryset.order_by('-add_time')

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """回复留言"""
        message = self.get_object()
        serializer = MessageReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message.reply = serializer.validated_data['reply']
        message.is_handle = True
        message.save()
        return Response(MessageSerializer(message).data)


class StockDataViewSet(viewsets.ModelViewSet):
    """
    股票数据视图集
    """
    queryset = GenericStockMarketData.objects.all()
    serializer_class = StockDataSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = GenericStockMarketData.objects.all()
        stock_code = self.request.query_params.get('stock_code')
        if stock_code:
            queryset = queryset.filter(stock_code=stock_code)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(current_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(current_time__date__lte=end_date)
        return queryset.order_by('-current_time')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取统计数据"""
        total = self.get_queryset().count()
        latest = self.get_queryset().order_by('-current_time').first()
        return Response({
            'total_records': total,
            'latest_date': latest.current_time if latest else None,
        })

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """批量删除"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'detail': '请选择要删除的记录'}, status=status.HTTP_400_BAD_REQUEST)
        deleted_count, _ = self.get_queryset().filter(id__in=ids).delete()
        return Response({'deleted': deleted_count})


class DashboardStatsView(views.APIView):
    """
    仪表盘统计数据
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = {
            'total_users': User.objects.count(),
            'total_messages': GetMessages.objects.count(),
            'total_stock_data': GenericStockMarketData.objects.count(),
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
