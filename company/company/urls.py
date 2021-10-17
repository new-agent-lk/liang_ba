"""company URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
__author__ = "版权所有@源码商城：https://codes-index.taobao.com/"
__date__ = "2020/6/13 1:03 下午"

from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url  # 添加include方法

from companyinfo.views import *  # 引入首页视图类

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # 第三方后台样式，一定要放在admin路由前面
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器
    path('', IndexView.as_view(), name='index'),  # 定义首页路由
    path('about/', AboutView.as_view(), name='about'),  # 关于我们
    path('products/', ProductsView.as_view(), name='products'),  # 产品中心
    path('productdetail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # 产品详情
    path('news/', NewsView.as_view(), name='news'),  # 新闻动态
    path('newsdetail/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # 新闻详情
    path('demos/', DemosView.as_view(), name='demos'),  # 工程案例
    path('demodetail/<int:pk>/', DemoDetailView.as_view(), name='demo_detail'),  # 案例详情
    path('recruits/', RecruitsView.as_view(), name='recruits'),  # 人才招聘
    path('contact/', ContactView.as_view(), name='contact'),  # 联系我们
    path('getmsg/', GetMsgView.as_view(), name='getmsg'),  # 留言
    path('fav_oppose/<slug:flag>/<slug:chose>/<int:pk>/', FavOpposeView.as_view(), name='fav_oppose'),  # 游客点赞或踩一下
]

if settings.DEBUG:
    #  配置静态文件访问问题的处理，防患于未然
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))
