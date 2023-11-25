from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel

from wagtail_apps.models.content_page import CompanyContentPage
from companyinfo.models import CompanyInfo, FriendlyLinks


class CompanyThirdPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('banner_images', label="Banner images"),
    ]

    def top_image(self):
        top_image = self.banner_images.first()
        if top_image:
            private_context = {'banner_image': top_image.banner_image, 'info': top_image.info,
                               'info_title': top_image.info_title}
            return private_context
        else:
            return None

    def get_context(self, request):
        context = super().get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象

        query_set = CompanyContentPage.objects.filter(category='Our Future').live().order_by('first_published_at')
        context['content_page_count'] = len(query_set)
        context['content_pages'] = query_set
        return context


class CompanyThirdPageBannerImage(Orderable):
    page = ParentalKey(CompanyThirdPage, on_delete=models.CASCADE, related_name='banner_images')
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
        FieldPanel('banner_image'),
        FieldPanel('info'),
        FieldPanel('info_title'),
    ]
