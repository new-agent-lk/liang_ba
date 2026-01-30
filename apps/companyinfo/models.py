#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块

from datetime import datetime

from django.db import models

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


# 招聘相关常量
JOB_CATEGORY_CHOICES = [
    ('quant_dev', '量化开发'),
    ('data_engineer', '数据工程师'),
    ('risk_manager', '风控专员'),
    ('researcher', '研究员'),
    ('it_support', 'IT支持'),
    ('other', '其他'),
]

RECRUITMENT_TYPE_CHOICES = [
    ('campus', '校园招聘'),
    ('social', '社会招聘'),
]

EDUCATION_CHOICES = [
    ('high_school', '高中'),
    ('associate', '大专'),
    ('bachelor', '本科'),
    ('master', '硕士'),
    ('doctor', '博士'),
]


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
