from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from companyinfo.models import CompanyInfo, ProductCats, FriendlyLinks, News
from companyinfo.models import City
# Create your models here.


class CompanySitePage(Page):
    index_ask_title = models.CharField(verbose_name='首页咨询标题', max_length=25, default="XXX")
    index_ask_info = models.CharField(verbose_name='首页咨询内容', max_length=50, default="XXX")

    content_panels = Page.content_panels + [
        InlinePanel('banner_images', label="Banner images"),
        InlinePanel('advantages_images', label="Advantages images"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        news = News.objects.all().order_by('-add_time')
        news = news[:8] if len(news) > 8 else news
        context['news'] = news
        return context


class CompanySitePageBannerImage(Orderable):
    page = ParentalKey(CompanySitePage, on_delete=models.CASCADE, related_name='banner_images')
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


class CompanySitePageAdvantagesImage(Orderable):
    page = ParentalKey(CompanySitePage, on_delete=models.CASCADE, related_name='advantages_images')
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


class CompanySiteChildPage(Page):
    content = RichTextField(blank=True)
    navigation = models.CharField(verbose_name='标题', max_length=255, default='关于我们')

    def top_image(self):

        top_image = self.child_images.first()

        if top_image:
            content = {'image': top_image.child_image, 'info': top_image.info}
            return content
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
        FieldPanel('navigation'),
        InlinePanel('child_images', label="Child images"),
    ]

    def get_context(self, request):

        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        return context


class CompanySiteChildPageImage(Orderable):
    page = ParentalKey(CompanySiteChildPage, on_delete=models.CASCADE, related_name='child_images')
    child_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    info = models.CharField(verbose_name='介绍', blank=True, null=True, max_length=250)
    title = models.CharField(verbose_name='标题', max_length=10, null=True, blank=True)

    panels = [
        ImageChooserPanel('child_image'),
        FieldPanel('info'),
        FieldPanel('title'),
    ]