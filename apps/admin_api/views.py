from rest_framework import viewsets, views, status
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import authenticate

from apps.admin_api.serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPasswordChangeSerializer,
    CompanyInfoSerializer, CompanyInfoUpdateSerializer,
    MessageSerializer, MessageReplySerializer,
    ResumeSerializer, ResumeReviewSerializer,
    JobPositionSerializer,
)
from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import GetMessages, CompanyInfo,  Resume, JobPosition
from apps.users.models import UserProfile

User = get_user_model()


class LoginView(views.APIView):
    """
    登录认证视图
    """
    permission_classes = [AllowAny]

    def post(self, request):
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

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    def logout(self, _request):
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
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().select_related('profile')
        username = self.request.query_params.get('username')
        is_active = self.request.query_params.get('is_active')

        if username:
            queryset = queryset.filter(username__icontains=username)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset.order_by('-date_joined')

    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, _pk=None):
        """修改用户密码"""
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': '密码修改成功'})

    @action(detail=True, methods=['post'])
    def toggle_active(self, _request, pk=None):
        """切换用户激活状态"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        status_text = '激活' if user.is_active else '禁用'
        return Response({'detail': f'用户已{status_text}'})
    


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
    def reply(self, request, _pk=None):
        """回复留言"""
        message = self.get_object()
        serializer = MessageReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message.reply = serializer.validated_data['reply']
        message.is_handle = True
        message.save()
        return Response(MessageSerializer(message).data)


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


class ResumeViewSet(viewsets.ModelViewSet):
    """
    简历管理视图集
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Resume.objects.select_related('user', 'reviewed_by').all()

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
                models.Q(email__icontains=search) |
                models.Q(user__username__icontains=search)
            )

        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def review(self, request, _pk=None):
        """审核简历"""
        resume = self.get_object()
        serializer = ResumeReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resume.status = serializer.validated_data['status']
        resume.review_notes = serializer.validated_data.get('review_notes', '')
        resume.reviewed_by = request.user
        resume.reviewed_at = timezone.now()
        resume.save()

        return Response(ResumeSerializer(resume).data)


class JobPositionViewSet(viewsets.ModelViewSet):
    """
    职位管理视图集
    """
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = JobPosition.objects.all()

        # 筛选状态
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # 筛选职位类别
        job_category = self.request.query_params.get('job_category')
        if job_category:
            queryset = queryset.filter(job_category=job_category)

        return queryset.order_by('sort_order', '-created_at')
