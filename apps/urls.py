from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include

from apps.view import IndexView
from apps.companyinfo.views import *  # 引入首页视图类

urlpatterns = [
    path('admin/', admin.site.urls),

    # re_path(r'^$', IndexView.as_view(), 'index'),
    path('manage/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('api/admin/', include('apps.admin_api.urls')),
    path('api/reports/', include('apps.reports.api_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器
    path('search/', SearchView.as_view(), name='search'),

    path('news/', NewsListView.as_view(), name='news'),  # 新闻动态

    # 研究报告
    path('reports/', include('apps.reports.urls')),

    # 量化因子分析
    path('api/factorhub/', include('apps.factorhub.urls')),

    # 简历投递
    path('resume/', ResumeView.as_view(), name='resume'),
    path('resume/submit/', ResumeSubmitView.as_view(), name='resume_submit'),
    path('resume/success/', ResumeSuccessView.as_view(), name='resume_success'),

    # 用户认证
    path('', include('apps.users.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    re_path(r'', include(wagtail_urls))

    # path('docs/', include_docs_urls(title='LIANG BA API')),
    # path('index/', IndexView.as_view(), name='index_1'),  # 定义首页路由
    # path('products/', ProductsView.as_view(), name='products'),  # 产品中心
    # path('productdetail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # 产品详情
    # path('news/', NewsView.as_view(), name='news'),  # 新闻动态
    # path('newsdetail/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # 新闻详情
    # path('demos/', DemosView.as_view(), name='demos'),  # 工程案例
    # path('demodetail/<int:pk>/', DemoDetailView.as_view(), name='demo_detail'),  # 案例详情
    # path('recruits/', RecruitsView.as_view(), name='recruits'),  # 人才招聘
    # path('getmsg/', GetMsgView.as_view(), name='getmsg'),  # 留言
    # path('fav_oppose/<slug:flag>/<slug:chose>/<int:pk>/', FavOpposeView.as_view(), name='fav_oppose'),  # 游客点赞或踩一下
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
