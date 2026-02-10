from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsResearcherOrReadOnly(permissions.BasePermission):
    """
    研究员只能编辑自己的报告，其他人只能阅读
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 超级管理员可以编辑任何报告
        if request.user.is_superuser:
            return True
        # 只能编辑自己的报告
        return obj.author == request.user


class CanReviewReport(permissions.BasePermission):
    """
    可以审核报告：超级管理员或部门负责人
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # 超级管理员可以审核
        if request.user.is_superuser:
            return True
        # 部门负责人可以审核
        if hasattr(request.user, "profile"):
            return request.user.profile.position and "负责人" in request.user.profile.position
        return False


class IsAuthorOrReviewer(permissions.BasePermission):
    """
    作者或审核人可以修改报告状态
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 超级管理员可以修改
        if request.user.is_superuser:
            return True
        # 部门负责人可以审核
        if hasattr(request.user, "profile") and request.user.profile.position:
            if "负责人" in request.user.profile.position:
                return True
        # 作者可以修改自己的草稿
        return obj.author == request.user and obj.status == "draft"
