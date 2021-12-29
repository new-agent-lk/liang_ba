#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "版权所有@源码商城：https://codes-index.taobao.com/"
__date__ = "2020/6/13 1:03 下午"

# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块

import json
from django.shortcuts import render, HttpResponse  # 用于后台渲染页面
from django.views.generic import View  # 使用django的视图类
from django.core.paginator import Paginator  # 分页器
from django.shortcuts import get_object_or_404  # 404报错模式获取对象

from .models import *


class IndexView(View):
    """首页视图"""

    def get(self, request):
        # 处理get请求的函数
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象
            carousels = Carousls.objects.all()  # 获取所有轮播图

            # 获取产品信息，最多获取9条
            products = Products.objects.all().order_by('-add_time')
            products = products[:9] if len(products) > 9 else products

            # 获取首页咨询，因为前端有两处内容，所以仅获取最新的两条记录，必须有两条记录
            indexasks = IndexAsk.objects.all().order_by('-id')
            if indexasks:
                if len(indexasks) > 1:
                    indexask_1 = indexasks[0]
                    indexask_2 = indexasks[1]
                else:
                    indexask_1 = indexask_2 = indexasks[0]
            else:
                indexask_1 = indexask_2 = []

            # 获取产品优势，最多获取3条
            advantages = Advantages.objects.all().order_by('-id')
            advantages = advantages[:3] if len(advantages) > 3 else advantages

            # 获取工程案例，最多获取9条
            projects = Projects.objects.all().order_by('-add_time')
            projects = projects[:9] if len(projects) > 9 else projects

            # 获取新闻数据，最多获取8条
            news = News.objects.all().order_by('-add_time')
            news = news[:8] if len(news) > 8 else news

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'carousels': carousels,
                'products': products,
                'indexask_1': indexask_1,
                'indexask_2': indexask_2,
                'advantages': advantages,
                'projects': projects,
                'news': news,
            }

            return render(request, 'index.html', context)
        except BaseException as e:
            return render(request, 'index.html', {})


class AboutView(View):
    """关于我们"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            # product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            # left_products = Products.objects.all()  # 默认按照id排序
            # if len(left_products) > 4: left_products = left_products[:4]  # 只获取前4个产品
            # for product in left_products:
            #     if len(product.name) > 6: product.name = product.name[:6] + '...'

            context = {
                'companyinfo': companyinfo,
                # 'product_cats': product_cats,
                'friendly_links': friendly_links,
                # 'left_products': left_products,
            }

            return render(request, '关于我们.html', context)
        except BaseException as e:
            return render(request, '关于我们.html', {})


class ProductsView(View):
    """产品中心"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 产品分类管理
            category = request.GET.get('category', '')
            keywords = request.GET.get('keywords', '')  # 处理搜索功能
            if category and ProductCats.objects.filter(id=category):  # 判断是否有该分类
                products = Products.objects.filter(category=category).order_by('id')  # 获取该分类下的所有产品
            elif keywords:
                products = Products.objects.filter(name__icontains=keywords).order_by('id')  # icontains 为忽略大小写；

            # 分页功能
            paginator = Paginator(products, 9)  # 每页显示9个对象
            page = request.GET.get('page', '')
            try:
                products = paginator.page(page)
            except BaseException as e:
                products = paginator.page(1)  # 出现任何异常，均显示第一页

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
            }

            return render(request, '产品列表.html', context)
        except BaseException as e:
            return render(request, '产品列表.html', {})


