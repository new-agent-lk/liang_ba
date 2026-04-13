from django.contrib.auth import authenticate, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.admin_api.permissions import IsConsoleUser
from apps.admin_api.serializers import UserSelfUpdateSerializer, UserSerializer
from utils.authz import can_access_console

User = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(views.APIView):
    """
    登录认证视图
    """

    permission_classes = [AllowAny]

    def post(self, request):
        if request.path.endswith("/login/"):
            return self.login(request)
        elif request.path.endswith("/logout/"):
            return self.logout(request)
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "用户名和密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"detail": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)

        if not can_access_console(user):
            return Response(
                {"detail": "您没有权限访问后台管理系统"}, status=status.HTTP_403_FORBIDDEN
            )

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )

    def logout(self, _request):
        # JWT 是无状态的，客户端只需删除 token
        return Response({"detail": "退出成功"})


@method_decorator(csrf_exempt, name="dispatch")
class UserInfoView(views.APIView):
    """
    获取当前用户信息视图
    """

    permission_classes = [IsConsoleUser]

    def get(self, request):
        """
        获取当前登录用户的最新信息
        """
        # 从数据库重新获取用户信息，确保数据是最新的
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data)

    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSelfUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.refresh_from_db()
        return Response(UserSerializer(user).data)
