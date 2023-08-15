# -*- coding: utf-8 -*-
from rest_framework import serializers

from data_apps.models import GenericStockMarketData


class GenericStockMarketDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericStockMarketData
        fields = "__all__"