class ProductDetailView(View):
    """产品中心-产品详情"""

    def get(self, request, pk):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            # 获取指定的产品信息
            product_pk = pk
            product = get_object_or_404(Products, pk=product_pk)  # 404报错模式获取对象
            product_pics = ProductPics.objects.filter(product_id=product_pk)  # 获取该产品的所有图片

            # 每浏览一次，人气加1
            product.click_nums += 1
            product.save()

            # 判断是否指定了产品分类
            product_cat = request.GET.get('category', '')
            keywords = request.GET.get('keywords', '')  # 处理搜索功能
            if product_cat:
                products = products.filter(category=product.category).order_by('id')  # 获取该分类下的所有产品，不要使用前端传过来的分类参数
            elif keywords:
                products = Products.objects.filter(name__icontains=keywords).order_by('id')  # icontains 为忽略大小写；

            pre_product = products.filter(id__lt=product_pk).order_by('-id').first()  # 上一篇
            next_product = products.filter(id__gt=product_pk).first()  # 下一篇

            # 获取该产品的所有评论
            comments = Comments.objects.filter(category='cp', obj_pk=product_pk, is_display=True)

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
                'product': product,
                'product_pics': product_pics,
                'pre_product': pre_product,
                'next_product': next_product,
                'comments': comments,
            }

            return render(request, '产品页面.html', context)
        except BaseException as e:
            return render(request, '产品页面.html', {})

    def post(self, request, pk):
        content = request.POST.get('content', '')  # 获取评论内容

        # 获取用户IP地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP

        try:
            get_object_or_404(Products, pk=pk)  # 判断是否有该产品
            Comments(ip=ip, msg=content, category='cp', obj_pk=pk).save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')


class NewsView(View):
    """新闻动态"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 分类管理
            category = request.GET.get('category', '')
            if category:
                news = News.objects.filter(category=category).order_by('-add_time')
            else:
                news = News.objects.all().order_by('-add_time')

            # 分页功能
            paginator = Paginator(news, 5)  # 每页显示9个对象
            page = request.GET.get('page', '')
            try:
                news = paginator.page(page)
            except BaseException as e:
                news = paginator.page(1)  # 出现任何异常，均显示第一页

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
                'news': news,
            }

            return render(request, '新闻列表.html', context)
        except BaseException as e:
            return render(request, '新闻列表.html', {})


class NewsDetailView(View):
    """新闻动态-新闻详情"""

    def get(self, request, pk):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            # 获取指定的新闻信息
            new_pk = pk
            new_ = get_object_or_404(News, pk=new_pk)  # 404报错模式获取对象

            # 每浏览一次，人气加1
            new_.click_nums += 1
            new_.save()

            # 判断是否指定了分类
            new_cat = request.GET.get('category', '')
            if new_cat:
                news = News.objects.filter(category=new_.category).order_by('id')  # 获取该分类下的所有对象，不要使用前端传过来的分类参数
            else:
                news = News.objects.all().order_by('id')

            pre_new = news.filter(id__lt=new_pk).order_by('-id').first()  # 上一篇
            next_new = news.filter(id__gt=new_pk).first()  # 下一篇

            # 获取该对象的所有评论
            comments = Comments.objects.filter(category='xw', obj_pk=new_pk, is_display=True)

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
                'new_': new_,
                'pre_new': pre_new,
                'next_new': next_new,
                'comments': comments,
            }

            return render(request, 'new.html', context)
        except BaseException as e:
            return render(request, 'new.html', {})

    def post(self, request, pk):
        content = request.POST.get('content', '')  # 获取评论内容

        # 获取用户IP地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP

        try:
            get_object_or_404(News, pk=pk)  # 判断是否有该对象
            Comments(ip=ip, msg=content, category='xw', obj_pk=pk).save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')


class DemosView(View):
    """工程案例"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 分类管理
            category = request.GET.get('category', '')
            if category:
                projects = Projects.objects.filter(category=category).order_by('-add_time')
            else:
                projects = Projects.objects.all().order_by('-add_time')

            # 分页功能
            paginator = Paginator(projects, 9)  # 每页显示9个对象
            page = request.GET.get('page', '')
            try:
                projects = paginator.page(page)
            except BaseException as e:
                projects = paginator.page(1)  # 出现任何异常，均显示第一页

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
                'projects': projects,
            }

            return render(request, '案例中心.html', context)
        except BaseException as e:
            return render(request, '案例中心.html', {})


