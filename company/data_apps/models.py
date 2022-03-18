import uuid

from django.db import models

from utils.models import BaseModel


class GenericStockMarketData(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock_code = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    stock_name = models.CharField(max_length=255, null=True, blank=True)
    now_price = models.CharField(max_length=255, null=True, blank=True)
    open_price = models.CharField(verbose_name='今日开盘价', max_length=255, null=True, blank=True)
    close_price = models.CharField(verbose_name='昨日收盘价', max_length=255, null=True, blank=True)
    high_price = models.CharField(verbose_name='今日最高价', max_length=255, null=True, blank=True)
    low_price = models.CharField(verbose_name='今日最低价', max_length=255, null=True, blank=True)
    turnover_of_shares = models.CharField(verbose_name='股票成交数', max_length=255, null=True, blank=True)
    trading_volume = models.CharField(verbose_name='成交金额', max_length=255, null=True, blank=True)

    current_time = models.DateTimeField(editable=True, blank=True)
    source_data = models.TextField(default='')

    class Meta:
        verbose_name = '股票市场历史数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stock_name

