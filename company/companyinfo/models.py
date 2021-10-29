#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块

from datetime import datetime

from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from ckeditor_uploader.fields import RichTextUploadingField  # 富文本编辑器


class Province(models.Model):
    """省份"""
    name = models.CharField(verbose_name='省份', max_length=64)

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class City(models.Model):
    """
    市区
    说明：由于从网上下载的区域表格信息复杂，如省直属县，高德地图存在无法识别的情况，因而已删除部分特殊情况的记录，如有需要可以在后台添加
    """
    name = models.CharField(verbose_name='市区', max_length=64)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, verbose_name='省份')

    class Meta:
        verbose_name = '市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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


class ProductCats(models.Model):
    """产品分类"""
    name = models.CharField(verbose_name='分类名称', max_length=20)

    class Meta:
        verbose_name = '产品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    """产品标签"""
    name = models.CharField(verbose_name='标签', max_length=20)

    class Meta:
        verbose_name = '产品标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Products(models.Model):
    """产品中心"""
    name = models.CharField(verbose_name='产品名称', max_length=100)
    # 产品分类同产品是一对多的关系，所以产品模块定义外键
    category = models.ForeignKey(ProductCats, on_delete=models.CASCADE, null=True, verbose_name='所属分类')
    img = models.ImageField(verbose_name='封面图', upload_to='productpic')
    add_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    click_nums = models.IntegerField(verbose_name='人气', default=0)
    info = RichTextUploadingField('产品内容', default='')
    # 产品同标签属于多对多的关系，所以可以在产品定义外键，方便新增产品时选择标签
    tag = models.ManyToManyField(ProductTags)

    class Meta:
        verbose_name = '产品中心'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductPics(models.Model):
    """产品图片"""
    name = models.CharField(verbose_name='图片名称', max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, verbose_name='所属产品')
    img = models.ImageField(verbose_name='产品图片', upload_to='productpic')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(models.Model):
    """新闻动态"""
    title = models.CharField(verbose_name='标题', max_length=100)
    category = models.CharField(verbose_name='所属分类', choices=(('gsxw', '公司新闻'), ('mtbd', '媒体报道'), ('yggh', '员工关怀')),
                                max_length=4, default='gsxw')
    img = models.ImageField(verbose_name='封面图', upload_to='news')
    add_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    click_nums = models.IntegerField(verbose_name='人气', default=0)
    digest = models.CharField(verbose_name='摘要', max_length=50, default='')
    info = RichTextUploadingField('新闻内容', default='')
    fav_nums = models.IntegerField(verbose_name='点赞数', default=0)
    oppose_nums = models.IntegerField(verbose_name='反对数', default=0)

    class Meta:
        verbose_name = '新闻动态'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Projects(models.Model):
    """工程案例"""
    title = models.CharField(verbose_name='标题', max_length=100)
    category = models.CharField(verbose_name='所属分类',
                                choices=(('trxf', '土壤修复类'), ('wszl', '污水治理类'), ('shlj', '生活垃圾发电类')),
                                max_length=4, default='trxf')
    img = models.ImageField(verbose_name='封面图', upload_to='projects')
    add_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    click_nums = models.IntegerField(verbose_name='人气', default=0)
    digest = models.CharField(verbose_name='摘要', max_length=60, default='')
    info = RichTextUploadingField('工程内容', default='')
    fav_nums = models.IntegerField(verbose_name='点赞数', default=0)
    oppose_nums = models.IntegerField(verbose_name='反对数', default=0)

    class Meta:
        verbose_name = '工程案例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Recruits(models.Model):
    """人才招聘"""
    category = models.CharField(verbose_name='所属分类', choices=(('rcln', '人才理念'), ('zwfb', '职位发布')),
                                max_length=4, default='rcln')
    info = RichTextUploadingField('内容', default='')

    class Meta:
        verbose_name = '人才招聘'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class Carousls(models.Model):
    """轮播图"""
    title = models.CharField(verbose_name='标题', max_length=100, default='')
    img = models.ImageField(verbose_name='轮播图', upload_to='carousls')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Advantages(models.Model):
    """产品优势"""
    title = models.CharField(verbose_name='标题', max_length=10, default='产品优势')
    img = models.ImageField(verbose_name='图标', upload_to='advantages')
    info = models.CharField(verbose_name='内容', max_length=50, default='产品优势')

    class Meta:
        verbose_name = '产品优势'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class IndexAsk(models.Model):
    """首页咨询"""
    title = models.CharField(verbose_name='标题', max_length=25)
    info = models.CharField(verbose_name='内容', max_length=50)

    class Meta:
        verbose_name = '首页咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FriendlyLinks(models.Model):
    """友情链接"""
    title = models.CharField(verbose_name='标题', max_length=10)
    friendly_link = models.URLField(verbose_name='链接')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


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


class Comments(models.Model):
    """评论管理"""
    ip = models.CharField(verbose_name='游客IP', max_length=50)
    msg = models.CharField(verbose_name='留言', max_length=200)
    add_time = models.DateTimeField(verbose_name='时间', default=datetime.now)
    category = models.CharField(verbose_name='评论分类', choices=(('cp', '产品'), ('xw', '新闻'), ('al', '案例')),
                                max_length=2, default='cp')
    obj_pk = models.IntegerField(verbose_name='评论对象')
    reply = models.TextField(verbose_name='回复', default='')
    is_display = models.BooleanField(verbose_name='是否显示', default=False)

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip
