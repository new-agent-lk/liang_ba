from rest_framework import serializers
from apps.companyinfo.models import CompanyInfo


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
