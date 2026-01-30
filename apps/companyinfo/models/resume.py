#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from .job_position import JobPosition
from .choices import JOB_CATEGORY_CHOICES, EDUCATION_CHOICES


class Resume(models.Model):
    """收到的简历"""
    # 基本信息
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    email = models.EmailField('电子邮箱')

    # 求职信息
    position = models.ForeignKey(
        JobPosition,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='应聘岗位'
    )
    job_category = models.CharField(
        '应聘职位类别',
        max_length=50,
        choices=JOB_CATEGORY_CHOICES,
        default='other'
    )
    expected_salary = models.CharField('期望薪资', max_length=50, blank=True)

    # 教育信息
    education = models.CharField(
        '最高学历',
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True
    )
    school = models.CharField('毕业院校', max_length=100, blank=True)
    major = models.CharField('专业', max_length=100, blank=True)

    # 工作经历
    work_experience = models.TextField('工作经历', blank=True)
    skills = models.TextField('专业技能', blank=True)

    # 自我介绍
    self_introduction = models.TextField('自我介绍', blank=True)

    # 简历文件
    resume_file = models.FileField(
        '简历文件',
        upload_to='resumes/%Y/%m/',
        null=True,
        blank=True
    )

    # 状态
    STATUS_CHOICES = [
        ('new', '待查看'),
        ('viewed', '已查看'),
        ('interview', '待面试'),
        ('hired', '已录用'),
        ('rejected', '已拒绝'),
        ('withdrawn', '已撤回'),
    ]
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    # 备注
    notes = models.TextField('备注', blank=True)
    reviewed_by = models.CharField('审核人', max_length=100, blank=True)
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)

    # 时间戳
    created_at = models.DateTimeField('投递时间', auto_now_add=True)

    class Meta:
        verbose_name = '收到的简历'
        verbose_name_plural = '简历管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.position if self.position else '未选择岗位'}"
