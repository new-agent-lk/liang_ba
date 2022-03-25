# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet

from data_apps.models import GenericStockMarketData
from data_apps.serializers.generic_stock_market_data import GenericStockMarketDataSerializer


class GenericStockMarketDataViewSet(ModelViewSet):

    queryset = GenericStockMarketData.objects.all()
    serializer_class = GenericStockMarketDataSerializer

    search_fields = ('id', 'stock_code')

