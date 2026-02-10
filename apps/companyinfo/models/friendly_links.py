#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models


class FriendlyLinks(models.Model):
    """友情链接"""

    title = models.CharField(verbose_name="标题", max_length=10)
    friendly_link = models.URLField(verbose_name="链接")

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
