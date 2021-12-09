#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "版权所有@源码商城：https://codes-index.taobao.com/"
__date__ = "2020/6/13 1:03 下午"

from django.contrib import admin

from .models import CompanyInfo, ProductCats, ProductTags, Products, ProductPics, News, Projects, Recruits, Carousls, \
    Advantages, IndexAsk, FriendlyLinks, GetMessages, Comments, Province, City


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """配置后台公司信息"""
    list_display = ['name', 'phone', 'fax', 'email', 'linkman', 'telephone', 'qq']  # 定义该model下内容列表中，展示的属性
    list_filter = ['name']  # 定义可筛选的属性
    search_fields = ['name']  # 定义可搜索的属性


# @admin.register(ProductCats)
# class ProductCatsAdmin(admin.ModelAdmin):
#     """配置后台产品分类"""
#     list_display = ['id', 'name']
#     list_filter = ['name']
#     search_fields = ['name']


# @admin.register(ProductTags)
# class ProductTagsAdmin(admin.ModelAdmin):
#     """配置后台产品标签"""
#     list_display = ['id', 'name']
#     list_filter = ['name']
#     search_fields = ['name']


# @admin.register(Products)
# class ProductsAdmin(admin.ModelAdmin):
#     """配置后台产品信息"""
#     list_display = ['name', 'category', 'add_time', 'click_nums']
#     list_filter = ['name']
#     search_fields = ['name']
#     readonly_fields = ['click_nums']  # 定义后台只读字段，不可在后台管理系统修改


# @admin.register(ProductPics)
# class ProductPicsAdmin(admin.ModelAdmin):
#     """配置后台产品图片"""
#     list_display = ['name', 'product']
#     list_filter = ['name']
#     search_fields = ['name']


# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     """配置后台新闻信息"""
#     list_display = ['title', 'category', 'add_time', 'click_nums', 'fav_nums', 'oppose_nums']
#     list_filter = ['title']
#     search_fields = ['title']
#     readonly_fields = ['click_nums', 'fav_nums', 'oppose_nums']


# @admin.register(Projects)
# class ProjectsAdmin(admin.ModelAdmin):
#     """配置后台工程案例"""
#     list_display = ['title', 'category', 'add_time', 'click_nums', 'fav_nums', 'oppose_nums']
#     list_filter = ['title']
#     search_fields = ['title']
#     readonly_fields = ['click_nums', 'fav_nums', 'oppose_nums']


# @admin.register(Recruits)
# class RecruitsAdmin(admin.ModelAdmin):
#     """配置后台人才招聘"""
#     list_display = ['id', 'category']
#     list_filter = ['category']
#     search_fields = ['category']


# @admin.register(Carousls)
# class CarouslsAdmin(admin.ModelAdmin):
#     """配置后台轮播图"""
#     list_display = ['id', 'title']
#     list_filter = ['title']
#     search_fields = ['title']


# @admin.register(Advantages)
# class AdvantagesAdmin(admin.ModelAdmin):
#     """配置后台公产品优势"""
#     list_display = ['id', 'title']
#     list_filter = ['title']
#     search_fields = ['title']


# @admin.register(IndexAsk)
# class IndexAskAdmin(admin.ModelAdmin):
#     """配置后台首页咨询"""
#     list_display = ['id', 'title']
#     list_filter = ['title']
#     search_fields = ['title']


@admin.register(FriendlyLinks)
class FriendlyLinksAdmin(admin.ModelAdmin):
    """配置后台友情链接"""
    list_display = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']


# @admin.register(GetMessages)
# class GetMessagesAdmin(admin.ModelAdmin):
#     """配置后台游客留言"""
#     list_display = ['name', 'phone', 'email', 'is_handle']
#     list_filter = ['name', 'phone']
#     search_fields = ['name', 'phone']
#
#
# @admin.register(Comments)
# class CommentsAdmin(admin.ModelAdmin):
#     """配置后台游客评论"""
#     list_display = ['ip', 'category', 'obj_pk', 'add_time', 'is_display']
#     list_filter = ['ip']
#     search_fields = ['ip']


# @admin.register(Province)
# class ProvinceAdmin(admin.ModelAdmin):
#     """配置后台省份信息"""
#     list_display = ['name', 'id']
#
#
# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     """配置后台市区信息"""
#     list_display = ['name', 'province', 'id']
