from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    自定义用户模型，扩展Django默认用户
    """
    # 基本信息
    phone = models.CharField('手机号', max_length=11, blank=True, null=True, unique=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    gender = models.CharField('性别', max_length=1, choices=[
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ], blank=True, null=True)
    birthday = models.DateField('生日', blank=True, null=True)
    
    # 工作信息
    department = models.CharField('部门', max_length=50, blank=True, null=True)
    position = models.CharField('职位', max_length=50, blank=True, null=True)
    employee_id = models.CharField('员工编号', max_length=20, blank=True, null=True, unique=True)
    
    # 状态信息
    is_active = models.BooleanField('是否激活', default=True)
    last_login_ip = models.GenericIPAddressField('最后登录IP', blank=True, null=True)
    login_count = models.PositiveIntegerField('登录次数', default=0)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    # 备注信息
    bio = models.TextField('个人简介', blank=True, null=True)
    notes = models.TextField('备注', blank=True, null=True)
    
    # 解决与默认User模型的反向关系冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='组',
        blank=True,
        help_text='该用户所属的组。',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='用户权限',
        blank=True,
        help_text='该用户拥有的特定权限。',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users_customuser'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.username})"
    
    @property
    def avatar_url(self):
        """获取头像URL"""
        if self.avatar:
            return self.avatar.url
        return None
    
    def get_full_name(self):
        """获取全名"""
        full_name = super().get_full_name()
        return full_name or self.username
    
    def update_login_info(self, ip_address=None):
        """更新登录信息"""
        self.last_login = timezone.now()
        if ip_address:
            self.last_login_ip = ip_address
        self.login_count += 1
        self.save(update_fields=['last_login', 'last_login_ip', 'login_count'])


class UserProfile(models.Model):
    """
    用户扩展信息
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户'
    )
    
    # 联系信息
    address = models.CharField('地址', max_length=200, blank=True, null=True)
    city = models.CharField('城市', max_length=50, blank=True, null=True)
    province = models.CharField('省份', max_length=50, blank=True, null=True)
    postal_code = models.CharField('邮编', max_length=10, blank=True, null=True)
    
    # 社交媒体
    wechat = models.CharField('微信号', max_length=50, blank=True, null=True)
    qq = models.CharField('QQ号', max_length=20, blank=True, null=True)
    linkedin = models.URLField('LinkedIn', blank=True, null=True)
    
    # 偏好设置
    language = models.CharField('语言', max_length=10, default='zh-cn')
    timezone = models.CharField('时区', max_length=50, default='Asia/Shanghai')
    theme = models.CharField('主题', max_length=20, default='light', choices=[
        ('light', '浅色'),
        ('dark', '深色'),
        ('auto', '自动'),
    ])
    
    # 通知设置
    email_notifications = models.BooleanField('邮件通知', default=True)
    sms_notifications = models.BooleanField('短信通知', default=False)
    push_notifications = models.BooleanField('推送通知', default=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        db_table = 'users_userprofile'
    
    def __str__(self):
        return f"{self.user.username} 的资料"