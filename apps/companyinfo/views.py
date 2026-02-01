#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块

import json
from django.shortcuts import render, HttpResponse, redirect  # 用于后台渲染页面
from django.views.generic import View, TemplateView  # 使用django的视图类
from django.core.paginator import Paginator  # 分页器
from django.shortcuts import get_object_or_404  # 404报错模式获取对象
from wagtail.search.utils import parse_query_string

from apps.wagtail_apps.models.content_page import CompanyContentPage
from apps.companyinfo.models import *



class SearchView(View):

    def get(self, request):
        query_string = request.GET.get('q')
        if query_string:
            pages = CompanyContentPage.objects.live().filter(navigation__contains=query_string)
        else:
            pages = CompanyContentPage.objects.none()

        companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        context = {
            'companyinfo': companyinfo,
            'friendly_links': friendly_links,
            'pages': pages,
        }

        return render(request, 'news_list.html', context)


class NewsListView(View):
    """新闻动态"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
            friendly_links = FriendlyLinks.objects.all()  # 获取所有友情链接对象
            pages = CompanyContentPage.objects.all()

            context = {
                'companyinfo': companyinfo,
                'friendly_links': friendly_links,
                'pages': pages,
            }

            return render(request, 'news_list.html', context)
        except BaseException as e:
            return render(request, 'news_list.html', {})


class ResumeSubmitView(View):
    """简历投递"""

    def get(self, request):
        # 检查是否已登录
        if not request.user.is_authenticated:
            next_url = '/resume/submit/'
            if request.GET.get('position'):
                next_url += f'?position={request.GET.get("position")}'
            return redirect(f'/login/?next={next_url}')

        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]
            friendly_links = FriendlyLinks.objects.all()

            # 获取正在招聘的岗位 - JobPosition 已在 models.py 中导入
            positions = JobPosition.objects.filter(is_active=True).order_by('sort_order')

            # 获取当前用户信息
            user = request.user
            profile = getattr(user, 'profile', None)

            # 获取URL中的职位参数
            selected_position_id = request.GET.get('position')
            selected_position = None
            if selected_position_id:
                try:
                    selected_position = JobPosition.objects.get(id=selected_position_id)
                except JobPosition.DoesNotExist:
                    pass

            context = {
                'companyinfo': companyinfo,
                'friendly_links': friendly_links,
                'positions': positions,
                'user': user,
                'profile': profile,
                'selected_position': selected_position,
            }

            return render(request, 'resume_submit.html', context)
        except BaseException as e:
            return render(request, 'resume_submit.html', {})

    def post(self, request):
        try:
            from django.utils import timezone
            from datetime import timedelta
            from django.db import transaction, IntegrityError

            # JobPosition 和 Resume 已在 models.py 中导入

            # 处理 JSON 数据（内联表单）和 FormData 数据（完整表单）
            content_type = request.content_type
            if content_type and 'application/json' in content_type:
                data = json.loads(request.body)
                name = data.get('name', '')
                phone = data.get('phone', '')
                email = data.get('email', '')
                position_id = data.get('position', '')
                job_type = data.get('job_type', '')  # campus 或 social
                education = data.get('education', '')
                # 映射 job_type 到 job_category
                if job_type == 'campus':
                    job_category = 'campus_recruit'
                elif job_type == 'social':
                    job_category = 'social_recruit'
                else:
                    job_category = data.get('job_category', '')
            else:
                name = request.POST.get('name', '')
                phone = request.POST.get('phone', '')
                email = request.POST.get('email', '')
                position_id = request.POST.get('position', '')
                job_category = request.POST.get('job_category', '')
                education = request.POST.get('education', '')

            expected_salary = request.POST.get('expected_salary', '')
            school = request.POST.get('school', '')
            major = request.POST.get('major', '')
            skills = request.POST.get('skills', '')
            work_experience = request.POST.get('work_experience', '')
            self_introduction = request.POST.get('self_introduction', '')

            # 获取应聘岗位
            if position_id:
                position = JobPosition.objects.get(id=position_id)
            else:
                position = None

            # 使用数据库事务防止并发重复提交
            with transaction.atomic():
                # 使用行级锁检查最近1分钟内是否提交过相同邮箱的简历
                one_minute_ago = timezone.now() - timedelta(minutes=1)
                recent_count = Resume.objects.filter(
                    email=email,
                    created_at__gte=one_minute_ago
                ).select_for_update().count()

                if recent_count > 0:
                    return HttpResponse(json.dumps({
                        "status": "failed",
                        "message": "请勿重复提交，您刚刚已经投递过简历了"
                    }), content_type='application/json')

                # 创建简历记录
                resume = Resume(
                    name=name,
                    phone=phone,
                    email=email,
                    position=position,
                    job_category=job_category,
                    expected_salary=expected_salary,
                    education=education,
                    school=school,
                    major=major,
                    skills=skills,
                    work_experience=work_experience,
                    self_introduction=self_introduction,
                )

                # 处理文件上传
                if request.FILES.get('resume_file'):
                    resume.resume_file = request.FILES.get('resume_file')

                resume.save()

            return HttpResponse(json.dumps({"status": "success", "message": "简历投递成功！"}), content_type='application/json')
        except IntegrityError:
            return HttpResponse(json.dumps({
                "status": "failed",
                "message": "请勿重复提交，您刚刚已经投递过简历了"
            }), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({"status": "failed", "message": str(e)}), content_type='application/json')


class ResumeSuccessView(View):
    """简历投递成功"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]
            friendly_links = FriendlyLinks.objects.all()

            context = {
                'companyinfo': companyinfo,
                'friendly_links': friendly_links,
            }

            return render(request, 'resume_success.html', context)
        except BaseException as e:
            return render(request, 'resume_success.html', {})


class ResumeView(View):
    """招聘职位页面 - 校园招聘/社会招聘"""

    def get(self, request):
        try:
            companyinfo = CompanyInfo.objects.all().order_by('-id')[0]
            friendly_links = FriendlyLinks.objects.all()

            # 获取正在招聘的岗位 - JobPosition 已在 models.py 中导入
            campus_positions = JobPosition.objects.filter(
                is_active=True, recruitment_type='campus'
            ).order_by('sort_order')
            social_positions = JobPosition.objects.filter(
                is_active=True, recruitment_type='social'
            ).order_by('sort_order')

            context = {
                'companyinfo': companyinfo,
                'friendly_links': friendly_links,
                'campus_positions': campus_positions,
                'social_positions': social_positions,
            }

            return render(request, 'resume.html', context)
        except BaseException as e:
            return render(request, 'resume.html', {})
