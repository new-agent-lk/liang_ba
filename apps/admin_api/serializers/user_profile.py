from rest_framework import serializers
from apps.users.models import UserProfile


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