class DemoDetailView(View):
    """工程案例-案例详情"""

    def get(self, request, pk):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            products = Products.objects.all().order_by('id')  # 默认按照id排序
            left_products = products[:4] if len(products) > 4 else products  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 底部新闻资讯推荐
            foot_news = News.objects.all().order_by('-add_time')  # 按照添加时间倒序排序，即为最新的咨询
            if len(foot_news) > 6: foot_news = foot_news[:8]  # 只获取前6个

            # 获取指定的新闻信息
            project_pk = pk
            project_ = get_object_or_404(Projects, pk=project_pk)  # 404报错模式获取对象

            # 每浏览一次，人气加1
            project_.click_nums += 1
            project_.save()

            # 判断是否指定了分类
            project_cat = request.GET.get('category', '')
            if project_cat:
                projects = Projects.objects.filter(category=project_.category).order_by(
                    'id')  # 获取该分类下的所有对象，不要使用前端传过来的分类参数
            else:
                projects = Projects.objects.all().order_by('id')

            pre_project = projects.filter(id__lt=project_pk).order_by('-id').first()  # 上一篇
            next_project = projects.filter(id__gt=project_pk).first()  # 下一篇

            # 获取该对象的所有评论
            comments = Comments.objects.filter(category='al', obj_pk=project_pk, is_display=True)

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'products': products,
                'foot_news': foot_news,
                'project_': project_,
                'pre_project': pre_project,
                'next_project': next_project,
                'comments': comments,
            }

            return render(request, '案例页面.html', context)
        except BaseException as e:
            return render(request, '案例页面.html', {})

    def post(self, request, pk):
        content = request.POST.get('content', '')  # 获取评论内容

        # 获取用户IP地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP

        try:
            get_object_or_404(News, pk=pk)  # 判断是否有该对象
            Comments(ip=ip, msg=content, category='al', obj_pk=pk).save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')


class RecruitsView(View):
    """人才招聘"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            # product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            # left_products = Products.objects.all()  # 默认按照id排序
            # if len(left_products) > 4: left_products = left_products[:4]  # 只获取前4个产品
            # for product in left_products:
            #     if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 获取对象
            recruit_cat = request.GET.get('category', '')
            if recruit_cat == 'zwfb':
                recruits = Recruits.objects.filter(category='zwfb').order_by('-id')
            else:
                recruits = Recruits.objects.filter(category='rcln').order_by('-id')
            recruit = recruits[0] if recruits else []

            context = {
                'companyinfo': companyinfo,
                # 'product_cats': product_cats,
                'friendly_links': friendly_links,
                # 'left_products': left_products,
                'recruit': recruit,
            }

            return render(request, '人才招聘.html', context)
        except BaseException as e:
            return render(request, '人才招聘.html', {})


class ContactView(View):
    """联系我们"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            product_cats = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象

            left_products = Products.objects.all()  # 默认按照id排序
            if len(left_products) > 4: left_products = left_products[:4]  # 只获取前4个产品
            for product in left_products:
                if len(product.name) > 6: product.name = product.name[:6] + '...'

            # 获取对象
            recruit_cat = request.GET.get('category', '')
            if recruit_cat == 'zwfb':
                recruits = Recruits.objects.filter(category='zwfb').order_by('-id')
            else:
                recruits = Recruits.objects.filter(category='rcln').order_by('-id')
            recruit = recruits[0] if recruits else []

            context = {
                'companyinfo': companyinfo,
                'product_cats': product_cats,
                'friendly_links': friendly_links,
                'left_products': left_products,
                'recruit': recruit,
            }

            return render(request, '联系我们.html', context)
        except BaseException as e:
            return render(request, '联系我们.html', {})


class GetMsgView(View):
    """留言"""

    def post(self, request):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        msg = request.POST.get('msg', '')
        try:
            new_msg = GetMessages()
            new_msg.name = name
            new_msg.phone = phone
            new_msg.email = email
            new_msg.msg = msg
            new_msg.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')


class FavOpposeView(View):
    """处理游客点赞或踩一下"""

    def post(self, request, flag, chose, pk):
        try:
            if flag == 'news':
                new_ = get_object_or_404(News, pk=pk)
                if chose == 'fav':
                    new_.fav_nums += 1
                    new_.save()
                    return HttpResponse('success')
                else:
                    new_.oppose_nums += 1
                    new_.save()
                    return HttpResponse('success')
            elif flag == 'demo':
                project_ = get_object_or_404(Projects, pk=pk)
                if chose == 'fav':
                    project_.fav_nums += 1
                    project_.save()
                    return HttpResponse('success')
                else:
                    project_.oppose_nums += 1
                    project_.save()
                    return HttpResponse('success')
            else:
                return HttpResponse('failed')
        except BaseException as e:
            return HttpResponse('failed')
