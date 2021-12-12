from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from companyinfo.models import CompanyInfo, ProductCats, FriendlyLinks, News
from companyinfo.models import City
# Create your models here.


class CompanyIndexPage(Page):
    index_ask_title = models.CharField(verbose_name='首页咨询标题', max_length=25, default="XXX")
    index_ask_info = models.CharField(verbose_name='首页咨询内容', max_length=50, default="XXX")

    content_panels = Page.content_panels + [
        FieldPanel('index_ask_title'),
        FieldPanel('index_ask_info'),
        InlinePanel('banner_images', label="Banner images"),
        InlinePanel('advantages_images', label="Advantages images"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        context['content_page_count'] = len(self.get_children())

        # news = News.objects.all().order_by('-add_time')
        # news = news[:8] if len(news) > 8 else news
        # context['news'] = news
        return context


class CompanyIndexPageBannerImage(Orderable):
    page = ParentalKey(CompanyIndexPage, on_delete=models.CASCADE, related_name='banner_images')
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    info = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('banner_image'),
        FieldPanel('info'),
    ]


class CompanyIndexPageAdvantagesImage(Orderable):
    page = ParentalKey(CompanyIndexPage, on_delete=models.CASCADE, related_name='advantages_images')
    advantages_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    info = models.CharField(blank=True, null=True, max_length=250)
    title = models.CharField(verbose_name='标题', max_length=10, default='产品优势')

    panels = [
        ImageChooserPanel('advantages_image'),
        FieldPanel('info'),
        FieldPanel('title'),
    ]