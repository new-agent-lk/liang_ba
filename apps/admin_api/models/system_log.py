"""
System Log Model for Indexing

Stores log metadata for fast filtering and search.
"""
from django.db import models
from utils.models import BaseModel


class LogType(models.TextChoices):
    APP = 'app', 'Application'
    ERROR = 'error', 'Error'
    SECURITY = 'security', 'Security'
    PERFORMANCE = 'performance', 'Performance'
    DJANGO = 'django', 'Django'


class LogLevel(models.TextChoices):
    DEBUG = 'DEBUG', 'Debug'
    INFO = 'INFO', 'Info'
    WARNING = 'WARNING', 'Warning'
    ERROR = 'ERROR', 'Error'
    CRITICAL = 'CRITICAL', 'Critical'


class SystemLogIndex(BaseModel):
    """
    Indexed log entry for fast filtering

    Note: This stores metadata only, not full log content.
    Full content is read from log files.
    """
    # Core fields from log
    timestamp = models.DateTimeField(db_index=True)
    level = models.CharField(max_length=10, choices=LogLevel.choices, db_index=True)
    logger = models.CharField(max_length=255, db_index=True)
    message = models.TextField()

    # Context fields
    trace_id = models.CharField(max_length=64, blank=True, default='-', db_index=True)
    request_id = models.CharField(max_length=32, blank=True, default='-')
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    client_ip = models.GenericIPAddressField(null=True, blank=True)

    # Source file info
    log_type = models.CharField(max_length=20, choices=LogType.choices, db_index=True)
    file_offset = models.BigIntegerField(help_text='Byte offset in log file')
    line_number = models.IntegerField()

    # Processing metadata
    indexed = models.BooleanField(default=True, db_index=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'system_log_index'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['log_type', '-timestamp']),
            models.Index(fields=['trace_id', '-timestamp']),
            models.Index(fields=['level', '-timestamp']),
            models.Index(fields=['user_id', '-timestamp']),
        ]

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message[:50]}"

    @classmethod
    def create_from_parsed(cls, entry, log_type: str, file_offset: int):
        """Create index entry from ParsedLogEntry"""
        return cls(
            timestamp=entry.timestamp,
            level=entry.level.value,
            logger=entry.logger,
            message=entry.message,
            trace_id=entry.trace_id,
            request_id=entry.request_id,
            user_id=entry.user_id,
            log_type=log_type,
            file_offset=file_offset,
            line_number=entry.line,
            extra_data=entry.extra,
        )


class LogRotationConfig(BaseModel):
    """
    Configuration for log rotation settings
    """
    log_type = models.CharField(max_length=20, unique=True, choices=LogType.choices)

    # Rotation settings
    max_size_mb = models.IntegerField(default=10, help_text='Maximum log file size in MB')
    max_files = models.IntegerField(default=10, help_text='Maximum number of archived files')
    max_age_days = models.IntegerField(default=30, help_text='Maximum age of archived files in days')
    compress_old = models.BooleanField(default=True, help_text='Compress old log files')
    enabled = models.BooleanField(default=True, help_text='Enable automatic rotation')

    # Manual override
    last_rotated = models.DateTimeField(null=True, blank=True)
    is_manually_paused = models.BooleanField(default=False)

    class Meta:
        db_table = 'log_rotation_config'
        verbose_name = 'Log Rotation Configuration'
        verbose_name_plural = 'Log Rotation Configurations'

    def __str__(self):
        return f"{self.log_type}: {self.max_size_mb}MB, {self.max_files} files"


class LogViewerAccessLog(BaseModel):
    """
    Audit log for log viewer access
    """
    user_id = models.IntegerField(db_index=True)
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=50, db_index=True)  # view, export, rotate
    log_type = models.CharField(max_length=20, null=True, blank=True)
    filters_applied = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'log_viewer_access_log'
        ordering = ['-create_time']

    def __str__(self):
        return f"{self.username} - {self.action} at {self.create_time}"
