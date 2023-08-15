# -*- coding: utf-8 -*-
from rest_framework import serializers

from offer_data.models import GenericStockMarketData


class GenericStockMarketDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericStockMarketData
        fields = "__all__"
