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
    ProductCategorySerializer, ProductSerializer, ProductCreateUpdateSerializer,
    NewsSerializer, NewsCreateUpdateSerializer,
    CaseSerializer, CaseCreateUpdateSerializer,
    CarouselSerializer, CarouselCreateUpdateSerializer,
    MessageSerializer, MessageReplySerializer,
    StockDataSerializer,
    ProvinceSerializer, CitySerializer,
)
from .permissions import IsAdminUser
from companyinfo.models import (
    ProductCats, Products, News, Projects, Carousls, GetMessages
)
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

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/me/'):
            return self.get_current_user(request)
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

    def get_current_user(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({'detail': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)


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


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    产品分类视图集
    """
    queryset = ProductCats.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductCats.objects.all().order_by('id')


class ProductViewSet(viewsets.ModelViewSet):
    """
    产品管理视图集
    """
    queryset = Products.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Products.objects.select_related('category').prefetch_related('tag')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('-add_time')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """上传产品图片"""
        product = self.get_object()
        # 图片上传逻辑
        return Response({'detail': '图片上传成功'})


class NewsViewSet(viewsets.ModelViewSet):
    """
    新闻管理视图集
    """
    queryset = News.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        return NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset.order_by('-add_time')


class CaseViewSet(viewsets.ModelViewSet):
    """
    案例管理视图集
    """
    queryset = Projects.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CaseCreateUpdateSerializer
        return CaseSerializer

    def get_queryset(self):
        queryset = Projects.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset.order_by('-add_time')


class CarouselViewSet(viewsets.ModelViewSet):
    """
    轮播图管理视图集
    """
    queryset = Carousls.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarouselCreateUpdateSerializer
        return CarouselSerializer

    def get_queryset(self):
        queryset = Carousls.objects.all()
        return queryset.order_by('-id')


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
            'total_products': Products.objects.count(),
            'total_news': News.objects.count(),
            'total_cases': Projects.objects.count(),
            'total_messages': GetMessages.objects.count(),
            'recent_activities': self.get_recent_activities(),
        }
        return Response(stats)

    def get_recent_activities(self):
        """获取最近活动"""
        activities = []

        # 最近添加的产品
        recent_products = Products.objects.order_by('-add_time')[:3]
        for p in recent_products:
            activities.append({
                'id': f'product_{p.id}',
                'type': 'create',
                'content': f'创建了产品: {p.name}',
                'created_at': p.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 最近添加的新闻
        recent_news = News.objects.order_by('-add_time')[:3]
        for n in recent_news:
            activities.append({
                'id': f'news_{n.id}',
                'type': 'create',
                'content': f'发布了新闻: {n.title}',
                'created_at': n.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 最近添加的案例
        recent_cases = Projects.objects.order_by('-add_time')[:3]
        for c in recent_cases:
            activities.append({
                'id': f'case_{c.id}',
                'type': 'create',
                'content': f'添加了案例: {c.title}',
                'created_at': c.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 最近收到的留言
        recent_messages = GetMessages.objects.order_by('-add_time')[:3]
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
