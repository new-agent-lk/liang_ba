from rest_framework import serializers
from apps.reports.models import ResearchReport


class ResearchReportListSerializer(serializers.ModelSerializer):
    """报告列表序列化器（精简版）"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

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
