from rest_framework import status, views
from rest_framework.response import Response

from apps.admin_api.permissions import IsAdminUser
from apps.admin_api.serializers import (
    CompanyInfoSerializer,
    CompanyInfoUpdateSerializer,
)
from apps.companyinfo.models import CompanyInfo


class CompanyInfoView(views.APIView):
    """
    公司信息视图
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        """获取公司信息"""
        company_info = CompanyInfo.objects.first()
        if not company_info:
            return Response({"detail": "公司信息不存在"}, status=status.HTTP_404_NOT_FOUND)
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
