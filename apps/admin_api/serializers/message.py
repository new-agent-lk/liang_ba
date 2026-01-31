from rest_framework import serializers
from apps.companyinfo.models import GetMessages


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMessages
        fields = ['id', 'name', 'phone', 'email', 'msg', 'is_handle', 'reply', 'add_time']


class MessageReplySerializer(serializers.Serializer):
    reply = serializers.CharField(required=True)
