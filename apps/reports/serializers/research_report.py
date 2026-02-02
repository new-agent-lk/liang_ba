import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from apps.reports.models import ResearchReport


class Base64ImageField(serializers.ImageField):
    """自定义字段：将图片转换为 base64 数据返回"""

    def to_representation(self, value):
        if not value:
            return None

        # 读取图片文件并转换为 base64
        try:
            # 获取文件路径
            if hasattr(value, 'path'):
                file_path = value.path
            elif hasattr(value, 'url'):
                # 获取文件的完整路径
                from django.conf import settings
                import os
                file_path = os.path.join(settings.MEDIA_ROOT, value.name)
            else:
                return None

            # 读取文件并编码为 base64
            with open(file_path, 'rb') as f:
                image_data = f.read()
                ext = file_path.split('.')[-1].lower()
                if ext == 'jpg':
                    ext = 'jpeg'
                mime_type = f'image/{ext}'
                base64_data = base64.b64encode(image_data).decode('utf-8')
                return f'data:{mime_type};base64,{base64_data}'
        except Exception:
            # 如果读取失败，返回原始 URL 作为备选
            try:
                if hasattr(value, 'url'):
                    request = self.context.get('request')
                    if request:
                        return request.build_absolute_uri(value.url)
                    return value.url
            except Exception:
                pass
        return None

    def to_internal_value(self, data):
        # 处理 null 值
        if data is None:
            return None
        # 处理 base64 数据
        if isinstance(data, str) and data.startswith('data:image'):
            # 解码 base64 图片数据
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'upload.{ext}')
        return super().to_internal_value(data)


class ResearchReportListSerializer(serializers.ModelSerializer):
    """报告列表序列化器（精简版）"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    detail_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = ResearchReport
        fields = [
            'id', 'title', 'summary', 'strategy_name', 'strategy_type',
            'annual_return', 'max_drawdown', 'sharpe_ratio',
            'author_username', 'status', 'status_display',
            'is_public', 'is_top', 'view_count',
            'created_at', 'published_at', 'content', 'detail_image'
        ]


class ResearchReportSerializer(serializers.ModelSerializer):
    """报告详情序列化器（完整版）"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    detail_image = Base64ImageField(required=False, allow_null=True)
    equity_curve_image = Base64ImageField(required=False, allow_null=True)
    drawdown_image = Base64ImageField(required=False, allow_null=True)
    monthly_returns_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = ResearchReport
        fields = [
            'id', 'title', 'summary', 'content',
            'strategy_name', 'strategy_type', 'market',
            'annual_return', 'max_drawdown', 'sharpe_ratio',
            'win_rate', 'profit_loss_ratio', 'total_trades',
            'backtest_start_date', 'backtest_end_date',
            'strategy_params',
            'equity_curve_image', 'drawdown_image', 'monthly_returns_image',
            'detail_image',
            'attachment', 'tags',
            'author', 'author_username',
            'status', 'status_display',
            'reviewer', 'reviewer_username', 'reviewed_at', 'review_notes',
            'is_public', 'is_top', 'view_count',
            'created_at', 'updated_at', 'published_at',
        ]
        read_only_fields = [
            'author', 'view_count', 'created_at', 'updated_at',
            'reviewer', 'reviewed_at',
        ]


class ResearchReportCreateSerializer(serializers.ModelSerializer):
    """创建报告序列化器"""

    class Meta:
        model = ResearchReport
        fields = [
            'title', 'summary', 'content',
            'strategy_name', 'strategy_type', 'market',
            'annual_return', 'max_drawdown', 'sharpe_ratio',
            'win_rate', 'profit_loss_ratio', 'total_trades',
            'backtest_start_date', 'backtest_end_date',
            'strategy_params',
            'equity_curve_image', 'drawdown_image', 'monthly_returns_image',
            'detail_image',
            'attachment', 'tags',
        ]

    def create(self, validated_data):
        # 设置作者为当前用户
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class ResearchReportReviewSerializer(serializers.Serializer):
    """审核报告序列化器"""
    STATUS_CHOICES = ['approved', 'rejected']

    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=True)
    review_notes = serializers.CharField(required=False, allow_blank=True)
