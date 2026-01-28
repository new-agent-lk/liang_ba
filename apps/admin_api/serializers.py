from rest_framework import serializers
from django.contrib.auth import get_user_model
from companyinfo.models import GetMessages, CompanyInfo
from apps.users.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'province', 'postal_code', 'wechat', 'qq', 
                  'linkedin', 'language', 'timezone', 'theme', 'email_notifications',
                  'sms_notifications', 'push_notifications']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name',
                  'phone', 'avatar', 'avatar_url', 'gender', 'birthday', 'department',
                  'position', 'employee_id', 'is_staff', 'is_superuser', 'is_active',
                  'last_login', 'date_joined', 'created_at', 'updated_at', 'login_count',
                  'last_login_ip', 'bio', 'notes', 'profile']
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 
                          'updated_at', 'login_count', 'last_login_ip']
    
    def get_avatar_url(self, obj):
        return obj.avatar_url if hasattr(obj, 'avatar') and obj.avatar else None
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name',
                  'last_name', 'phone', 'department', 'position', 'is_staff', 'is_superuser']
    
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
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'avatar',
                  'gender', 'birthday', 'department', 'position', 'employee_id',
                  'is_active', 'is_staff', 'is_superuser', 'bio', 'notes', 'profile']
    
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
