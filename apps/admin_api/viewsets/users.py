from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.admin_api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserPasswordChangeSerializer,
)
from apps.admin_api.permissions import IsAdminUser

from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
        department = self.request.query_params.get('department')
        position = self.request.query_params.get('position')
        is_staff = self.request.query_params.get('is_staff')
        is_superuser = self.request.query_params.get('is_superuser')

        if username:
            queryset = queryset.filter(username__icontains=username)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if department:
            queryset = queryset.filter(profile__department=department)
        if position:
            queryset = queryset.filter(profile__position=position)
        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff.lower() == 'true')
        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser.lower() == 'true')

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
