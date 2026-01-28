from rest_framework import serializers
from django.contrib.auth.models import User
from companyinfo.models import GetMessages, CompanyInfo
from data_apps.models import GenericStockMarketData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericStockMarketData
        fields = ['id', 'stock_code', 'stock_name', 'now_price', 'open_price',
                  'close_price', 'high_price', 'low_price', 'turnover_of_shares',
                  'trading_volume', 'current_time']


class StockDataImportSerializer(serializers.Serializer):
    file = serializers.FileField()
