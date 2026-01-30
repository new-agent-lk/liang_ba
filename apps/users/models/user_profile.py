#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户'
    )

    # 基本信息
    phone = models.CharField('联系电话', max_length=20, blank=True, null=True)
    avatar = models.ImageField('头像', upload_to='avatars/%Y/%m/', blank=True, null=True)
    gender = models.CharField('性别', max_length=10, choices=[
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ], blank=True, null=True)
    birthday = models.DateField('生日', blank=True, null=True)

    # 职位信息
    department = models.CharField('部门', max_length=50, blank=True, null=True)
    position = models.CharField('职位', max_length=50, blank=True, null=True)
    employee_id = models.CharField('员工ID', max_length=50, blank=True, null=True)

    # 联系信息
    address = models.CharField('地址', max_length=200, blank=True, null=True)
    city = models.CharField('城市', max_length=50, blank=True, null=True)
    province = models.CharField('省份', max_length=50, blank=True, null=True)
    postal_code = models.CharField('邮编', max_length=10, blank=True, null=True)

    # 社交媒体
    wechat = models.CharField('微信号', max_length=50, blank=True, null=True)
    qq = models.CharField('QQ号', max_length=20, blank=True, null=True)
    linkedin = models.URLField('LinkedIn', blank=True, null=True)

    # 其他信息
    bio = models.TextField('个人简介', blank=True, null=True)
    notes = models.TextField('备注', blank=True, null=True)
    login_count = models.IntegerField('登录次数', default=0)
    last_login_ip = models.GenericIPAddressField('最后登录IP', blank=True, null=True)

    # 偏好设置
    language = models.CharField('语言', max_length=10, default='zh-cn')
    timezone_str = models.CharField('时区', max_length=50, default='Asia/Shanghai')
    theme = models.CharField('主题', max_length=20, default='light', choices=[
        ('light', '浅色'),
        ('dark', '深色'),
        ('auto', '自动'),
    ])

    # 通知设置
    email_notifications = models.BooleanField('邮件通知', default=True)
    sms_notifications = models.BooleanField('短信通知', default=False)
    push_notifications = models.BooleanField('推送通知', default=True)

    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        db_table = 'users_userprofile'

    def __str__(self):
        return f"{self.user.username} 的资料"
