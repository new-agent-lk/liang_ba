from rest_framework import serializers

from apps.companyinfo.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    """简历序列化器"""

    job_category_display = serializers.CharField(source="get_job_category_display", read_only=True)
    education_display = serializers.CharField(source="get_education_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    position_title = serializers.CharField(source="position.title", read_only=True, allow_null=True)
    resume_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "job_category",
            "job_category_display",
            "expected_salary",
            "education",
            "education_display",
            "school",
            "major",
            "work_experience",
            "skills",
            "self_introduction",
            "resume_file",
            "resume_file_url",
            "position",
            "position_title",
            "status",
            "status_display",
            "notes",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "reviewed_at"]

    def get_resume_file_url(self, obj):
        if obj.resume_file:
            return obj.resume_file.url
        return None


class ResumeReviewSerializer(serializers.Serializer):
    """简历审核序列化器"""

    status = serializers.ChoiceField(choices=["reviewing", "approved", "rejected"])
    review_notes = serializers.CharField(required=False, allow_blank=True)
