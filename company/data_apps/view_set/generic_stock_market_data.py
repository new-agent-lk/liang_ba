# -*- coding: utf-8 -*-
import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework.viewsets import ModelViewSet

from data_apps.models import GenericStockMarketData
from data_apps.serializers.generic_stock_market_data import GenericStockMarketDataSerializer


class GenericStockMarketDataFilter(FilterSet):
    create_time = django_filters.DateTimeFromToRangeFilter(field_name='create_time', lookup_expr='gte')
    current_time = django_filters.DateTimeFromToRangeFilter(field_name='current_time', lookup_expr='gte')
    stock_name = django_filters.CharFilter(field_name='stock_name')
    now_price = django_filters.CharFilter(field_name='now_price')
    open_price = django_filters.CharFilter(field_name='open_price')
    close_price = django_filters.CharFilter(field_name='close_price')
    high_price = django_filters.CharFilter(field_name='high_price')
    low_price = django_filters.CharFilter(field_name='low_price')
    turnover_of_shares = django_filters.CharFilter(field_name='turnover_of_shares')
    trading_volume = django_filters.CharFilter(field_name='trading_volume')

    class Meta:
        model = GenericStockMarketData
        fields = [
            'id',
            'stock_code',
            'stock_name',
            'now_price',
            'open_price',
            'close_price',
            'high_price',
            'low_price',
            'turnover_of_shares',
            'trading_volume',
            'create_time',
            'current_time'
        ]


class GenericStockMarketDataViewSet(ModelViewSet):
    queryset = GenericStockMarketData.objects.all()
    serializer_class = GenericStockMarketDataSerializer
    filter_class = GenericStockMarketDataFilter
    search_fields = ('id', 'stock_code')
