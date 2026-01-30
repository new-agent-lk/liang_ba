#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from .choices import JOB_CATEGORY_CHOICES, RECRUITMENT_TYPE_CHOICES


class JobPosition(models.Model):
    """招聘岗位"""
    title = models.CharField('岗位名称', max_length=100)
    category = models.CharField(
        '岗位类别',
        max_length=50,
        choices=JOB_CATEGORY_CHOICES,
        default='other'
    )
    recruitment_type = models.CharField(
        '招聘类型',
        max_length=20,
        choices=RECRUITMENT_TYPE_CHOICES,
        default='social'
    )
    department = models.CharField('部门', max_length=50, blank=True)
    location = models.CharField('工作地点', max_length=100, blank=True)
    description = models.TextField('岗位职责', blank=True)
    requirements = models.TextField('任职要求', blank=True)
    salary_range = models.CharField('薪资范围', max_length=100, blank=True)

    is_active = models.BooleanField('是否招聘中', default=True)
    sort_order = models.IntegerField('排序', default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '招聘岗位'
        verbose_name_plural = '招聘岗位管理'
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title
