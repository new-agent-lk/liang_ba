from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    仅允许管理员用户访问
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsSuperUser(permissions.BasePermission):
    """
    仅允许超级管理员访问
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAuthenticated(permissions.BasePermission):
    """
    允许任何已认证的用户访问
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
