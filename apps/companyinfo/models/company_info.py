#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from .city import City


class CompanyInfo(models.Model):
    """公司信息"""
    """
    各属性定义时，常用参数说明：
    verbose_name：最常用的元数据之一！用于自定义该属性在后台显示的名称
    max_length：该属性的最大长度
    blak：表示该属性在数据库中可以为空，如果没有这个参数，说明该属性时必填项
    default：默认值
    upload_to：上传路径，基于media文件夹内
    choices：定义选择项（当前model没用到，后面有）
    """
    name = models.CharField(verbose_name='公司名称', max_length=50,
                            default='北京源码商城有限公司')  # 定义姓名字段，当前设置可在数据库相应的表中创建一个name字段，字符类型，长度为50
    logo = models.ImageField(verbose_name='logo', upload_to='companyinfo')  # 使用图片类型时，必需pillow依赖包
    area = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name='市区')
    address = models.CharField(verbose_name='详细地址', max_length=200, default='')
    phone = models.CharField(verbose_name='电话', max_length=15, default='+86 0000 96877')
    fax = models.CharField(verbose_name='传真', max_length=15, default='+86 0000 96877')
    postcode = models.CharField(verbose_name='邮编', max_length=15, default='000000')
    email = models.EmailField(verbose_name='邮箱', default='')
    linkman = models.CharField(verbose_name='联系人', max_length=10, default='梦小白')
    telephone = models.CharField(verbose_name='联系电话', max_length=15, default='+86 0000 96877')
    digest = models.CharField(verbose_name='关于我们摘要', max_length=300, default='')
    info = RichTextUploadingField('公司简介', default='')  # 使用富文本编辑器
    honor = RichTextUploadingField('荣誉资质', default='')  # 使用富文本编辑器
    qrcode = models.ImageField(verbose_name='微信二维码', upload_to='companyinfo')
    weichat = models.CharField(verbose_name='微信号', max_length=50, default='')
    qq = models.CharField(verbose_name='客服QQ', max_length=15, default='888888888')
    record_nums = models.CharField(verbose_name='备案号', max_length=50, default='京ICP备00000000号')
    topimg = models.ImageField(verbose_name='非首页顶长图', upload_to='companyinfo')

    class Meta:  # 元类，可定义该模块的基本信息
        verbose_name = '公司信息'
        verbose_name_plural = verbose_name

    def __str__(self):  # 当print输出实例对象，或str() 实例对象时，调用这个方法
        return self.name

    @property
    def current_year(self):
        return datetime.now().year

    @property
    def logo_url(self):
        """返回logo的完整URL"""
        if self.logo:
            return self.logo.url
        return None

    @property
    def qrcode_url(self):
        """返回微信二维码的完整URL"""
        if self.qrcode:
            return self.qrcode.url
        return None

    @property
    def topimg_url(self):
        """返回非首页顶长图的完整URL"""
        if self.topimg:
            return self.topimg.url
        return None
