#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models


class Province(models.Model):
    """省份"""
    name = models.CharField(verbose_name='省份', max_length=64)

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
