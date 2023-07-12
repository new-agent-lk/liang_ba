import re

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from companyinfo.models import CompanyInfo, FriendlyLinks
from wagtail_apps.blocks import BasePageStreamBlock, BaseDailyPageStreamBlock


# Create your models here.


class CompanyContentPage(Page):
    CONTENT_PAGE_CATEGORIES = (
        ('Our Opinions', 'Our Opinions'),
        ('Our Advantages', 'Our Advantages'),
        ('Our Future', 'Our Future'),
        ('Recruits', 'Recruits'),
        ('Daily', 'Daily'),
    )
    category = models.CharField(verbose_name='文章分类', max_length=255, default='Our Opinions',
                                choices=CONTENT_PAGE_CATEGORIES)
    navigation = models.CharField(verbose_name='页面内标题', max_length=255, default='关于我们')
    page_intro = models.CharField(verbose_name='页面简要介绍', max_length=512, default='简要介绍')
    page_type = models.CharField(verbose_name='文章类型', max_length=20, default='观点')
    page_intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='首页内容介绍图片'
    )

    content_stream = StreamField(
        BasePageStreamBlock(),
        blank=True,
        null=True,
        block_counts={
            'big_title': {'max_num': 1},
            'content': {'max_num': 1},
            'author_info': {'max_num': 1},
        }, use_json_field=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('navigation'),
    ]

    def top_image(self):
        top_image = self.child_images.first()
        if top_image:
            content = {'image': top_image.child_image, 'info': top_image.info}
            return content
        else:
            return None

    def digest(self):
        content_str = ""
        for block in self.content_stream:
            if block.block_type == 'content':
                # match_list = re.findall(r"(?<=>)[^}]+(?=<)", str(block.value[0]), re.S)
                content_str = re.sub(r"<[^<]+?>", '', str(block.value[0])).replace('\n', '').strip()
                if content_str:
                    return content_str[:50]
        return content_str

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('navigation'),
        FieldPanel('page_intro'),
        FieldPanel('page_type'),
        FieldPanel('page_intro_image'),
        FieldPanel('content_stream'),
        InlinePanel('child_images', label="Child images"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        return context


class CompanyContentPageImage(Orderable):
    page = ParentalKey(CompanyContentPage, on_delete=models.CASCADE, related_name='child_images')
    child_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    info = models.CharField(verbose_name='介绍', blank=True, null=True, max_length=255)
    title = models.CharField(verbose_name='标题', max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('child_image'),
        FieldPanel('info'),
        FieldPanel('title'),
    ]


class CompanyDailyContentPage(Page):
    category = models.CharField(verbose_name='文章分类', max_length=255, default='Daily')
    navigation = models.CharField(verbose_name='页面内标题', max_length=255, default='每日财报')
    page_intro = models.CharField(verbose_name='页面简要介绍', max_length=512, default='简要介绍')
    page_intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='首页内容介绍图片'
    )

    body = StreamField(
        BaseDailyPageStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True,
        block_counts={
            'source_code': {'max_num': 1},
            'big_title': {'max_num': 1},
            'content': {'max_num': 1},
            'ico_image': {'max_num': 1},
            'author_name': {'max_num': 1},
            'author_intro': {'max_num': 1}
        }
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="内容页图片",
    )

    search_fields = Page.search_fields + [
        index.SearchField('navigation'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('navigation'),
        FieldPanel('page_intro'),
        FieldPanel('page_intro_image'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]

    @property
    def first_big_title(self):
        return self.body.first_block_by_name('big_title')

    @property
    def first_ico_image(self):
        return self.body.first_block_by_name('ico_image')

    @property
    def first_author_name(self):
        return self.body.first_block_by_name('author_name')

    @property
    def first_author_intro(self):
        return self.body.first_block_by_name('author_intro')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['companyinfo'] = CompanyInfo.objects.all().order_by('-id')[0]  # 获取最新的一个公司信息对象
        context['friendly_links'] = FriendlyLinks.objects.all()  # 获取所有友情链接对象
        return context

    parent_page_types = ["CompanyDailyPage"]

