# 用户认证视图
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.http import JsonResponse
import json


def register_view(request):
    """用户注册页面"""
    return render(request, 'registration/register.html')


@require_http_methods(["POST"])
def register_api(request):
    """用户注册 API"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        user_category = data.get('user_category', 'job_seeker')

        # 验证必填字段
        if not username or not email or not password:
            return JsonResponse({
                'status': 'error',
                'message': '请填写所有必填字段'
            }, status=400)

        # 验证密码
        if password != password_confirm:
            return JsonResponse({
                'status': 'error',
                'message': '两次输入的密码不一致'
            }, status=400)

        if len(password) < 6:
            return JsonResponse({
                'status': 'error',
                'message': '密码长度不能少于6位'
            }, status=400)

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': '用户名已存在'
            }, status=400)

        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'status': 'error',
                'message': '邮箱已被注册'
            }, status=400)

        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )

        # 创建用户资料
        from .models import UserProfile
        profile = UserProfile.objects.create(
            user=user,
            phone=data.get('phone', ''),
            user_category=user_category
        )

        # 登录用户
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

        return JsonResponse({
            'status': 'success',
            'message': '注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '请求数据格式错误'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'注册失败: {str(e)}'
        }, status=500)


def profile_view(request):
    """用户个人中心页面"""
    if not request.user.is_authenticated:
        return redirect('/login/')

    user = request.user
    profile = getattr(user, 'profile', None)

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@require_http_methods(["POST"])
def profile_api(request):
    """更新用户资料 API"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': '请先登录'
        }, status=401)

    try:
        data = json.loads(request.body)

        # 更新 User 字段
        user = request.user
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        user.save()

        # 更新 UserProfile 字段
        profile = getattr(user, 'profile', None)
        if profile:
            profile_fields = [
                'phone', 'gender', 'birthday', 'department',
                'position', 'bio', 'wechat', 'qq', 'linkedin'
            ]
            for field in profile_fields:
                if field in data:
                    setattr(profile, field, data[field])
            profile.save()

        return JsonResponse({
            'status': 'success',
            'message': '资料更新成功'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'更新失败: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
def logout_api(request):
    """用户登出 API"""
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': '退出成功'
    })
