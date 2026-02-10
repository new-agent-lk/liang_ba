from rest_framework import serializers

from apps.companyinfo.models import JobPosition


class JobPositionSerializer(serializers.ModelSerializer):
    """职位序列化器"""

    category_display = serializers.CharField(source="get_category_display", read_only=True)
    recruitment_type_display = serializers.CharField(
        source="get_recruitment_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = JobPosition
        fields = [
            "id",
            "title",
            "category",
            "category_display",
            "recruitment_type",
            "recruitment_type_display",
            "department",
            "location",
            "description",
            "requirements",
            "salary_range",
            "status",
            "status_display",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
