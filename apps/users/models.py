from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

JOB_CATEGORY_CHOICES = [
    ('quant_dev', '量化开发'),
    ('data_engineer', '数据工程师'),
    ('risk_manager', '风控专员'),
    ('researcher', '研究员'),
    ('it_support', 'IT支持'),
    ('other', '其他'),
]

EDUCATION_CHOICES = [
    ('high_school', '高中'),
    ('associate', '大专'),
    ('bachelor', '本科'),
    ('master', '硕士'),
    ('doctor', '博士'),
]


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


class Resume(models.Model):
    """简历模型 - 管理招聘投递的简历"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='提交用户'
    )

    # 基本信息
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    email = models.EmailField('电子邮箱')
    age = models.IntegerField('年龄', null=True, blank=True)

    # 求职信息
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

    # 简历文件
    resume_file = models.FileField(
        '简历文件',
        upload_to='resumes/%Y/%m/',
        null=True,
        blank=True
    )

    # 自我介绍
    self_introduction = models.TextField('自我介绍', blank=True)

    # 状态
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('reviewing', '审核中'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 审核信息
    review_notes = models.TextField('审核备注', blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_resumes',
        verbose_name='审核人'
    )
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)

    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '简历管理'
        verbose_name_plural = '简历管理'
        ordering = ['-created_at']
        db_table = 'users_resume'

    def __str__(self):
        return f"{self.name} - {self.get_job_category_display()}"

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_approved(self):
        return self.status == 'approved'


class UserCategory(models.Model):
    """用户类别模型"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='用户'
    )

    CATEGORY_CHOICES = [
        ('individual', '个人投资者'),
        ('institutional', '机构投资者'),
        ('partner', '合作伙伴'),
        ('recruiter', '求职者'),
        ('media', '媒体'),
        ('other', '其他'),
    ]
    category = models.CharField(
        '用户类别',
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='individual'
    )

    company = models.CharField('公司/机构名称', max_length=100, blank=True)
    position = models.CharField('职位', max_length=50, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户类别'
        verbose_name_plural = '用户类别'
        db_table = 'users_usercategory'

    def __str__(self):
        return f"{self.user.username} - {self.get_category_display()}"


class JobPosition(models.Model):
    """职位模型 - 管理招聘职位"""
    title = models.CharField('职位名称', max_length=100)
    department = models.CharField('部门', max_length=50, blank=True)
    job_category = models.CharField(
        '职位类别',
        max_length=50,
        choices=JOB_CATEGORY_CHOICES
    )
    location = models.CharField('工作地点', max_length=100, blank=True)

    # 薪资范围
    salary_min = models.CharField('最低薪资', max_length=20, blank=True)
    salary_max = models.CharField('最高薪资', max_length=20, blank=True)
    salary_display = models.CharField('薪资显示', max_length=50, blank=True)

    # 职位描述
    description = models.TextField('职位描述')
    requirements = models.TextField('任职要求')
    responsibilities = models.TextField('工作职责', blank=True)

    # 职位详情
    experience = models.CharField('经验要求', max_length=50, blank=True)
    education_required = models.CharField(
        '学历要求',
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True
    )
    headcount = models.IntegerField('招聘人数', default=1)

    # 状态
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('active', '招聘中'),
        ('paused', '暂停招聘'),
        ('closed', '已关闭'),
    ]
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # 排序
    sort_order = models.IntegerField('排序', default=0)

    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    publish_date = models.DateField('发布日期', null=True, blank=True)
    expiry_date = models.DateField('截止日期', null=True, blank=True)

    class Meta:
        verbose_name = '职位管理'
        verbose_name_plural = '职位管理'
        ordering = ['sort_order', '-created_at']
        db_table = 'users_jobposition'

    def __str__(self):
        return self.title
