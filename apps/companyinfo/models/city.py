#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models

from .province import Province


class City(models.Model):
    """
    市区
    说明：由于从网上下载的区域表格信息复杂，如省直属县，高德地图存在无法识别的情况，因而已删除部分特殊情况的记录，如有需要可以在后台添加
    """

    name = models.CharField(verbose_name="市区", max_length=64)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, verbose_name="省份")

    class Meta:
        verbose_name = "市区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
