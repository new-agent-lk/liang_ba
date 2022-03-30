# -*- coding: utf-8 -*-
import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework.viewsets import ModelViewSet

from data_apps.models import GenericStockMarketData
from data_apps.serializers.generic_stock_market_data import GenericStockMarketDataSerializer


class GenericStockMarketDataFilter(FilterSet):
    create_time = django_filters.DateTimeFromToRangeFilter(field_name='create_time')
    current_time = django_filters.DateTimeFromToRangeFilter(field_name='current_time')
    stock_name = django_filters.CharFilter(field_name='stock_name')
    now_price = django_filters.NumberFilter(field_name='now_price')
    open_price = django_filters.NumberFilter(field_name='open_price')
    close_price = django_filters.NumberFilter(field_name='close_price')
    high_price = django_filters.NumberFilter(field_name='high_price')
    low_price = django_filters.NumberFilter(field_name='low_price')
    turnover_of_shares = django_filters.NumberFilter(field_name='turnover_of_shares')
    trading_volume = django_filters.NumberFilter(field_name='trading_volume')

    class Meta:
        model = GenericStockMarketData
        fields = {

        }
        # fields = {
        #     'stock_code': ['contains', 'exact'],
        #     'stock_name': ['exact', 'contains'],
        #     'now_price': ['__all__'],
        #     'open_price': ['__all__'],
        #     'close_price': ['__all__'],
        #     'high_price': ['__all__'],
        #     'low_price': ['__all__'],
        #     'turnover_of_shares': ['__all__'],
        #     'trading_volume': ['__all__'],
        #     'create_time': ['__all__'],
        #     'current_time': ['__all__']
        # }


class GenericStockMarketDataViewSet(ModelViewSet):
    queryset = GenericStockMarketData.objects.all()
    serializer_class = GenericStockMarketDataSerializer
    filter_class = GenericStockMarketDataFilter
    search_fields = ('id', 'stock_code')
    ordering_fields = ('current_time', )
