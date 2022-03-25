from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url  # 添加include方法

from companyinfo.views import *  # 引入首页视图类

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # 第三方后台样式，一定要放在admin路由前面
    path('admin/', admin.site.urls),


    path('manage/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('api/v1/data/', include('data_apps.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器
    path('index/', IndexView.as_view(), name='index'),  # 定义首页路由
    path('about/', AboutView.as_view(), name='about'),  # 关于我们
    # path('products/', ProductsView.as_view(), name='products'),  # 产品中心
    # path('productdetail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # 产品详情
    # path('news/', NewsView.as_view(), name='news'),  # 新闻动态
    path('news/', NewsListView.as_view(), name='news'),  # 新闻动态
    # path('newsdetail/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # 新闻详情
    # path('demos/', DemosView.as_view(), name='demos'),  # 工程案例
    # path('demodetail/<int:pk>/', DemoDetailView.as_view(), name='demo_detail'),  # 案例详情
    # path('recruits/', RecruitsView.as_view(), name='recruits'),  # 人才招聘
    path('contact/', ContactView.as_view(), name='contact'),  # 联系我们
    path('search/', SearchView.as_view(), name='search'),
    # path('getmsg/', GetMsgView.as_view(), name='getmsg'),  # 留言
    # path('fav_oppose/<slug:flag>/<slug:chose>/<int:pk>/', FavOpposeView.as_view(), name='fav_oppose'),  # 游客点赞或踩一下

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/media/favicon.ico')),

    re_path(r'', include(wagtail_urls)),
]


