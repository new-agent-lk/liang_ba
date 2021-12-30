import re

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel, BaseChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from companyinfo.models import CompanyInfo, ProductCats, FriendlyLinks, News
from companyinfo.models import City


# Create your models here.


class CompanyContentPage(Page):
    CONTENT_PAGE_CATEGORIES = (
        ('Our Opinions', 'Our Opinions'),
        ('Our Advantages', 'Our Advantages'),
        ('Our Future', 'Our Future'),
    )
    category = models.CharField(verbose_name='文章分类', max_length=255, default='Our Opinions',
                                choices=CONTENT_PAGE_CATEGORIES)
    navigation = models.CharField(verbose_name='页面内标题', max_length=255, default='关于我们')
    page_intro = models.CharField(verbose_name='页面简要介绍', max_length=512, default='简要介绍')
    page_intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='首页内容介绍图片'
    )

    content_stream = StreamField([
        ('source_code', blocks.RawHTMLBlock()),
        ('big_title', blocks.CharBlock(max_length=512, help_text='大标题')),
        ('content', blocks.ListBlock(blocks.RichTextBlock(help_text='内容'), help_text='这里可以填入多个内容，也可以只填写一个')),

        ('author_info', blocks.StructBlock([
            ('ico_image', ImageChooserBlock(help_text='头像')),
            ('author_name', blocks.CharBlock(max_length=255, help_text='作者')),
            ('author_intro', blocks.CharBlock(max_length=255, help_text='作者介绍')),
        ], null=True, blank=True, max_num=1, help_text='作者信息')),

    ], blank=True, null=True, block_counts={
        'big_title': {'max_num': 1},
        'content': {'max_num': 1},
        'author_info': {'max_num': 1},
    })

    search_fields = [
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
        match_list = []
        for block in self.content_stream:
            if block.block_type == 'content':
                match_list = re.findall(r"(?<=>)[^}]+(?=<)", str(block.value[0]), re.S)
        if match_list:
            return match_list[0][:50]
        return ""

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('navigation'),
        FieldPanel('page_intro'),
        ImageChooserPanel('page_intro_image'),
        StreamFieldPanel('content_stream'),
        InlinePanel('child_images', label="Child images"),
    ]

    def get_context(self, request):

        context = super().get_context(request)
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
        ImageChooserPanel('child_image'),
        FieldPanel('info'),
        FieldPanel('title'),
    ]

