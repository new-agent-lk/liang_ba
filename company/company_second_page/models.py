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


class CompanySecondPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('banner_images', label="Banner images"),
    ]


class CompanySecondPageBannerImage(Orderable):
    page = ParentalKey(CompanySecondPage, on_delete=models.CASCADE, related_name='banner_images')
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