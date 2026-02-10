#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserCategory(models.Model):
    """用户类别模型"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="category", verbose_name="用户"
    )

    CATEGORY_CHOICES = [
        ("individual", "个人投资者"),
        ("institutional", "机构投资者"),
        ("partner", "合作伙伴"),
        ("recruiter", "求职者"),
        ("media", "媒体"),
        ("other", "其他"),
    ]
    category = models.CharField(
        "用户类别", max_length=30, choices=CATEGORY_CHOICES, default="individual"
    )

    company = models.CharField("公司/机构名称", max_length=100, blank=True)
    position = models.CharField("职位", max_length=50, blank=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户类别"
        verbose_name_plural = "用户类别"
        db_table = "users_usercategory"

    def __str__(self):
        return f"{self.user.username} - {self.get_category_display()}"
