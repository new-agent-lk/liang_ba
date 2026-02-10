"""
Log Serializers

Serializers for log viewing API
"""

from rest_framework import serializers

from apps.admin_api.models.system_log import (
    LogLevel,
    LogRotationConfig,
    LogType,
    LogViewerAccessLog,
)


class ParsedLogEntrySerializer(serializers.Serializer):
    """Serializer for parsed log entries from files"""

    timestamp = serializers.DateTimeField()
    level = serializers.CharField()
    logger = serializers.CharField()
    message = serializers.CharField()
    module = serializers.CharField(required=False, allow_blank=True)
    function = serializers.CharField(required=False, allow_blank=True)
    line = serializers.IntegerField(required=False, default=0)
    process_id = serializers.IntegerField(required=False, default=0)
    thread_id = serializers.IntegerField(required=False, default=0)
    trace_id = serializers.CharField(required=False, allow_blank=True)
    request_id = serializers.CharField(required=False, allow_blank=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    extra = serializers.DictField(required=False, default=dict)


class LogListQuerySerializer(serializers.Serializer):
    """Serializer for log list query parameters"""

    log_type = serializers.ChoiceField(choices=LogType.choices, default="app")
    level = serializers.ChoiceField(choices=LogLevel.choices, required=False, allow_blank=True)
    trace_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    search = serializers.CharField(required=False, max_length=500)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    offset = serializers.IntegerField(min_value=0, default=0)
    limit = serializers.IntegerField(min_value=1, max_value=500, default=100)


class LogListResponseSerializer(serializers.Serializer):
    """Serializer for log list response"""

    entries = ParsedLogEntrySerializer(many=True)
    total = serializers.IntegerField()
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()
    has_more = serializers.BooleanField()


class LogStatsSerializer(serializers.Serializer):
    """Serializer for log statistics"""

    file_path = serializers.CharField()
    file_size_mb = serializers.FloatField()
    last_modified = serializers.CharField()
    level_counts = serializers.DictField()
    total_entries = serializers.IntegerField()


class LogRotationConfigSerializer(serializers.ModelSerializer):
    """Serializer for rotation configuration"""

    class Meta:
        model = LogRotationConfig
        fields = [
            "id",
            "log_type",
            "max_size_mb",
            "max_files",
            "max_age_days",
            "compress_old",
            "enabled",
            "last_rotated",
            "is_manually_paused",
            "create_time",
        ]
        read_only_fields = ["id", "create_time"]


class LogRotationStatusSerializer(serializers.Serializer):
    """Serializer for rotation status response"""

    log_type = serializers.CharField()
    policy = serializers.DictField()
    current_size_mb = serializers.FloatField()
    last_modified = serializers.CharField(allow_blank=True)
    archived_files_count = serializers.IntegerField()
    archived_files = serializers.ListField(child=serializers.DictField())


class LogRotationActionSerializer(serializers.Serializer):
    """Serializer for rotation action request"""

    action = serializers.ChoiceField(choices=["rotate", "pause", "resume"])
    log_type = serializers.ChoiceField(choices=LogType.choices)

    def validate(self, data):
        if data["action"] in ["pause", "resume"] and not data.get("log_type"):
            raise serializers.ValidationError("log_type required for pause/resume")
        return data


class LogViewerAccessLogSerializer(serializers.ModelSerializer):
    """Serializer for access audit log"""

    class Meta:
        model = LogViewerAccessLog
        fields = [
            "id",
            "user_id",
            "username",
            "action",
            "log_type",
            "filters_applied",
            "ip_address",
            "user_agent",
            "create_time",
        ]
