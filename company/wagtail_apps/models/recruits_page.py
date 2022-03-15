from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_apps.models.content_page import CompanyContentPage
from companyinfo.models import CompanyInfo, FriendlyLinks


class CompanyRecruitsPage(Page):
    info = RichTextField(null=True, blank=True)
    campus_intro = models.CharField(verbose_name='校园招聘介绍', max_length=255, null=True, blank=True)
    social_intro = models.CharField(verbose_name='社会招聘介绍', max_length=255, null=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('info', classname='full'),
        FieldPanel('campus_intro'),
        FieldPanel('social_intro'),
        InlinePanel('banner_images', label="Banner images")
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
        context = super(CompanyRecruitsPage, self).get_context(request)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象

        campus_recruitments = CompanyContentPage.objects.filter(category='Recruits', page_type='校园招聘').live().order_by(
            'first_published_at')
        Social_recruitments = CompanyContentPage.objects.filter(category='Recruits', page_type='社会招聘').live().order_by(
            'first_published_at')
        context['campus_recs'] = campus_recruitments
        context['social_recs'] = Social_recruitments
        return context


class CompanyRecruitsPageBannerImage(Orderable):
    page = ParentalKey(CompanyRecruitsPage, on_delete=models.CASCADE, related_name='banner_images')
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
