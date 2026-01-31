from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.admin_api.serializers import MessageSerializer, MessageReplySerializer
from apps.admin_api.permissions import IsAdminUser
from apps.companyinfo.models import GetMessages


class MessageViewSet(viewsets.ModelViewSet):
    """
    留言管理视图集
    """
    queryset = GetMessages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = GetMessages.objects.all()
        is_handle = self.request.query_params.get('is_handle')
        if is_handle is not None:
            queryset = queryset.filter(is_handle=is_handle.lower() == 'true')
        return queryset.order_by('-add_time')

    @action(detail=True, methods=['post'])
    def reply(self, request, _pk=None):
        """回复留言"""
        message = self.get_object()
        serializer = MessageReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message.reply = serializer.validated_data['reply']
        message.is_handle = True
        message.save()
        return Response(MessageSerializer(message).data)
