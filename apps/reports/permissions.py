from rest_framework import permissions

from utils.authz import can_access_console, is_manager_user


class IsConsoleReportUser(permissions.BasePermission):
    """
    仅允许后台控制台用户访问研究报告管理
    """

    def has_permission(self, request, view):
        return can_access_console(request.user)


class CanReviewReport(permissions.BasePermission):
    """
    可以审核报告：超级管理员或部门负责人
    """

    def has_permission(self, request, view):
        return is_manager_user(request.user)


class IsAuthorOrReviewer(permissions.BasePermission):
    """
    作者或审核人可以修改报告状态
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if is_manager_user(request.user):
            return True
        # 作者可以修改自己的草稿
        return obj.author == request.user and obj.status == "draft"
