from django.db import models


class FactorComputation(models.Model):
    """因子计算记录"""
    name = models.CharField('因子名称', max_length=100)
    symbol = models.CharField('股票代码', max_length=20)
    date = models.DateField('日期')
    value = models.FloatField('因子值')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '因子计算'
        verbose_name_plural = '因子计算'
        indexes = [
            models.Index(fields=['name', 'symbol', 'date']),
        ]

    def __str__(self):
        return f"{self.name} - {self.symbol} - {self.date}"


class BacktestResult(models.Model):
    """回测结果"""
    name = models.CharField('策略名称', max_length=100)
    initial_capital = models.FloatField('初始资金', default=1000000)
    final_value = models.FloatField('最终价值')
    total_return = models.FloatField('总收益率(%)')
    annual_return = models.FloatField('年化收益率(%)')
    max_drawdown = models.FloatField('最大回撤(%)')
    sharpe_ratio = models.FloatField('夏普比率')
    win_rate = models.FloatField('胜率(%)')
    params = models.JSONField('策略参数', default=dict)
    result_data = models.JSONField('结果数据', default=dict)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '回测结果'
        verbose_name_plural = '回测结果'

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
