from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.companyinfo.models import GetMessages, CompanyInfo, Resume, JobPosition
from apps.users.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'avatar', 'gender', 'birthday',
            'department', 'position', 'employee_id',
            'address', 'city', 'province', 'postal_code',
            'wechat', 'qq', 'linkedin',
            'bio', 'notes', 'login_count', 'last_login_ip',
            'language', 'timezone_str', 'theme',
            'email_notifications', 'sms_notifications', 'push_notifications',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['login_count', 'last_login_ip', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name',
                  'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined',
                  'profile']
        read_only_fields = ['id', 'date_joined', 'last_login']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name',
                  'last_name', 'is_staff', 'is_superuser']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不一致")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # UserProfile 会通过信号自动创建

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar',
                  'is_active', 'is_staff', 'is_superuser', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # 更新用户信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 更新用户资料
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("新密码不一致")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码错误")
        return value


class CompanyInfoSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.name', read_only=True, allow_null=True)

    class Meta:
        model = CompanyInfo
        fields = ['id', 'name', 'logo', 'logo_url', 'area', 'area_name', 'address',
                  'phone', 'fax', 'postcode', 'email', 'linkman', 'telephone',
                  'digest', 'info', 'honor', 'qrcode', 'qrcode_url', 'weichat',
                  'qq', 'record_nums', 'topimg', 'topimg_url']


class CompanyInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = ['id', 'name', 'logo', 'area', 'address', 'phone', 'fax', 'postcode',
                  'email', 'linkman', 'telephone', 'digest', 'info', 'honor', 'qrcode',
                  'weichat', 'qq', 'record_nums', 'topimg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # 如果是更新，所有图片字段都设为可选
            for field in ['logo', 'qrcode', 'topimg']:
                if field in self.fields:
                    self.fields[field].required = False


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMessages
        fields = ['id', 'name', 'phone', 'email', 'msg', 'is_handle', 'reply', 'add_time']


class MessageReplySerializer(serializers.Serializer):
    reply = serializers.CharField(required=True)


class ResumeSerializer(serializers.ModelSerializer):
    """简历序列化器"""
    job_category_display = serializers.CharField(source='get_job_category_display', read_only=True)
    education_display = serializers.CharField(source='get_education_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    resume_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = [
            'id', 'user', 'user_username', 'name', 'phone', 'email', 'age',
            'job_category', 'job_category_display', 'expected_salary',
            'education', 'education_display', 'school', 'major',
            'work_experience', 'skills', 'self_introduction',
            'resume_file', 'resume_file_url',
            'status', 'status_display', 'review_notes', 'reviewed_by',
            'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'reviewed_at']

    def get_resume_file_url(self, obj):
        if obj.resume_file:
            return obj.resume_file.url
        return None


class ResumeReviewSerializer(serializers.Serializer):
    """简历审核序列化器"""
    status = serializers.ChoiceField(choices=['reviewing', 'approved', 'rejected'])
    review_notes = serializers.CharField(required=False, allow_blank=True)


class JobPositionSerializer(serializers.ModelSerializer):
    """职位序列化器"""
    job_category_display = serializers.CharField(source='get_job_category_display', read_only=True)
    education_required_display = serializers.CharField(source='get_education_required_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = JobPosition
        fields = [
            'id', 'title', 'department', 'job_category', 'job_category_display',
            'location', 'salary_min', 'salary_max', 'salary_display',
            'description', 'requirements', 'responsibilities',
            'experience', 'education_required', 'education_required_display',
            'headcount', 'status', 'status_display', 'sort_order',
            'publish_date', 'expiry_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
