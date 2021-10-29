from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from companyinfo.models import CompanyInfo, ProductCats,FriendlyLinks
# Create your models here.


class CompanySitePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):

        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['product_cats'] = ProductCats.objects.all()  # 获取所有产品分类，用于产品中心的二级菜单
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        return context
