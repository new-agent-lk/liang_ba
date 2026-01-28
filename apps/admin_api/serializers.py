from rest_framework import serializers
from django.contrib.auth.models import User
from companyinfo.models import (
    Province, City, ProductCats, ProductTags, Products, ProductPics,
    News, Projects, Carousls, Advantages, IndexAsk, FriendlyLinks,
    GetMessages, Comments, CompanyInfo, Recruits
)
from data_apps.models import GenericStockMarketData, BlastStockMarketData


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


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'province_name']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCats
        fields = ['id', 'name']


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTags
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'name', 'category', 'category_name', 'tag', 'tag_names',
                  'img', 'img_url', 'add_time', 'click_nums', 'info']

    def get_tag_names(self, obj):
        return list(obj.tag.values_list('name', flat=True))


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'category', 'tag', 'img', 'info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.img:
            self.fields['img'].required = False


class ProductPicSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductPics
        fields = ['id', 'name', 'product', 'product_name', 'img', 'img_url']


class NewsSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'category', 'category_display', 'img', 'img_url',
                  'add_time', 'click_nums', 'digest', 'info', 'fav_nums',
                  'oppose_nums']


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'category', 'img', 'digest', 'info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.img:
            self.fields['img'].required = False


class CaseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Projects
        fields = ['id', 'title', 'category', 'category_display', 'img', 'img_url',
                  'add_time', 'click_nums', 'digest', 'info', 'fav_nums',
                  'oppose_nums']


class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'category', 'img', 'digest', 'info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.img:
            self.fields['img'].required = False


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousls
        fields = ['id', 'title', 'img', 'img_url', 'link']


class CarouselCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousls
        fields = ['id', 'title', 'img', 'link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.img:
            self.fields['img'].required = False


class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantages
        fields = ['id', 'title', 'img', 'img_url', 'info']


class IndexAskSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexAsk
        fields = ['id', 'title', 'info']


class FriendlyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendlyLinks
        fields = ['id', 'title', 'friendly_link']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMessages
        fields = ['id', 'name', 'phone', 'email', 'msg', 'is_handle', 'reply', 'add_time']


class MessageReplySerializer(serializers.Serializer):
    reply = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'ip', 'msg', 'add_time', 'category', 'category_display',
                  'obj_pk', 'reply', 'is_display']


class CompanyInfoSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.name', read_only=True)

    class Meta:
        model = CompanyInfo
        fields = ['id', 'name', 'logo', 'logo_url', 'area', 'area_name', 'address',
                  'phone', 'fax', 'postcode', 'email', 'linkman', 'telephone',
                  'digest', 'info', 'honor', 'qrcode', 'qrcode_url', 'weichat',
                  'qq', 'record_nums', 'topimg', 'topimg_url']


class RecruitSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Recruits
        fields = ['id', 'category', 'category_display', 'info']


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericStockMarketData
        fields = ['id', 'stock_code', 'stock_name', 'now_price', 'open_price',
                  'close_price', 'high_price', 'low_price', 'turnover_of_shares',
                  'trading_volume', 'current_time']


class StockDataImportSerializer(serializers.Serializer):
    file = serializers.FileField()
