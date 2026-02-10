#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "版权所有@源码商城：https://codes-index.taobao.com/"
__date__ = "2020/6/13 1:03 下午"

from django.contrib import admin

from .models import City, CompanyInfo, FriendlyLinks, Province


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """配置后台公司信息"""

    list_display = ["name", "phone", "fax", "email", "linkman", "telephone", "qq"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(FriendlyLinks)
class FriendlyLinksAdmin(admin.ModelAdmin):
    """配置后台友情链接"""

    list_display = ["id", "title"]
    list_filter = ["title"]
    search_fields = ["title"]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """配置后台省份信息"""

    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """配置后台市区信息"""

    list_display = ["id", "name", "province"]
    list_filter = ["province"]
    search_fields = ["name"]
