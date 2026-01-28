#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "版权所有@源码商城：https://codes-index.taobao.com/"
__date__ = "2020/6/13 1:03 下午"

from django.contrib import admin

from .models import (
    CompanyInfo, Advantages, IndexAsk,
    FriendlyLinks, GetMessages, Comments, Province, City
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """配置后台公司信息"""
    list_display = ['name', 'phone', 'fax', 'email', 'linkman', 'telephone', 'qq']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    """配置后台产品优势"""
    list_display = ['id', 'title', 'info']
    search_fields = ['title']


@admin.register(IndexAsk)
class IndexAskAdmin(admin.ModelAdmin):
    """配置后台首页咨询"""
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(FriendlyLinks)
class FriendlyLinksAdmin(admin.ModelAdmin):
    """配置后台友情链接"""
    list_display = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']


@admin.register(GetMessages)
class GetMessagesAdmin(admin.ModelAdmin):
    """配置后台游客留言"""
    list_display = ['name', 'phone', 'email', 'is_handle']
    list_filter = ['is_handle']
    search_fields = ['name', 'phone', 'email']
    list_per_page = 20


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """配置后台游客评论"""
    list_display = ['ip', 'category', 'obj_pk', 'add_time', 'is_display']
    list_filter = ['ip', 'category', 'is_display']
    search_fields = ['ip']


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """配置后台省份信息"""
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """配置后台市区信息"""
    list_display = ['id', 'name', 'province']
    list_filter = ['province']
    search_fields = ['name']
