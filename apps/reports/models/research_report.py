#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ResearchReport(models.Model):
    """
    深度研究报告
    包含策略回测结果、指标数据等
    """

    # 报告基本信息
    title = models.CharField('报告标题', max_length=200)
    summary = models.TextField('摘要', blank=True)
    content = models.TextField('报告内容')

    # 策略信息
    strategy_name = models.CharField('策略名称', max_length=100, blank=True)
    strategy_type = models.CharField('策略类型', max_length=50, blank=True)
    market = models.CharField('适用市场', max_length=50, blank=True)

    # 回测指标
    annual_return = models.DecimalField('年化收益率', max_digits=10, decimal_places=2, null=True, blank=True)
    max_drawdown = models.DecimalField('最大回撤', max_digits=10, decimal_places=2, null=True, blank=True)
    sharpe_ratio = models.DecimalField('夏普比率', max_digits=10, decimal_places=2, null=True, blank=True)
    win_rate = models.DecimalField('胜率', max_digits=10, decimal_places=2, null=True, blank=True)
    profit_loss_ratio = models.DecimalField('盈亏比', max_digits=10, decimal_places=2, null=True, blank=True)
    total_trades = models.IntegerField('总交易次数', default=0)

    # 回测时间范围
    backtest_start_date = models.DateField('回测开始日期', null=True, blank=True)
    backtest_end_date = models.DateField('回测结束日期', null=True, blank=True)

    # 策略参数（JSON格式存储）
    strategy_params = models.JSONField('策略参数', default=dict, blank=True)

    # 回测结果图表（图片路径）
    equity_curve_image = models.ImageField('资金曲线图', upload_to='reports/equity/%Y/%m/', null=True, blank=True)
    drawdown_image = models.ImageField('回撤图', upload_to='reports/drawdown/%Y/%m/', null=True, blank=True)
    monthly_returns_image = models.ImageField('月度收益图', upload_to='reports/monthly/%Y/%m/', null=True, blank=True)

    # 首页详情图
    detail_image = models.ImageField('首页详情图', upload_to='reports/detail/%Y/%m/', null=True, blank=True,
        help_text='显示在报告列表页的封面图')

    # 附加文件
    attachment = models.FileField('附件', upload_to='reports/files/%Y/%m/', null=True, blank=True)

    # 标签
    tags = models.CharField('标签', max_length=200, blank=True)

    # 作者
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='research_reports',
        verbose_name='作者'
    )

    # 审核信息
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('published', '已发布'),
    ]
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports',
        verbose_name='审核人',
        null=True,
        blank=True
    )
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)
    review_notes = models.TextField('审核备注', blank=True)

    # 是否公开
    is_public = models.BooleanField('是否公开', default=False)

    # 是否置顶
    is_top = models.BooleanField('是否置顶', default=False)

    # 阅读量
    view_count = models.IntegerField('阅读量', default=0)

    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)

    class Meta:
        verbose_name = '研究报告'
        verbose_name_plural = '研究报告管理'
        ordering = ['-is_top', '-published_at', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.username}"

    def publish(self):
        """发布报告"""
        self.status = 'published'
        self.is_public = True
        self.published_at = timezone.now()
        self.save()

    def approve(self, reviewer, notes=''):
        """通过审核"""
        self.status = 'approved'
        self.reviewer = reviewer
        self.reviewed_at = timezone.now()
        self.review_notes = notes
        self.save()

    def reject(self, reviewer, notes=''):
        """拒绝审核"""
        self.status = 'rejected'
        self.reviewer = reviewer
        self.reviewed_at = timezone.now()
        self.review_notes = notes
        self.save()
