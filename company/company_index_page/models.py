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
from company_content_page.models import CompanyContentPage
# Create your models here.


class CompanyIndexPage(Page):
    index_ask_title = models.CharField(verbose_name='首页咨询标题', max_length=25, default="XXX")
    index_ask_info = models.CharField(verbose_name='首页咨询内容', max_length=50, default="XXX")

    content_panels = Page.content_panels + [
        FieldPanel('index_ask_title'),
        FieldPanel('index_ask_info'),
        InlinePanel('banner_images', label="Banner images"),
    ]

    def top_image(self):
        top_image = self.banner_images.first()
        if top_image:
            content = {'image': top_image.banner_image, 'info': top_image.info, 'info_title': top_image.info_title}
            return content
        else:
            return None

    def get_context(self, request):
        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象

        query_set = CompanyContentPage.objects.filter(category='Our Opinions').live().order_by('first_published_at')
        context['content_page_count'] = len(query_set)
        context['content_pages'] = query_set

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
    info_title = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('banner_image'),
        FieldPanel('info'),
        FieldPanel('info_title'),
    ]
