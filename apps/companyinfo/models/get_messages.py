#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models


class GetMessages(models.Model):
    """留言管理"""
    name = models.CharField(verbose_name='姓名', max_length=10)
    phone = models.CharField(verbose_name='电话', max_length=15)
    email = models.EmailField(verbose_name='邮箱')
    msg = models.TextField(verbose_name='留言')
    is_handle = models.BooleanField(verbose_name='处理', default=False)

    class Meta:
        verbose_name = '留言管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
